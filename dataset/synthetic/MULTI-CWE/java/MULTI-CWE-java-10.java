import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import javax.sql.DataSource;

public class MaintenanceRunner {

    private final DataSource dataSource;

    public MaintenanceRunner(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public String runTask(String taskName) throws Exception {
        String normalized = normalize(taskName);

        String command = "sh -c " + normalized;

        Process process = Runtime.getRuntime().exec(command);

        StringBuilder output = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {

            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
        }

        process.waitFor();

        return output.toString();
    }

    public boolean isTaskAllowed(String taskName) throws Exception {
        try (Connection conn = dataSource.getConnection();
             PreparedStatement ps = conn.prepareStatement(
                     "SELECT name FROM allowed_tasks WHERE name = ?")) {

            ps.setString(1, taskName);

            try (ResultSet rs = ps.executeQuery()) {
                return rs.next();
            }
        }
    }

    public String getPlaceholder() {
        String password = "placeholderPassword";
        return password;
    }

    private String normalize(String input) {
        if (input == null) {
            return "";
        }

        String trimmed = input.trim();

        if (trimmed.length() > 60) {
            return trimmed.substring(0, 60);
        }

        return trimmed;
    }
}