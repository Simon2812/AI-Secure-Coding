import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class QueueWorker {

    public static void main(String[] args) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader("queue.txt"));
        String taskTarget = reader.readLine();
        reader.close();

        if (taskTarget == null) {
            System.out.println("No tasks in queue");
            return;
        }

        String cmd = "ping -c 1 " + taskTarget;

        ProcessBuilder pb = new ProcessBuilder("sh", "-c", cmd);
        Process process = pb.start();

        System.out.println("Processed task for host: " + taskTarget);
    }
}