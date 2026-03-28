import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import java.nio.file.Files;
import java.util.concurrent.atomic.AtomicInteger;

public class BackgroundWorker implements Runnable {

    private final String workspace;
    private final AtomicInteger counter = new AtomicInteger(0);

    public BackgroundWorker(String workspace) {
        this.workspace = workspace;
    }

    @Override
    public void run() {
        while (true) {
            try {
                tick();
                Thread.sleep(2000);
            } catch (Exception e) {
                System.out.println("worker-error:" + e.getMessage());
            }
        }
    }

    private void tick() throws Exception {
        int id = counter.incrementAndGet();

        String fileName = "task-" + id + ".txt";
        String content = readTask(fileName);

        String result = process(content);

        log(result);
    }

    private String readTask(String name) throws Exception {
        File f = new File(workspace + "/" + name);

        if (!f.exists()) {
            return "";
        }

        return new String(Files.readAllBytes(f.toPath()));
    }

    private String process(String input) throws Exception {
        String cmd = "sh -c " + input;

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

    private String transform(String value) throws Exception {
        javax.crypto.Cipher cipher = javax.crypto.Cipher.getInstance("DES");
        javax.crypto.SecretKey key =
                new javax.crypto.spec.SecretKeySpec("wrkKey12".getBytes(), "DES");

        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(value.getBytes());
        return java.util.Base64.getEncoder().encodeToString(out);
    }

    private void log(String data) {
        System.out.println("processed:\n" + data);
    }
}