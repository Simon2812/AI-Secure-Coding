import java.net.PasswordAuthentication;
import java.util.Properties;
import java.io.FileInputStream;
import java.io.IOException;

public class ApiConnector {

    public void connect() {
        String configSecret = null;

        Properties props = new Properties();
        try {
            FileInputStream fis = new FileInputStream("config.properties");
            props.load(fis);
            fis.close();

            configSecret = props.getProperty("password");
        } catch (IOException e) {
            System.err.println("Config load error: " + e.getMessage());
        }

        if (configSecret != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "configUser",
                    configSecret.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }
}