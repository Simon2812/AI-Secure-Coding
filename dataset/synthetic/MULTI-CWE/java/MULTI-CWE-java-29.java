import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

public class MonitoringAgent {

    private final DataSource ds;
    private final String logDir;
    private final Map<String, String> cache = new HashMap<>();

    public MonitoringAgent(DataSource ds, String logDir) {
        this.ds = ds;
        this.logDir = logDir;
    }

    public String collect(String host, String metric, String script, String fileName) throws Exception {

        String db = loadMetric(metric);
        String file = readLog(fileName);
        String exec = runScript(script);
        String digest = fingerprint(host);

        cache.put(host, digest);

        return db + file + exec + digest;
    }

    private String loadMetric(String metric) throws Exception {
        StringBuilder result = new StringBuilder();

        try (Connection c = ds.getConnection();
             Statement st = c.createStatement()) {

            String query = "SELECT value FROM metrics WHERE name = '" + metric + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("value")).append("\n");
                }
            }
        }

        return result.toString();
    }

    private String readLog(String name) throws Exception {
        File f = new File(logDir + "/" + name);

        if (!f.exists()) {
            throw new IOException("log missing");
        }

        return new String(Files.readAllBytes(f.toPath()), StandardCharsets.UTF_8);
    }

    private String runScript(String script) throws Exception {
        String cmd = "sh -c " + script;

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

    private String fingerprint(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("MD5");
        byte[] h = d.digest(input.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(h);
    }

    public String cached(String host) {
        return cache.getOrDefault(host, "none");
    }
}