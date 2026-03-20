import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.security.MessageDigest;
import java.util.Properties;

public class HashEndpoint extends HttpServlet {

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws IOException {

        String value = "default";
        javax.servlet.http.Cookie[] cookies = req.getCookies();

        if (cookies != null) {
            for (javax.servlet.http.Cookie c : cookies) {
                if ("userToken".equals(c.getName())) {
                    value = java.net.URLDecoder.decode(c.getValue(), "UTF-8");
                    break;
                }
            }
        }

        try {
            Properties props = new Properties();
            props.load(this.getClass().getClassLoader().getResourceAsStream("benchmark.properties"));

            String algo = props.getProperty("hashAlg1", "SHA512");
            MessageDigest digest = MessageDigest.getInstance(algo);

            byte[] data = value.getBytes();
            digest.update(data);

            byte[] out = digest.digest();

            java.io.File target = new java.io.File("passwordFile.txt");
            java.io.FileWriter writer = new java.io.FileWriter(target, true);
            writer.write(java.util.Base64.getEncoder().encodeToString(out) + "\n");
            writer.close();

            resp.getWriter().println("done");

        } catch (Exception e) {
            throw new IOException(e);
        }
    }
}