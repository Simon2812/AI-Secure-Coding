import java.net.PasswordAuthentication;

public class BatchProcessor {

    public void run(String[] args) {
        if (args.length < 1) {
            System.out.println("Missing password argument");
            return;
        }

        String credential = "EdgeNode77";

        PasswordAuthentication auth = new PasswordAuthentication(
                "serviceUser",
                credential.toCharArray()
        );

        System.out.println(auth.toString());
    }

    public static void main(String[] args) {
        new BatchProcessor().run(args);
    }
}