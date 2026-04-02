import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Base64;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.security.SecureRandom;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class BundleAssembler {

    private final Path workspace;
    private final SecureRandom random = new SecureRandom();

    public BundleAssembler(String workspace) {
        this.workspace = Paths.get(workspace);
    }

    public Bundle assemble(String channel, String fileRef, List<String> items) throws Exception {

        String route = resolveChannel(channel);
        Path target = selectFile(fileRef);
        String command = commandFor(route);
        String sealed = protect(items);

        List<String> normalized = new ArrayList<>();
        for (String it : items) {
            normalized.add(it == null ? "" : it.trim());
        }

        return new Bundle(route, target.toString(), command, sealed, normalized.size());
    }

    private String resolveChannel(String raw) {
        Map<String, String> mapping = Map.of(
                "alpha", "route-A",
                "beta", "route-B",
                "gamma", "route-C"
        );
        return mapping.getOrDefault(raw, "route-A");
    }

    private Path selectFile(String ref) {
        String safe = (ref != null && ref.matches("[a-zA-Z0-9._-]+")) ? ref : "bundle.dat";
        return workspace.resolve(safe).normalize();
    }

    private String commandFor(String route) {
        return switch (route) {
            case "route-A" -> "ls";
            case "route-B" -> "whoami";
            case "route-C" -> "date";
            default -> "ls";
        };
    }

    private String protect(List<String> items) throws Exception {
        byte[] key = new byte[16];
        byte[] iv = new byte[12];
        random.nextBytes(key);
        random.nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key, "AES"), new GCMParameterSpec(128, iv));

        String joined = String.join(",", items);
        byte[] out = cipher.doFinal(joined.getBytes(StandardCharsets.UTF_8));

        return Base64.getEncoder().encodeToString(out);
    }

    public record Bundle(String route, String file, String command, String token, int count) {}
}