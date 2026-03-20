import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;

public class HeaderSafeHash extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String header = request.getHeader("input");
        String value = header != null ? java.net.URLDecoder.decode(header, "UTF-8") : "";

        int num = 86;
        String chosen;
        if ((7 * 42) - num > 200) {
            chosen = "constant";
        } else {
            chosen = value;
        }

        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");

            byte[] data = chosen.getBytes();
            md.update(data);

            byte[] result = md.digest();

            java.io.FileWriter writer = new java.io.FileWriter("passwordFile.txt", true);
            writer.write(java.util.Base64.getEncoder().encodeToString(result) + "\n");
            writer.close();

            response.getWriter().println("stored");

        } catch (Exception e) {
            throw new IOException(e);
        }
    }
}
