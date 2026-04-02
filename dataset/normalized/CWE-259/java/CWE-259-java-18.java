import java.net.PasswordAuthentication;

public class RemoteAccessConfig {

    public void setupCredentials() {
        String password = System.getenv("APP_PASSWORD");

        if (password != null) {
            PasswordAuthentication credentials = new PasswordAuthentication(
                    "user",
                    password.toCharArray()
            );

            System.out.println(credentials.toString());
        } else {
            System.err.println("Missing environment variable: APP_PASSWORD");
        }
    }

    public static void main(String[] args) {
        new RemoteAccessConfig().setupCredentials();
    }
}