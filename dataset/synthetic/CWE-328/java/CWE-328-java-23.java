import java.security.MessageDigest;

public class Selector {

    public static void main(String[] args) throws Exception {
        String option = args.length > 0 ? args[0] : "A";

        String algorithm;
        if ("A".equals(option)) {
            algorithm = "SHA-256";
        } else {
            algorithm = "SHA-512";
        }

        MessageDigest md = MessageDigest.getInstance(algorithm);
        byte[] out = md.digest("input".getBytes());

        System.out.println(out.length);
    }
}