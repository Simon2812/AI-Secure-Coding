import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class HealthCheckRunner {

    public static void main(String[] args) throws IOException {

        Properties config = new Properties();
        config.load(new FileInputStream("service.properties"));

        String serviceHost = config.getProperty("service.host");

        if (serviceHost == null) {
            System.out.println("No service.host defined");
            return;
        }

        String cmd = "curl http://" + serviceHost + "/health";

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Running health check for " + serviceHost);
    }
}