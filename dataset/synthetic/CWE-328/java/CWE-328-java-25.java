import java.security.MessageDigest;

public class WrapperSafe {

    public static void main(String[] args) throws Exception {
        byte[] result = compute("data");
        System.out.println(result.length);
    }

    private static byte[] compute(String input) throws Exception {
        MessageDigest md = createDigest("MD5");
        return md.digest(input.getBytes());
    }

    private static MessageDigest createDigest(String ignored) throws Exception {
        return MessageDigest.getInstance("SHA-256");
    }
}
