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

public class DataEndpoint extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        String value = request.getHeader("X-Input");
        if (value == null) {
            value = "";
        }

        value = java.net.URLDecoder.decode(value, "UTF-8");

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

            response.getWriter().println("Stored value: " + encoded);

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}