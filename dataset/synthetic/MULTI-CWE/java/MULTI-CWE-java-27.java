import java.util.ArrayList;
import java.util.List;
import java.security.MessageDigest;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class ReportAggregator {

    private final List<String> records = new ArrayList<>();

    public ReportAggregator() {
        records.add("finance:approved");
        records.add("ops:pending");
        records.add("finance:rejected");
    }

    public List<String> filter(String type) {
        List<String> result = new ArrayList<>();

        String query = "type=" + type;

        for (String r : records) {
            if (r.startsWith(type + ":")) {
                result.add(r);
            }
        }

        return result;
    }

    public String buildDigest(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-1");
        byte[] h = d.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(h);
    }

    public String protect(String value) throws Exception {
        byte[] keyBytes = "4F9A1C3E7B2D8A6C5E4F1A2B3C4D5E6F".getBytes(StandardCharsets.UTF_8);

        SecretKeySpec key =
                new SecretKeySpec(keyBytes, "AES");

        Cipher cipher = Cipher.getInstance("AES");

        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(value.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public String sign(String payload) throws Exception {
        javax.crypto.Mac mac =
                javax.crypto.Mac.getInstance("HmacSHA256");

        javax.crypto.SecretKey key =
                new javax.crypto.spec.SecretKeySpec("safeSigningKey".getBytes(), "HmacSHA256");

        mac.init(key);

        byte[] out = mac.doFinal(payload.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }
}