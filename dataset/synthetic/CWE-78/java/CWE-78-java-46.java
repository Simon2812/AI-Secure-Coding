import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class TaskExecutor {

    public static void main(String[] args) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader("task.json"));
        String line;
        String targetNode = null;

        while ((line = reader.readLine()) != null) {
            if (line.contains("\"host\"")) {
                targetNode = line.split(":")[1].replace("\"", "").replace(",", "").trim();
            }
        }

        reader.close();

        if (targetNode == null) {
            System.out.println("No host defined in task.json");
            return;
        }

        String cmd = "ssh " + targetNode + " uptime";

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Executed uptime check on " + targetNode);
    }
}