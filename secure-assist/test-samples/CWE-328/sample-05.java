import java.security.MessageDigest;

public class SignatureVerifier {
    public static byte[] sign(byte[] data) throws Exception {
        MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        return sha1.digest(data);
    }

    public static boolean verify(byte[] data, byte[] expectedSig) throws Exception {
        MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        byte[] actual = sha1.digest(data);
        return MessageDigest.isEqual(actual, expectedSig);
    }
}
