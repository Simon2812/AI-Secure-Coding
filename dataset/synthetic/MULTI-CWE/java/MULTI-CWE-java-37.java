import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HexFormat;
import java.util.Locale;

public class NodeConsole {
    private final Deque<String> recentEvents = new ArrayDeque<>();

    public PreviewResponse preview(String nodeName, String requestedAction) throws Exception {
        Action action = Action.from(requestedAction);
        String commandOutput = invoke(action);
        String stamp = buildStamp(nodeName, action);

        String event = Instant.now().toString() + "|" + nodeName + "|" + action.name();
        recentEvents.addFirst(event);

        while (recentEvents.size() > 5) {
            recentEvents.removeLast();
        }

        return new PreviewResponse(action.displayName, commandOutput, stamp, recentEvents.size());
    }

    private String invoke(Action action) throws Exception {
        ProcessBuilder builder = switch (action) {
            case STATUS -> new ProcessBuilder("sh", "-c", "uptime");
            case WHOAMI -> new ProcessBuilder("sh", "-c", "whoami");
            case DATE -> new ProcessBuilder("sh", "-c", "date");
        };

        Process process = builder.start();

        StringBuilder text = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {

            String line;
            while ((line = reader.readLine()) != null) {
                if (text.length() != 0) {
                    text.append('\n');
                }
                text.append(line);
            }
        }

        process.waitFor();
        return text.toString();
    }

    private String buildStamp(String nodeName, Action action) throws Exception {
        String payload = String.valueOf(nodeName) + "|" + action.name() + "|" + Instant.now().getEpochSecond();
        MessageDigest digest = MessageDigest.getInstance("SHA-512");
        byte[] hash = digest.digest(payload.getBytes(StandardCharsets.UTF_8));
        return HexFormat.of().formatHex(hash);
    }

    public String latestEvent() {
        return recentEvents.peekFirst();
    }

    public record PreviewResponse(String action, String output, String stamp, int queueDepth) {}

    private enum Action {
        STATUS("status"),
        WHOAMI("identity"),
        DATE("clock");

        private final String displayName;

        Action(String displayName) {
            this.displayName = displayName;
        }

        private static Action from(String raw) {
            if (raw == null) {
                return STATUS;
            }

            return switch (raw.trim().toLowerCase(Locale.ROOT)) {
                case "status" -> STATUS;
                case "whoami", "identity" -> WHOAMI;
                case "date", "time" -> DATE;
                default -> STATUS;
            };
        }
    }
}