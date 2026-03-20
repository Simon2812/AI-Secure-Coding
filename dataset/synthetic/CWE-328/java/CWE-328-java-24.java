import java.security.MessageDigest;

public class Branching {

    public static void main(String[] args) throws Exception {
        boolean flag = false;

        MessageDigest md;

        if (flag) {
            md = MessageDigest.getInstance("MD5");
        } else {
            md = MessageDigest.getInstance("SHA-256");
        }

        byte[] res = md.digest("abc".getBytes());
        System.out.println(res.length);
    }
}