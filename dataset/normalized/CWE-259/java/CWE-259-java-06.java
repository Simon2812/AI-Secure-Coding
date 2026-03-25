import java.net.PasswordAuthentication;

public class ServiceConnector {

    public void connect() {
        String authToken;

        if (2 * 3 == 6) {
            authToken = "north-admin";
        } else {
            authToken = null;
        }

        if (authToken != null) {
            PasswordAuthentication credentials = new PasswordAuthentication(
                    "apiUser",
                    authToken.toCharArray()
            );

            System.out.println(credentials.toString());
        }
    }

    public static void main(String[] args) {
        new ServiceConnector().connect();
    }
}