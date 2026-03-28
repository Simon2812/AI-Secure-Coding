import java.time.LocalTime;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class MeetingScheduler {

    public static final class MeetingRequest {
        public final String id;
        public final int durationMinutes;
        public final Set<String> requiredParticipants;

        public MeetingRequest(String id, int durationMinutes, Set<String> requiredParticipants) {
            this.id = id;
            this.durationMinutes = durationMinutes;
            this.requiredParticipants = new HashSet<>(requiredParticipants);
        }
    }

    public static final class TimeSlot {
        public final LocalTime start;
        public final LocalTime end;

        public TimeSlot(LocalTime start, LocalTime end) {
            this.start = start;
            this.end = end;
        }

        public boolean fits(int durationMinutes) {
            return start.plusMinutes(durationMinutes).compareTo(end) <= 0;
        }
    }

    public static final class Assignment {
        public final String meetingId;
        public final TimeSlot slot;

        public Assignment(String meetingId, TimeSlot slot) {
            this.meetingId = meetingId;
            this.slot = slot;
        }
    }

    private final List<MeetingRequest> requests;
    private final List<TimeSlot> availableSlots;

    public MeetingScheduler(List<MeetingRequest> requests, List<TimeSlot> availableSlots) {
        this.requests = requests;
        this.availableSlots = availableSlots;
    }

    public List<Assignment> solve() {
        List<Assignment> result = new ArrayList<>();
        if (backtrack(0, result, new HashSet<>())) {
            return result;
        }
        return new ArrayList<>();
    }

    private boolean backtrack(
            int index,
            List<Assignment> current,
            Set<String> busyParticipants
    ) {
        if (index == requests.size()) {
            return true;
        }

        MeetingRequest request = requests.get(index);

        for (TimeSlot slot : availableSlots) {
            if (!slot.fits(request.durationMinutes)) {
                continue;
            }

            if (conflicts(request, busyParticipants)) {
                continue;
            }

            assign(request, slot, current, busyParticipants);

            if (backtrack(index + 1, current, busyParticipants)) {
                return true;
            }

            unassign(request, current, busyParticipants);
        }

        return false;
    }

    private boolean conflicts(MeetingRequest request, Set<String> busyParticipants) {
        for (String p : request.requiredParticipants) {
            if (busyParticipants.contains(p)) {
                return true;
            }
        }
        return false;
    }

    private void assign(
            MeetingRequest request,
            TimeSlot slot,
            List<Assignment> current,
            Set<String> busyParticipants
    ) {
        current.add(new Assignment(request.id, slot));
        busyParticipants.addAll(request.requiredParticipants);
    }

    private void unassign(
            MeetingRequest request,
            List<Assignment> current,
            Set<String> busyParticipants
    ) {
        current.remove(current.size() - 1);
        busyParticipants.removeAll(request.requiredParticipants);
    }

    public static MeetingScheduler sampleScenario() {
        List<MeetingRequest> requests = List.of(
                new MeetingRequest("M1", 30, Set.of("Alice", "Bob")),
                new MeetingRequest("M2", 45, Set.of("Bob", "Dana")),
                new MeetingRequest("M3", 30, Set.of("Eli")),
                new MeetingRequest("M4", 60, Set.of("Alice", "Eli"))
        );

        List<TimeSlot> slots = List.of(
                new TimeSlot(LocalTime.of(9, 0), LocalTime.of(10, 0)),
                new TimeSlot(LocalTime.of(10, 0), LocalTime.of(11, 0)),
                new TimeSlot(LocalTime.of(11, 0), LocalTime.of(12, 0))
        );

        return new MeetingScheduler(requests, slots);
    }
}