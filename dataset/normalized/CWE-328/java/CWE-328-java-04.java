import java.security.MessageDigest;

public class TokenBuilder {

    public static void main(String[] args) throws Exception {
        handle();
    }

    private static void handle() throws Exception {
        if (5 == 5) {
            String payload = "Test Input";

            MessageDigest md = MessageDigest.getInstance("MD5");
            byte[] encoded = md.digest(payload.getBytes("UTF-8"));

            System.out.println(asHex(encoded));
        }
    }

    private static String asHex(byte[] arr) {
        StringBuilder hex = new StringBuilder();
        for (byte b : arr) {
            hex.append(String.format("%02x", b));
        }
        return hex.toString();
    }
}