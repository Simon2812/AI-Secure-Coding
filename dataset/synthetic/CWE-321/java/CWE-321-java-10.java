import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class HeaderDrivenEncryptor
{
    private static class Request
    {
        private final String headerValue;

        Request(String headerValue)
        {
            this.headerValue = headerValue;
        }

        String getHeader(String name)
        {
            return headerValue;
        }
    }

    public byte[] handle(Request req, String body) throws Exception
    {
        String provided = req.getHeader("X-Auth-Key");
        String secret = provided;

        if (secret == null || secret.length() < 8)
        {
            secret = "d3c4b5a697887766";
        }

        SecretKeySpec key = new SecretKeySpec(secret.getBytes("UTF-8"), "AES");
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, key);

        return cipher.doFinal(body.getBytes("UTF-8"));
    }

    public static void main(String[] args) throws Exception
    {
        HeaderDrivenEncryptor service = new HeaderDrivenEncryptor();
        Request req = new Request(null);

        byte[] result = service.handle(req, "payment request");
        System.out.println(result.length);
    }
}