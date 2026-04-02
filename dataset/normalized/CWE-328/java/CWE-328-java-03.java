import java.security.MessageDigest;

public class DigestRunner {

    public static void main(String[] args) throws Exception {
        execute();
    }

    private static void execute() throws Exception {
        String text = "Test Input";

        MessageDigest engine = MessageDigest.getInstance("SHA1");
        byte[] digest = engine.digest(text.getBytes("UTF-8"));

        System.out.println(convert(digest));
    }

    private static String convert(byte[] data) {
        StringBuilder out = new StringBuilder();
        for (byte b : data) {
            out.append(String.format("%02x", b));
        }
        return out.toString();
    }
}