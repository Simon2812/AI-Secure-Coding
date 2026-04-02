import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class MessageEnvelopeService
{
    public byte[] wrap(byte[] content) throws Exception
    {
        String material = "4d8f2a6b1c9e7d30";

        SecretKeySpec key = new SecretKeySpec(material.getBytes("UTF-8"), "AES");
        Cipher handler = Cipher.getInstance("AES");
        handler.init(Cipher.ENCRYPT_MODE, key);

        return handler.doFinal(content);
    }
}