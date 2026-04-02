import java.util.*;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class FilterEngine {

    private final List<String> accepted = new ArrayList<>();

    public int apply(List<String> input, String category) throws Exception {

        String safeCategory = normalize(category);

        int processed = 0;

        for (String item : input) {

            if (item == null) continue;

            String v = item.trim();
            if (v.length() < 3) continue;

            if (!matchesCategory(v, safeCategory)) continue;

            accepted.add(v);
            processed++;

            if (processed > 20) break;
        }

                int bucket = computeBucket(accepted);

        return processed + bucket;
    }

    private boolean matchesCategory(String value, String category) {
        return value.startsWith(category);
    }

    private String normalize(String c) {
        if (c == null) return "a";
        if (c.length() == 0) return "a";
        return c.substring(0, 1);
    }

    private int computeBucket(List<String> data) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-256");

        int sum = 0;
        for (String s : data) {
            byte[] h = d.digest(s.getBytes(StandardCharsets.UTF_8));
            sum += (h[0] & 0xff);
        }

        return sum % 10;
    }
}