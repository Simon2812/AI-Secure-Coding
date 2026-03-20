import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class CryptoFlow {

    private static final boolean ENABLE = true;

    public static void main(String[] args) {
        execute();
    }

    private static void execute() {
        if (ENABLE) {
            String text = "ABCDEFG123456";

            try {
                KeyGenerator gen = KeyGenerator.getInstance("DES");
                gen.init(56);

                SecretKey key = gen.generateKey();
                byte[] data = key.getEncoded();

                SecretKeySpec spec = new SecretKeySpec(data, "DES");

                Cipher cipher = Cipher.getInstance("DES");
                cipher.init(Cipher.ENCRYPT_MODE, spec);

                byte[] result = cipher.doFinal(text.getBytes("UTF-8"));

                System.out.println(format(result));
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static String format(byte[] input) {
        StringBuilder sb = new StringBuilder();
        for (byte b : input) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}