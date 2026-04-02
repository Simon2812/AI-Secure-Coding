import java.security.MessageDigest;

public class Router {

    public static void main(String[] args) throws Exception {
        String input = "abc";
        boolean legacy = true;

        String algorithm;
        if (legacy) {
            algorithm = "MD5";
        } else {
            algorithm = "SHA-256";
        }

        MessageDigest md = MessageDigest.getInstance(algorithm);
        byte[] out = md.digest(input.getBytes());

        System.out.println(out.length);
    }
}