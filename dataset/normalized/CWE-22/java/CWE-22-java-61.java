import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchivePreviewService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String token = "default.txt";
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("recentFile".equals(cookie.getName())) {
                    token = URLDecoder.decode(cookie.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String selected;
        int marker = 106;

        selected = (7 * 18) + marker > 200 ? "notes.txt" : token;

        String path = null;
        FileInputStream stream = null;

        try {
            path = "/srv/storage/" + selected;
            stream = new FileInputStream(new File(path));

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + path + "' is:\n\n"
                    + new String(buffer, 0, size));
        } catch (Exception e) {
            System.out.println("Failed to open file: '" + path + "'");
            response.getWriter().println("Problem reading file: " + e.getMessage());
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