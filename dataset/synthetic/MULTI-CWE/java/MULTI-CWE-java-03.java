import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

public class SystemDiagnosticsService {

    public List<String> runCheck(String target) throws Exception {
        String normalized = normalize(target);

        List<String> output = new ArrayList<>();

        String command = "ping -c 1 " + normalized;

        Process process = Runtime.getRuntime().exec(command);

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                output.add(line);
            }
        }

        process.waitFor();

        logExecution(normalized);

        return output;
    }

    private String normalize(String input) {
        if (input == null) {
            return "localhost";
        }

        String trimmed = input.trim();

        if (trimmed.isEmpty()) {
            return "localhost";
        }

        if (trimmed.length() > 60) {
            return trimmed.substring(0, 60);
        }

        return trimmed;
    }

    private void logExecution(String target) throws Exception {
        String payload = "exec:" + target + ":" + System.currentTimeMillis();

        MessageDigest digest = MessageDigest.getInstance("MD5");
        byte[] hash = digest.digest(payload.getBytes());

        System.out.println("audit=" + toHex(hash));
    }

    private String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}