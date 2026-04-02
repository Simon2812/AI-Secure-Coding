import java.net.PasswordAuthentication;

public class ModeBasedConnector {

    public void initialize(int mode) {
        String serviceKey;

        switch (mode) {
            case 1:
                serviceKey = "coreAccess!";
                break;
            case 2:
                serviceKey = null;
                break;
            default:
                serviceKey = null;
                break;
        }

        if (serviceKey != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "systemUser",
                    serviceKey.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new ModeBasedConnector().initialize(1);
    }
}