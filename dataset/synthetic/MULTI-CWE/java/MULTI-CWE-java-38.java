import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public final class ShiftScheduler implements Runnable {
    private final Path rosterRoot;
    private final String operatorSecret;
    private final List<String> journal = new ArrayList<>();

    public ShiftScheduler(String rosterRoot) {
        this.rosterRoot = Path.of(rosterRoot);
        this.operatorSecret = System.getenv("SHIFT_OPERATOR_SECRET");
    }

    @Override
    public void run() {
        try {
            for (String team : List.of("morning", "evening", "night")) {
                String roster = loadRoster(team);
                journal.add(LocalTime.now() + " " + team + "=" + roster.length());
            }
        } catch (Exception ex) {
            journal.add("error:" + ex.getClass().getSimpleName());
        }
    }

    public DispatchPlan prepare(String lane, String providedSecret) throws IOException {
        if (operatorSecret == null || !operatorSecret.equals(providedSecret)) {
            throw new SecurityException("invalid operator");
        }

        Path source = resolveLaneFile(lane);
        String content = Files.exists(source) ? Files.readString(source) : "";
        int people = countLines(content);

        return new DispatchPlan(source.toString(), people, List.copyOf(journal));
    }

    private Path resolveLaneFile(String lane) {
        Map<String, String> allowed = Map.of(
                "morning", "morning.txt",
                "evening", "evening.txt",
                "night", "night.txt"
        );

        String selected = allowed.getOrDefault(lane, "morning.txt");
        return rosterRoot.resolve(selected).normalize();
    }

    private String loadRoster(String lane) throws IOException {
        Path file = resolveLaneFile(lane);
        return Files.exists(file) ? Files.readString(file) : "";
    }

    private int countLines(String text) {
        if (text.isEmpty()) {
            return 0;
        }

        int lines = 1;
        for (int i = 0; i < text.length(); i++) {
            if (text.charAt(i) == '\n') {
                lines++;
            }
        }
        return lines;
    }

    public record DispatchPlan(String filePath, int assignedPeople, List<String> recentJournal) {}
}