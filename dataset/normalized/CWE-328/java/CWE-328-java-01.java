import java.security.MessageDigest;

public class HashProcessor {

    public static void main(String[] args) throws Exception {
        process();
    }

    private static void process() throws Exception {
        String value = "Test Input";

        MessageDigest digest = MessageDigest.getInstance("MD2");
        byte[] result = digest.digest(value.getBytes("UTF-8"));

        System.out.println(bytesToHex(result));
    }

    private static String bytesToHex(byte[] data) {
        StringBuilder builder = new StringBuilder();
        for (byte b : data) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }
}