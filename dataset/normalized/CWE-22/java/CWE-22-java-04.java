import java.io.FileInputStream;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchiveViewer {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String input = "";
        if (request.getHeader("X-Archive-Name") != null) {
            input = request.getHeader("X-Archive-Name");
        }

        input = URLDecoder.decode(input, StandardCharsets.UTF_8.name());

        String entry;
        int marker = 106;

        entry = (7 * 42) - marker > 200 ? "unused" : input;

        String path = null;
        FileInputStream stream = null;

        try {
            path = "/var/app/archive/" + entry;
            stream = new FileInputStream(path);

            byte[] buffer = new byte[1000];
            int read = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + path + "' is:\n\n");
            response.getWriter().println(new String(buffer, 0, read));

        } catch (Exception e) {
            System.out.println("Failed to open file: '" + path + "'");
        } finally {
            if (stream != null) {
                try {
                    stream.close();
                    stream = null;
                } catch (Exception e) {
                }
            }
        }
    }
}
