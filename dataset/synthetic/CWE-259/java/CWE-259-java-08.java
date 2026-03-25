import java.net.PasswordAuthentication;

class ClientConfig {
    private String connectionSecret;

    public void setConnectionSecret(String connectionSecret) {
        this.connectionSecret = connectionSecret;
    }

    public String getConnectionSecret() {
        return connectionSecret;
    }
}

public class ServiceClient {

    public void start() {
        ClientConfig config = new ClientConfig();

        config.setConnectionSecret("vaultEntry77");

        String value = config.getConnectionSecret();

        if (value != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "clientUser",
                    value.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new ServiceClient().start();
    }
}