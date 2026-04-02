import java.time.Duration;
import java.time.LocalTime;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.Deque;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class CallCenterDeskBoard {

    enum TicketState {
        NEW,
        IN_PROGRESS,
        WAITING_CUSTOMER,
        RESOLVED
    }

    enum QueueName {
        BILLING,
        TECHNICAL,
        ONBOARDING
    }

    record Agent(String code, String fullName, QueueName queue, boolean senior) { }

    record Ticket(
            String ticketNo,
            QueueName queue,
            TicketState state,
            int waitingMinutes,
            int customerMessages,
            boolean escalated
    ) { }

    record Assignment(String ticketNo, String agentCode, LocalTime assignedAt) { }

    private final Map<QueueName, Deque<Ticket>> lanes = new LinkedHashMap<>();
    private final List<Agent> agents = new ArrayList<>();
    private final List<Assignment> history = new ArrayList<>();

    public CallCenterDeskBoard() {
        for (QueueName q : QueueName.values()) {
            lanes.put(q, new ArrayDeque<>());
        }
    }

    public void registerAgent(Agent agent) {
        agents.add(agent);
    }

    public void accept(Ticket ticket) {
        lanes.get(ticket.queue()).addLast(ticket);
    }

    public List<String> dispatchNextWave(LocalTime now) {
        List<String> events = new ArrayList<>();

        for (QueueName queue : QueueName.values()) {
            List<Agent> availablePool = agentsFor(queue);

            if (availablePool.isEmpty()) {
                events.add("No agents available for " + queue);
                continue;
            }

            Deque<Ticket> bucket = lanes.get(queue);
            if (bucket.isEmpty()) {
                continue;
            }

            List<Ticket> candidates = new ArrayList<>(bucket);
            candidates.sort(ticketPriority());

            int index = 0;
            while (index < availablePool.size() && !candidates.isEmpty()) {
                Agent selectedAgent = availablePool.get(index);
                Ticket selectedTicket = removeFirstMatching(bucket, candidates.remove(0).ticketNo());

                if (selectedTicket == null) {
                    continue;
                }

                history.add(new Assignment(selectedTicket.ticketNo(), selectedAgent.code(), now));
                events.add(formatDispatchLine(selectedTicket, selectedAgent, now));
                index++;
            }
        }

        if (events.isEmpty()) {
            events.add("Nothing to dispatch");
        }

        return events;
    }

    public String boardSnapshot() {
        StringBuilder out = new StringBuilder();

        out.append("CALL CENTER DESK BOARD").append('\n');
        out.append("======================").append('\n');

        for (QueueName queue : QueueName.values()) {
            out.append('\n');
            out.append("[").append(queue).append("]").append('\n');

            Deque<Ticket> items = lanes.get(queue);
            if (items.isEmpty()) {
                out.append("  (empty)").append('\n');
                continue;
            }

            List<Ticket> ordered = new ArrayList<>(items);
            ordered.sort(ticketPriority());

            int row = 1;
            for (Ticket t : ordered) {
                out.append("  ")
                   .append(row++)
                   .append(". ")
                   .append(ticketCell(t))
                   .append('\n');
            }
        }

        out.append('\n');
        out.append("Assignments today: ").append(history.size()).append('\n');

        return out.toString();
    }

    public String utilizationDigest() {
        Map<String, Integer> countByAgent = new LinkedHashMap<>();
        for (Agent agent : agents) {
            countByAgent.put(agent.code(), 0);
        }

        for (Assignment item : history) {
            countByAgent.computeIfPresent(item.agentCode(), (k, v) -> v + 1);
        }

        StringBuilder text = new StringBuilder();
        text.append("AGENT LOAD").append('\n');
        text.append("----------").append('\n');

        for (Agent agent : agents) {
            int handled = countByAgent.getOrDefault(agent.code(), 0);
            text.append(agent.code())
                .append(" | ")
                .append(agent.fullName())
                .append(" | ")
                .append(agent.queue())
                .append(" | handled=")
                .append(handled);

            if (agent.senior()) {
                text.append(" | senior");
            }

            text.append('\n');
        }

        return text.toString();
    }

    private Comparator<Ticket> ticketPriority() {
        return Comparator
                .comparing(CallCenterDeskBoard::priorityBand)
                .thenComparing(Ticket::waitingMinutes, Comparator.reverseOrder())
                .thenComparing(Ticket::customerMessages, Comparator.reverseOrder())
                .thenComparing(Ticket::ticketNo);
    }

    private static int priorityBand(Ticket ticket) {
        if (ticket.escalated()) {
            return 0;
        }
        if (ticket.state() == TicketState.IN_PROGRESS) {
            return 1;
        }
        if (ticket.state() == TicketState.WAITING_CUSTOMER) {
            return 3;
        }
        return 2;
    }

    private List<Agent> agentsFor(QueueName queue) {
        List<Agent> result = new ArrayList<>();
        for (Agent agent : agents) {
            if (agent.queue() == queue) {
                result.add(agent);
            }
        }

        result.sort((a, b) -> {
            if (a.senior() == b.senior()) {
                return a.code().compareTo(b.code());
            }
            return a.senior() ? -1 : 1;
        });

        return result;
    }

    private Ticket removeFirstMatching(Deque<Ticket> bucket, String ticketNo) {
        for (Ticket ticket : bucket) {
            if (ticket.ticketNo().equals(ticketNo)) {
                bucket.remove(ticket);
                return ticket;
            }
        }
        return null;
    }

    private String formatDispatchLine(Ticket ticket, Agent agent, LocalTime now) {
        return now + " -> " +
                ticket.ticketNo() +
                " assigned to " +
                agent.fullName() +
                " (" + agent.code() + ", " + agent.queue() + ")";
    }

    private String ticketCell(Ticket ticket) {
        StringBuilder cell = new StringBuilder();

        cell.append(ticket.ticketNo())
            .append(" | ")
            .append(ticket.state())
            .append(" | wait=")
            .append(ticket.waitingMinutes())
            .append("m | msgs=")
            .append(ticket.customerMessages());

        if (ticket.escalated()) {
            cell.append(" | ESCALATED");
        }

        return cell.toString();
    }

    public static void main(String[] args) {
        CallCenterDeskBoard board = new CallCenterDeskBoard();

        board.registerAgent(new Agent("A-14", "Rina Barak", QueueName.BILLING, true));
        board.registerAgent(new Agent("A-22", "Yuval Cohen", QueueName.BILLING, false));
        board.registerAgent(new Agent("T-05", "Maksim Levin", QueueName.TECHNICAL, true));
        board.registerAgent(new Agent("T-08", "Noa Peleg", QueueName.TECHNICAL, false));
        board.registerAgent(new Agent("O-03", "Lior Shani", QueueName.ONBOARDING, false));

        board.accept(new Ticket("INC-3001", QueueName.TECHNICAL, TicketState.NEW, 42, 3, false));
        board.accept(new Ticket("INC-3002", QueueName.TECHNICAL, TicketState.IN_PROGRESS, 18, 5, true));
        board.accept(new Ticket("BIL-1104", QueueName.BILLING, TicketState.NEW, 27, 2, false));
        board.accept(new Ticket("BIL-1109", QueueName.BILLING, TicketState.WAITING_CUSTOMER, 90, 1, false));
        board.accept(new Ticket("ONB-7003", QueueName.ONBOARDING, TicketState.NEW, 12, 4, false));
        board.accept(new Ticket("INC-3014", QueueName.TECHNICAL, TicketState.NEW, 63, 6, true));

        System.out.println(board.boardSnapshot());

        List<String> wave = board.dispatchNextWave(LocalTime.of(9, 15));
        System.out.println("DISPATCH WAVE");
        System.out.println("-------------");
        for (String line : wave) {
            System.out.println(line);
        }

        System.out.println();
        System.out.println(board.boardSnapshot());
        System.out.println(board.utilizationDigest());

        Duration serviceWindow = Duration.between(LocalTime.of(9, 0), LocalTime.of(17, 0));
        System.out.println("Desk window minutes: " + serviceWindow.toMinutes());
    }
}