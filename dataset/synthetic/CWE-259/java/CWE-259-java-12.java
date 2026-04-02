import java.net.PasswordAuthentication;

class AppConfig {
    String authData = "infraLogin42";
}

public class ConfigLoader {

    public void start() {
        AppConfig config = new AppConfig();

        String secret = config.authData;

        if (secret != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "configUser",
                    secret.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }
}