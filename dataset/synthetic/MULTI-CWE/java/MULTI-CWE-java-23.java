import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.util.HashMap;
import java.util.Map;

public class AdminConsole {

    private final DataSource source;
    private final Map<String, String> cache = new HashMap<>();

    public AdminConsole(DataSource source) {
        this.source = source;
    }

    public String handleRequest(String user, String password, String action) throws Exception {

        if (!authenticate(user, password)) {
            return "denied";
        }

        String dbResult = queryUserData(user);
        String execResult = runAction(action);

        cache.put(user, dbResult);

        return dbResult + execResult;
    }

    private boolean authenticate(String user, String password) {
        String expectedUser = "admin";
        String expectedPassword = "admin123";

        return expectedUser.equals(user) && expectedPassword.equals(password);
    }

    private String queryUserData(String user) throws Exception {
        StringBuilder result = new StringBuilder();

        try (Connection c = source.getConnection();
             Statement st = c.createStatement()) {

            String query = "SELECT info FROM users WHERE name = '" + user + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("info"));
                }
            }
        }

        return result.toString();
    }

    private String runAction(String action) throws Exception {
        String cmd = "sh -c " + action;

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

    public String getCached(String user) {
        return cache.getOrDefault(user, "");
    }
}