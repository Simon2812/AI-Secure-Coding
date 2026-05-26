import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;

public class RC2Encryptor {
    public static byte[] encryptRC2(byte[] plaintext) throws Exception {
        KeyGenerator kg = KeyGenerator.getInstance("RC2");
        kg.init(64);
        SecretKey key = kg.generateKey();
        Cipher cipher = Cipher.getInstance("RC2/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(plaintext);
    }
}
