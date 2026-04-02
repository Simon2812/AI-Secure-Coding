import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;
import java.security.Security;
import java.util.Enumeration;

public class HeaderDigestSafe extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String value = "";
        Enumeration<String> headers = request.getHeaderNames();

        while (headers.hasMoreElements()) {
            String name = headers.nextElement();
            Enumeration<String> vals = request.getHeaders(name);

            if (vals != null && vals.hasMoreElements()) {
                value = name;
                break;
            }
        }

        try {
            java.security.Provider[] providers = Security.getProviders();
            MessageDigest md;

            if (providers.length > 1) {
                md = MessageDigest.getInstance("SHA-512", providers[0]);
            } else {
                md = MessageDigest.getInstance("SHA-512", "SUN");
            }

            byte[] data = value.getBytes();
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