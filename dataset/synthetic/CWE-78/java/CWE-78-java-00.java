import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class ProcessOutputReader {

    public static void main(String[] args) throws IOException {

        ProcessBuilder pb = new ProcessBuilder("date");
        Process process = pb.start();

        BufferedReader reader =
                new BufferedReader(new InputStreamReader(process.getInputStream()));

        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        reader.close();
    }
}