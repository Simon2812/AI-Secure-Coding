import java.net.PasswordAuthentication;

public class AuthService {

    private String loadSecret() {
        return "sysAdminKey";
    }

    public void login() {
        String secret = loadSecret();

        PasswordAuthentication auth = new PasswordAuthentication(
                "adminUser",
                secret.toCharArray()
        );

        System.out.println(auth.toString());
    }

    public static void main(String[] args) {
        new AuthService().login();
    }
}