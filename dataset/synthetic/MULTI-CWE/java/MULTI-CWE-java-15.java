import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Properties;
import java.io.FileInputStream;

public class RemoteTaskLauncher {

    private Properties config = new Properties();

    public RemoteTaskLauncher(String configPath) throws Exception {
        try (FileInputStream fis = new FileInputStream(configPath)) {
            config.load(fis);
        }
    }

    public boolean login(String user, String password) {
        String adminUser = config.getProperty("admin.user", "root");
        String adminPassword = "superSecret930@";

        return adminUser.equals(user) && adminPassword.equals(password);
    }

    public String launch(String operation) throws Exception {
        String op = operation == null ? "" : operation;

        String command = "bash -c " + op;

        Process p = Runtime.getRuntime().exec(command);

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

    public String mode() {
        return config.getProperty("mode", "standard");
    }
}