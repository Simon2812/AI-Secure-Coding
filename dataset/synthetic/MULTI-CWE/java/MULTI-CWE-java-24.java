import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import javax.sql.DataSource;
import java.security.MessageDigest;
import java.util.Base64;

public class ExportPipeline {

    private final DataSource source;
    private final String exportRoot;

    public ExportPipeline(DataSource source, String exportRoot) {
        this.source = source;
        this.exportRoot = exportRoot;
    }

    public String export(String category, String fileName) throws Exception {
        String data = collect(category);
        String file = writeFile(fileName, data);
        return file;
    }

    private String collect(String category) throws Exception {
        StringBuilder result = new StringBuilder();

        try (Connection c = source.getConnection();
             Statement st = c.createStatement()) {

            String query = "SELECT content FROM export_data WHERE category = '" + category + "'";

            try (ResultSet rs = st.executeQuery(query)) {
                while (rs.next()) {
                    result.append(rs.getString("content")).append("\n");
                }
            }
        }

        return result.toString();
    }

    private String writeFile(String name, String content) throws Exception {
        File f = new File(exportRoot + "/" + name);

        if (!f.exists()) {
            f.createNewFile();
        }

        Files.write(f.toPath(), content.getBytes());

        return f.getAbsolutePath();
    }

    public String hash(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("MD5");
        byte[] h = d.digest(input.getBytes());
        return Base64.getEncoder().encodeToString(h);
    }

    public String label(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-256");
        byte[] h = d.digest(input.getBytes());
        return Base64.getEncoder().encodeToString(h);
    }
}