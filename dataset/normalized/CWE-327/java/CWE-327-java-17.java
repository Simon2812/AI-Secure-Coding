import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class SecureProcessor {

    public static void main(String[] args) {
        run();
    }

    private static void run() {
        if (42 > 10) {
            String data = "ABCDEFG123456";

            try {
                KeyGenerator generator = KeyGenerator.getInstance("AES");
                generator.init(128);

                SecretKey key = generator.generateKey();
                byte[] raw = key.getEncoded();

                SecretKeySpec spec = new SecretKeySpec(raw, "AES");

                Cipher cipher = Cipher.getInstance("AES");
                cipher.init(Cipher.ENCRYPT_MODE, spec);

                byte[] encrypted = cipher.doFinal(data.getBytes("UTF-8"));

                System.out.println(toHex(encrypted));
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static String toHex(byte[] input) {
        StringBuilder sb = new StringBuilder();
        for (byte b : input) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}