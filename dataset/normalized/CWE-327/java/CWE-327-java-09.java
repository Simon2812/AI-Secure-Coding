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
import java.util.HashMap;

public class ProcessingEndpoint extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        response.setContentType("text/html;charset=UTF-8");

        String header = request.getHeader("X-Data");
        if (header == null) {
            header = "";
        }

        header = java.net.URLDecoder.decode(header, "UTF-8");

        String a = header;
        StringBuilder b = new StringBuilder(a);
        b.append(" Safe");
        b.replace(b.length() - 4, b.length(), "Data");

        HashMap<String, Object> map = new HashMap<>();
        map.put("k", b.toString());

        String c = (String) map.get("k");
        String d = c.substring(0, c.length() - 1);

        String e = new String(Base64.getDecoder().decode(Base64.getEncoder().encode(d.getBytes())));
        String f = e.split(" ")[0];

        String processed = f;

        SecureRandom random = new SecureRandom();
        byte[] iv = random.generateSeed(8);

        try {
            Cipher cipher = Cipher.getInstance("DES/CBC/PKCS5Padding");

            SecretKey key = KeyGenerator.getInstance("DES").generateKey();
            IvParameterSpec spec = new IvParameterSpec(iv);

            cipher.init(Cipher.ENCRYPT_MODE, key, spec);

            byte[] input = processed.getBytes("UTF-8");
            byte[] encrypted = cipher.doFinal(input);

            String encoded = Base64.getEncoder().encodeToString(encrypted);

            response.getWriter().println("Stored: " + encoded);

        } catch (Exception ex) {
            throw new ServletException(ex);
        }

        response.getWriter().println("Done");
    }
}