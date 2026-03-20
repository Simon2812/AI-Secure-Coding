import java.security.MessageDigest;

public class ValueHasher {

    public static void main(String[] args) throws Exception {
        perform();
    }

    private static void perform() throws Exception {
        if (true) {
            String content = "Test Input";

            MessageDigest processor = MessageDigest.getInstance("SHA1");
            byte[] result = processor.digest(content.getBytes("UTF-8"));

            System.out.println(toHex(result));
        }
    }

    private static String toHex(byte[] bytes) {
        StringBuilder buffer = new StringBuilder();
        for (byte b : bytes) {
            buffer.append(String.format("%02x", b));
        }
        return buffer.toString();
    }
}