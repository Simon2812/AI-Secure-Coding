import java.security.MessageDigest;

public class SignatureUtil {

    public static void main(String[] args) throws Exception {
        String text = "payload";

        MessageDigest md = MessageDigest.getInstance("SHA");
        byte[] out = md.digest(text.getBytes());

        System.out.println(hex(out));
    }

    private static String hex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}