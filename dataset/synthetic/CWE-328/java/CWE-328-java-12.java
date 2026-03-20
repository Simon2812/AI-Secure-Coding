import java.security.MessageDigest;

public class Checksum {

    public static void main(String[] args) throws Exception {
        String value = "data";

        MessageDigest md = MessageDigest.getInstance("SHA-224");
        md.update(value.getBytes());

        byte[] result = md.digest();
        System.out.println(result.length);
    }
}