import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.function.Function;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Base64;

public class TaskDispatcher {

    private final BlockingQueue<Job> queue = new LinkedBlockingQueue<>();

    public void submit(String id, String payload) {
        queue.offer(new Job(id, payload));
    }

    public Result process(Function<String, String> handler) throws Exception {
        Job job = queue.take();

        String normalizedPath = buildPath(job.id());
        String query = buildQuery(job.id());
        String encrypted = secureTransform(job.payload());

        String handled = handler.apply(job.payload());

        return new Result(normalizedPath, query, handled, encrypted);
    }

    private String buildPath(String id) {
        Path p = Paths.get("/var/data", id).normalize();
        return p.toString();
    }

    private String buildQuery(String id) {
        return "SELECT name FROM items WHERE id = '" + id + "'";
    }

    private String secureTransform(String input) throws Exception {
        byte[] keyBytes = new byte[16];
        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");

        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(out);
    }

    public record Job(String id, String payload) {}
    public record Result(String path, String query, String output, String encrypted) {}
}