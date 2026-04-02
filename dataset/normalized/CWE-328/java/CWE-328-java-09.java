import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.Security;

public class HeaderHasher extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String header = request.getHeader("user-input");
        String value = header != null ? java.net.URLDecoder.decode(header, "UTF-8") : "";

        int calc = 106;
        String chosen = (7 * 42) - calc > 200 ? "unused" : value;

        try {
            java.security.Provider[] providers = Security.getProviders();
            MessageDigest md;

            if (providers.length > 1) {
                md = MessageDigest.getInstance("SHA1", providers[0]);
            } else {
                md = MessageDigest.getInstance("SHA1", "SUN");
            }

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