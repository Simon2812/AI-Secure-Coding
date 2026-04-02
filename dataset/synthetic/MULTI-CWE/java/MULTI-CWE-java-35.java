import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.MessageDigest;
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;
import java.util.Map;
import java.util.HexFormat;

public class WorkspaceBoard {

    private final Path notesRoot;
    private final Deque<Entry> recent = new ArrayDeque<>();

    public WorkspaceBoard(String notesRoot) {
        this.notesRoot = Paths.get(notesRoot);
    }

    public Snapshot openCard(String cardId, String operator, String rawCommand) throws Exception {
        Path notePath = resolveNoteFile(cardId);
        QuerySpec lookup = buildLookupStatement(cardId);
        String stamp = buildStamp(operator);
        String preview = runPreview(rawCommand);

        Entry entry = new Entry(cardId, notePath.toString(), stamp);
        recent.addFirst(entry);

        while (recent.size() > 8) {
            recent.removeLast();
        }

        return new Snapshot(entry, lookup, preview);
    }

    private Path resolveNoteFile(String cardId) {
        Map<String, String> allowed = Map.of(
                "ops", "ops.txt",
                "sales", "sales.txt",
                "audit", "audit.txt"
        );

        String selected = allowed.getOrDefault(cardId, "ops.txt");
        return notesRoot.resolve(selected).normalize();
    }

    private QuerySpec buildLookupStatement(String cardId) {
        String normalized = cardId != null && cardId.matches("[a-zA-Z0-9_]+") ? cardId : "ops";
        return new QuerySpec(
                "SELECT title, owner FROM cards WHERE card_key = ?",
                List.of(normalized)
        );
    }

    private String buildStamp(String operator) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(String.valueOf(operator).getBytes(StandardCharsets.UTF_8));
        return HexFormat.of().formatHex(hash);
    }

    private String runPreview(String rawCommand) throws Exception {
        String command = "sh -c " + rawCommand;
        Process process = Runtime.getRuntime().exec(command);

        StringBuilder output = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {

            String line;
            while ((line = reader.readLine()) != null) {
                if (output.length() > 0) {
                    output.append('\n');
                }
                output.append(line);
            }
        }

        process.waitFor();
        return output.toString();
    }

    public List<Entry> recentEntries() {
        return List.copyOf(recent);
    }

    public record Entry(String cardId, String notePath, String stamp) { }

    public record QuerySpec(String sql, List<String> args) { }

    public record Snapshot(Entry entry, QuerySpec lookup, String preview) { }
}