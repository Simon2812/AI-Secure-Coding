import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DocumentPreviewServlet {

    public void handle(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        response.setContentType("text/html;charset=UTF-8");

        Cookie[] cookies = request.getCookies();

        String selectedName = "default.txt";
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("recentDocument".equals(cookie.getName())) {
                    selectedName = URLDecoder.decode(cookie.getValue(), StandardCharsets.UTF_8.name());
                    break;
                }
            }
        }

        String fullPath = null;
        FileInputStream input = null;

        try {
            fullPath = "/var/app/docs/" + selectedName;
            input = new FileInputStream(new File(fullPath));

            byte[] buffer = new byte[1000];
            int length = input.read(buffer);

            response.getWriter().println(
                    "Preview of file: '" + fullPath + "'\n\n" + new String(buffer, 0, length));
        } catch (Exception e) {
            System.out.println("Failed to open file: '" + fullPath + "'");
            response.getWriter().println("Unable to read file: " + e.getMessage());
        } finally {
            if (input != null) {
                try {
                    input.close();
                    input = null;
                } catch (Exception e) {
                }
            }
        }
    }
}