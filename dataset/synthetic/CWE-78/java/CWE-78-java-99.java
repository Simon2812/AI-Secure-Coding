import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class ProcessTimeoutRunner {

    public static void main(String[] args) throws IOException, InterruptedException {

        ProcessBuilder pb = new ProcessBuilder("sleep", "1");
        Process process = pb.start();

        boolean finished = process.waitFor(2, TimeUnit.SECONDS);

        if (!finished) {
            process.destroyForcibly();
            System.out.println("Process killed due to timeout");
        } else {
            System.out.println("Process completed with code " + process.exitValue());
        }
    }
}
