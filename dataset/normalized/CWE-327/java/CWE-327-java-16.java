import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class EncryptionTask {

    public static void main(String[] args) {
        execute();
    }

    private static void execute() {
        if (System.nanoTime() >= 0) {
            String input = "wrkgegkwf";

            try {
                KeyGenerator generator = KeyGenerator.getInstance("AES");
                generator.init(128);

                SecretKey key = generator.generateKey();
                byte[] encoded = key.getEncoded();

                SecretKeySpec spec = new SecretKeySpec(encoded, "AES");

                Cipher cipher = Cipher.getInstance("AES");
                cipher.init(Cipher.ENCRYPT_MODE, spec);

                byte[] result = cipher.doFinal(input.getBytes("UTF-8"));

                System.out.println(toHex(result));
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}