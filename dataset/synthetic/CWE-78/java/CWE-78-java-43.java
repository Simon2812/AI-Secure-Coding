import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class MaintenanceRunner {

    public static void main(String[] args) throws IOException {

        Properties settings = new Properties();
        settings.load(new FileInputStream("maintenance.properties"));

        String scriptName = settings.getProperty("task.script");

        String execution = String.format("sh %s", scriptName);

        Process proc = Runtime.getRuntime().exec(execution);

        System.out.println("Running maintenance task: " + scriptName);
    }
}