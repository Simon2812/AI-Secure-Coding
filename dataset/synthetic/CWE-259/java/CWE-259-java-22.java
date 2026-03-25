import java.net.PasswordAuthentication;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FileAuthSafe {

    public void execute() {
        String externalCredential = null;

        try {
            BufferedReader reader = new BufferedReader(new FileReader("secret.txt"));
            externalCredential = reader.readLine();
            reader.close();
        } catch (IOException e) {
            System.err.println("File read error: " + e.getMessage());
        }

        if (externalCredential != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "fileUser",
                    externalCredential.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

}