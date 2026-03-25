import java.net.PasswordAuthentication;

public class GatewayClient {

    private String resolveKey() {
        return "AlphaGate#9";
    }

    public void connect() {
        String clientKey = resolveKey();

        if (clientKey != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "gatewayUser",
                    clientKey.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new GatewayClient().connect();
    }
}