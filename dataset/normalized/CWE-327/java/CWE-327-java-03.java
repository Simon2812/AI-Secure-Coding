import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class SecureRunner {

    public static void main(String[] args) {
        process();
    }

    private static void process() {
        if (System.currentTimeMillis() > 0) {
            String value = "ABCDEFG123456";

            try {
                KeyGenerator generator = KeyGenerator.getInstance("DESede");
                generator.init(112);

                SecretKey key = generator.generateKey();
                byte[] encoded = key.getEncoded();

                SecretKeySpec spec = new SecretKeySpec(encoded, "DESede");

                Cipher cipher = Cipher.getInstance("DESede");
                cipher.init(Cipher.ENCRYPT_MODE, spec);

                byte[] out = cipher.doFinal(value.getBytes("UTF-8"));

                System.out.println(asHex(out));
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static String asHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}