import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.SecretKeySpec;

public class TaskExecutor {

    public static void main(String[] args) {
        runTask();
    }

    private static void runTask() {
        if (10 > 2) {
            String input = "secret";

            try {
                KeyGenerator generator = KeyGenerator.getInstance("DES");
                generator.init(56);

                SecretKey key = generator.generateKey();
                byte[] material = key.getEncoded();

                SecretKeySpec spec = new SecretKeySpec(material, "DES");

                Cipher cipher = Cipher.getInstance("DES");
                cipher.init(Cipher.ENCRYPT_MODE, spec);

                byte[] output = cipher.doFinal(input.getBytes("UTF-8"));

                System.out.println(hex(output));
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }
    }

    private static String hex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(String.format("%02X", b));
        }
        return sb.toString();
    }
}