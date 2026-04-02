import java.security.MessageDigest;

public class HashExample {

    public static void main(String[] args) throws Exception {
        execute();
    }

    private static void execute() throws Exception {
        String value = "Test Input";

        MessageDigest md = MessageDigest.getInstance("SHA-512");
        byte[] result = md.digest(value.getBytes("UTF-8"));

        System.out.println(toHex(result));
    }

    private static String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}