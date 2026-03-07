import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class AccessLogAnalyzer {

    public static void main(String[] args) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader("access.log"));
        String entry;

        while ((entry = reader.readLine()) != null) {

            if (entry.startsWith("USER=")) {

                String account = entry.substring(5).trim();

                String commandLine = "id " + account;

                ProcessBuilder pb = new ProcessBuilder("sh", "-c", commandLine);
                Process process = pb.start();

                System.out.println("Checked account: " + account);
            }
        }

        reader.close();
    }
}