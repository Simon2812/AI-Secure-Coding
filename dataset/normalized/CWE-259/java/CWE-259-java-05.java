import java.net.PasswordAuthentication;

public class RemoteAccessConfig {

    public void setupCredentials() {
        String userPasscode;

        if (System.nanoTime() >= 0) {
            userPasscode = "backupEntry88";
        } else {
            userPasscode = null;
        }

        if (userPasscode != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "serviceUser",
                    userPasscode.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new RemoteAccessConfig().setupCredentials();
    }
}