import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class EncryptionService {

    public static void main(String[] args) {
        String payload = "ndgdkglfd";

        try {
            KeyGenerator generator = KeyGenerator.getInstance("DES");
            generator.init(56);

            SecretKey key = generator.generateKey();
            byte[] encoded = key.getEncoded();

            SecretKeySpec keySpec = new SecretKeySpec(encoded, "DES");

            Cipher cipher = Cipher.getInstance("DES");
            cipher.init(Cipher.ENCRYPT_MODE, keySpec);

            byte[] result = cipher.doFinal(payload.getBytes("UTF-8"));

            System.out.println(toHex(result));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static String toHex(byte[] data) {
        StringBuilder builder = new StringBuilder();
        for (byte b : data) {
            builder.append(String.format("%02X", b));
        }
        return builder.toString();
    }
}