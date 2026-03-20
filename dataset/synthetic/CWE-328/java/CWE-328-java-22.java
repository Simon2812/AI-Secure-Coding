import java.security.MessageDigest;

public class LabelPrinter {

    public static void main(String[] args) throws Exception {
        String label1 = "MD5";
        String label2 = "SHA1";

        String data = "value";

        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] result = md.digest(data.getBytes());

        System.out.println(label1 + ":" + label2);
        System.out.println(result.length);
    }
}