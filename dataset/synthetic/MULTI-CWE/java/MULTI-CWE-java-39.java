import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.HexFormat;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.util.Base64;

public class EdgeGateway {

    private final SecureRandom random = new SecureRandom();
    private final Path base = Paths.get("/srv/edge");

    public GatewayResponse handle(GatewayRequest request) throws Exception {

        String route = routeOf(request.endpoint());
        Path resource = resolveResource(request.resource());
        String fingerprint = fingerprint(request.client());
        String token = encodeToken(request.payload());

        return new GatewayResponse(route, resource.toString(), fingerprint, token);
    }

    private String routeOf(String endpoint) {
        return switch (endpoint == null ? "" : endpoint) {
            case "metrics" -> "metrics-service";
            case "health" -> "health-service";
            default -> "default-service";
        };
    }

    private Path resolveResource(String resource) {
        Map<String, String> allow = Map.of(
                "config", "config.json",
                "state", "state.json",
                "meta", "meta.json"
        );

        String selected = allow.getOrDefault(resource, "config.json");
        return base.resolve(selected).normalize();
    }

    private String fingerprint(String client) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-256");
        byte[] h = d.digest(String.valueOf(client).getBytes(StandardCharsets.UTF_8));
        return HexFormat.of().formatHex(h);
    }

    private String encodeToken(String payload) throws Exception {
        byte[] key = new byte[16];
        byte[] iv = new byte[12];
        random.nextBytes(key);
        random.nextBytes(iv);

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(key, "AES"), new GCMParameterSpec(128, iv));

        byte[] out = cipher.doFinal(String.valueOf(payload).getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public List<String> auditTrail() {
        List<String> data = new ArrayList<>();
        data.add("ok");
        return data;
    }

    public record GatewayRequest(String endpoint, String resource, String client, String payload) {}
    public record GatewayResponse(String route, String path, String fingerprint, String token) {}
}