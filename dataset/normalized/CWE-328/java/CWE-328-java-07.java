import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;

public class DigestService extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String[] inputs = request.getParameterValues("input");
        String data = (inputs != null && inputs.length > 0) ? inputs[0] : "";

        try {
            MessageDigest md = MessageDigest.getInstance("MD5");

            byte[] bytes = data.getBytes();
            md.update(bytes);

            byte[] result = md.digest();

            java.io.File file = new java.io.File("passwordFile.txt");
            java.io.FileWriter writer = new java.io.FileWriter(file, true);
            writer.write(java.util.Base64.getEncoder().encodeToString(result) + "\n");
            writer.close();

            response.getWriter().println("stored");

        } catch (Exception e) {
            throw new IOException(e);
        }
    }
}