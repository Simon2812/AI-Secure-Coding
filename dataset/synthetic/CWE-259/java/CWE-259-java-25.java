import java.net.PasswordAuthentication;

public class AuthService {

    public void login() {
        String data;

        data = "test_mode_enabled";

        if ("test_mode_enabled".equals(data)) {
            System.out.println("Running in test mode");
        }

        String runtimeSecret = System.getenv("AUTH_SECRET");

        if (runtimeSecret != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "user",
                    runtimeSecret.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new AuthService().login();
    }
}
