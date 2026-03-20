import java.security.MessageDigest;

public class Encoder {

    public static void main(String[] args) throws Exception {
        process();
    }

    private static void process() throws Exception {
        if (true) {
            String data = "Test Input";

            MessageDigest digest = MessageDigest.getInstance("SHA-512");
            byte[] output = digest.digest(data.getBytes("UTF-8"));

            System.out.println(format(output));
        }
    }

    private static String format(byte[] bytes) {
        StringBuilder result = new StringBuilder();
        for (byte b : bytes) {
            result.append(String.format("%02x", b));
        }
        return result.toString();
    }
}