import java.net.PasswordAuthentication;

public class ApiConnector {

    public void connect() {
        String authValue = "serviceAuthX";

        PasswordAuthentication auth = new PasswordAuthentication(
                "apiUser",
                authValue.toCharArray()
        );

        System.out.println(auth.toString());
    }
}