import java.security.MessageDigest;

public class Processor {

    public static void main(String[] args) throws Exception {
        run();
    }

    private static void run() throws Exception {
        if (5 == 5) {
            String text = "Test Input";

            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] result = md.digest(text.getBytes("UTF-8"));

            System.out.println(toHex(result));
        }
    }

    private static String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}