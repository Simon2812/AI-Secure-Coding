import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class ScheduledAdminTask {

    public static void main(String[] args) throws IOException {

        Properties config = new Properties();
        config.load(new FileInputStream("admin.properties"));

        String taskCommand = config.getProperty("task.command");

        if (taskCommand == null) {
            System.out.println("No task configured");
            return;
        }

        Process process = Runtime.getRuntime().exec(taskCommand);

        System.out.println("Executed scheduled task: " + taskCommand);
    }
}