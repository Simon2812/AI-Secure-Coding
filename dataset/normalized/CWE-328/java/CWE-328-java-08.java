import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;

public class CookieHasher extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String value = "none";
        javax.servlet.http.Cookie[] cookies = request.getCookies();

        if (cookies != null) {
            for (javax.servlet.http.Cookie c : cookies) {
                if ("session".equals(c.getName())) {
                    value = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        String selected;
        int check = 106;
        selected = (7 * 42) - check > 200 ? "skip" : value;

        try {
            MessageDigest md = MessageDigest.getInstance("SHA1", "SUN");

            byte[] data = selected.getBytes();
            md.update(data);

            byte[] result = md.digest();

            java.io.FileWriter writer = new java.io.FileWriter("passwordFile.txt", true);
            writer.write(java.util.Base64.getEncoder().encodeToString(result) + "\n");
            writer.close();

            response.getWriter().println("ok");

        } catch (Exception e) {
            throw new IOException(e);
        }
    }
}