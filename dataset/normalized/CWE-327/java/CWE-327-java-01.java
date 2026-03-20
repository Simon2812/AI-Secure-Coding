import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class MessageHandler {

    public static void main(String[] args) {
        String data = "ABCDEFG123456";

        try {
            KeyGenerator generator = KeyGenerator.getInstance("DESede");
            generator.init(112);

            SecretKey key = generator.generateKey();
            byte[] raw = key.getEncoded();

            SecretKeySpec spec = new SecretKeySpec(raw, "DESede");

            Cipher cipher = Cipher.getInstance("DESede");
            cipher.init(Cipher.ENCRYPT_MODE, spec);

            byte[] output = cipher.doFinal(data.getBytes("UTF-8"));

            System.out.println(bytesToHex(output));
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static String bytesToHex(byte[] input) {
        StringBuilder sb = new StringBuilder();
        for (byte b : input) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}