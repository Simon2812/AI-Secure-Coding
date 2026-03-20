import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.ServletException;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Properties;
import java.util.Base64;

public class RequestHandler extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        String selected = "";
        boolean found = true;

        Enumeration<String> params = request.getParameterNames();
        while (params.hasMoreElements() && found) {
            String key = params.nextElement();
            String[] values = request.getParameterValues(key);

            if (values != null) {
                for (String v : values) {
                    if ("targetValue".equals(v)) {
                        selected = key;
                        found = false;
                        break;
                    }
                }
            }
        }

        try {
            Properties props = new Properties();
            props.load(this.getClass().getClassLoader().getResourceAsStream("benchmark.properties"));

            String algo = props.getProperty("cryptoAlg1", "DESede/ECB/PKCS5Padding");

            Cipher cipher = Cipher.getInstance(algo);

            SecretKey key = KeyGenerator.getInstance("DES").generateKey();
            cipher.init(Cipher.ENCRYPT_MODE, key);

            byte[] input = selected.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(input);

            String encoded = Base64.getEncoder().encodeToString(encrypted);

            response.getWriter().println("Stored: " + encoded);

        } catch (Exception e) {
            throw new ServletException(e);
        }
    }
}