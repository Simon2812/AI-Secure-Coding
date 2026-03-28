import java.io.BufferedReader;
import java.io.InputStreamReader;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class DiagnosticsRunner {

    public String run(String host) throws Exception {
        String target = host == null ? "localhost" : host;

        String cmd = "ping -c 1 " + target;

        Process p = Runtime.getRuntime().exec(cmd);

        StringBuilder out = new StringBuilder();

        try (BufferedReader r = new BufferedReader(
                new InputStreamReader(p.getInputStream()))) {

            String line;
            while ((line = r.readLine()) != null) {
                out.append(line).append("\n");
            }
        }

        p.waitFor();
        return out.toString();
    }

    public String secure(String input) throws Exception {
        byte[] keyBytes = "diagKey12345678".getBytes(StandardCharsets.UTF_8);
        SecretKeySpec key = new SecretKeySpec(keyBytes, "RC4");

        Cipher cipher = Cipher.getInstance("RC4");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public String label() {
        return "diag-mode";
    }
}