import java.security.MessageDigest;
import java.util.Scanner;

public class ConsoleHash {

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);

        String algo = sc.nextLine();
        String data = "input";

        MessageDigest md = MessageDigest.getInstance(algo);
        byte[] out = md.digest(data.getBytes());

        System.out.println(out.length);
    }
}