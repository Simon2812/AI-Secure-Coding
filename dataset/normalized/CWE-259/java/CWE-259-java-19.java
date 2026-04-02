import java.net.PasswordAuthentication;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class ServiceConnector {

    public void connect() {
        String password = null;

        try {
            BufferedReader reader = new BufferedReader(new FileReader("password.txt"));
            password = reader.readLine();
            reader.close();
        } catch (IOException e) {
            System.err.println("File error: " + e.getMessage());
        }

        if (password != null) {
            PasswordAuthentication credentials = new PasswordAuthentication(
                    "user",
                    password.toCharArray()
            );

            System.out.println(credentials.toString());
        }
    }

}
