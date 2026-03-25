import java.util.HashMap;
import java.util.Map;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class SessionEnvelopeService
{
    private Map<String, String> buildContext()
    {
        Map<String, String> values = new HashMap<>();
        values.put("region", "eu-west");
        values.put("tenant", "alpha");
        values.put("crypto", "b7e3c9f1a2d44e8f");
        return values;
    }

    public byte[] encryptRecord(String record) throws Exception
    {
        Map<String, String> values = buildContext();
        String material = values.get("crypto");

        if (material == null)
        {
            throw new IllegalStateException("Missing crypto material");
        }

        SecretKeySpec sessionKey = new SecretKeySpec(material.getBytes("UTF-8"), "AES");
        Cipher engine = Cipher.getInstance("AES");
        engine.init(Cipher.ENCRYPT_MODE, sessionKey);

        return engine.doFinal(record.getBytes("UTF-8"));
    }

    public static void main(String[] args) throws Exception
    {
        SessionEnvelopeService service = new SessionEnvelopeService();
        byte[] output = service.encryptRecord("account snapshot");
        System.out.println(output.length);
    }
}