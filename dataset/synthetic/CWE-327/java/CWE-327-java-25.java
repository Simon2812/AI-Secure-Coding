import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

public class ConditionalCrypto {

    public static void main(String[] args) {
        run(false);
    }

    private static void run(boolean useLegacy) {
        try {
            if (useLegacy) {
                Cipher c = Cipher.getInstance("DES");
                KeyGenerator g = KeyGenerator.getInstance("DES");
                SecretKey k = g.generateKey();
                c.init(Cipher.ENCRYPT_MODE, k);
                c.doFinal("test".getBytes());
            } else {
                Cipher c = Cipher.getInstance("AES");
                KeyGenerator g = KeyGenerator.getInstance("AES");
                SecretKey k = g.generateKey();
                c.init(Cipher.ENCRYPT_MODE, k);
                c.doFinal("test".getBytes());
            }

            System.out.println("Completed safely");

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
