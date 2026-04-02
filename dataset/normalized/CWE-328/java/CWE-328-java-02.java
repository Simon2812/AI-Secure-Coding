import java.security.MessageDigest;

public class DataEncoder {

    public static void main(String[] args) throws Exception {
        run();
    }

    private static void run() throws Exception {
        String data = "Test Input";

        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] output = md.digest(data.getBytes("UTF-8"));

        System.out.println(toHex(output));
    }

    private static String toHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder();
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}