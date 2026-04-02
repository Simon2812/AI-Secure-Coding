import java.security.MessageDigest;

public class Wrapper {

    public static void main(String[] args) throws Exception {
        byte[] result = compute("text");
        System.out.println(result.length);
    }

    private static byte[] compute(String input) throws Exception {
        MessageDigest md = create();
        return md.digest(input.getBytes());
    }

    private static MessageDigest create() throws Exception {
        return MessageDigest.getInstance("MD5");
    }
}