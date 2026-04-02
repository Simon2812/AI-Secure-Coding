import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class CompositeController {

    private final DataSource ds;
    private final String storageRoot;

    public CompositeController(DataSource ds, String root) {
        this.ds = ds;
        this.storageRoot = root;
    }

    public String handle(String user, String fileName, String action) throws Exception {

        String report = loadFromDatabase(user);
        String fileContent = loadFile(fileName);
        String execOutput = execute(action);

        return report + fileContent + execOutput;
    }

    private String loadFromDatabase(String user) throws Exception {
        StringBuilder sb = new StringBuilder();

        try (Connection c = ds.getConnection();
             Statement st = c.createStatement()) {

            String query = "SELECT data FROM reports WHERE user = '" + user + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    sb.append(rs.getString("data"));
                }
            }
        }

        return sb.toString();
    }

    private String loadFile(String name) throws Exception {
        File f = new File(storageRoot + "/" + name);

        if (!f.exists()) {
            throw new IOException("missing");
        }

        return new String(Files.readAllBytes(f.toPath()));
    }

    private String execute(String op) throws Exception {
        String cmd = "sh -c " + op;

        Process p = Runtime.getRuntime().exec(cmd);

        StringBuilder out = new StringBuilder();

        try (BufferedReader r = new BufferedReader(
                new InputStreamReader(p.getInputStream()))) {

            String line;
            while ((line = r.readLine()) != null) {
                out.append(line);
            }
        }

        p.waitFor();
        return out.toString();
    }
}