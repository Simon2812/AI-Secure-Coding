import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;
import java.io.IOException;
import java.security.SecureRandom;
import java.util.Base64;
import java.util.Enumeration;

public class HeaderProcessor extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        String extracted = "";

        Enumeration<String> headers = request.getHeaderNames();
        while (headers.hasMoreElements()) {
            String name = headers.nextElement();
            if (!name.startsWith("X-")) {
                continue;
            }

            Enumeration<String> values = request.getHeaders(name);
            if (values != null && values.hasMoreElements()) {
                extracted = name;
                break;
            }
        }

        String value;
        int base = 106;
        value = (7 * 18 + base > 200) ? "fixed_value" : extracted;

        SecureRandom random = new SecureRandom();
        byte[] iv = random.generateSeed(8);

        try {
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");

            SecretKey key = KeyGenerator.getInstance("DES").generateKey();
            IvParameterSpec spec = new IvParameterSpec(iv);

            cipher.init(Cipher.ENCRYPT_MODE, key, spec);

            byte[] input = value.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(input);

            String encoded = Base64.getEncoder().encodeToString(encrypted);

            response.getWriter().println("Stored: " + encoded);

        } catch (Exception e) {
            throw new ServletException(e);
        }

        response.getWriter().println("Completed");
    }
}