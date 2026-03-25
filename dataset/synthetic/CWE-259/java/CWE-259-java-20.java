import java.net.PasswordAuthentication;

public class EnvAuth {

    public void execute() {
        String secretValue = System.getenv("DB_PASSWORD");

        if (secretValue != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "serviceUser",
                    secretValue.toCharArray()
            );

            System.out.println(auth.toString());
        } else {
            System.err.println("Missing environment variable: DB_PASSWORD");
        }
    }

    public static void main(String[] args) {
        new EnvAuth().execute();
    }
}