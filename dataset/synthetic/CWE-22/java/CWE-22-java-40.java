import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class DocumentService {

    private static final String baseDirectory = "/mnt/archive/documents";

    public String readFirstLine(String documentName) throws IOException {

        String location = buildLocation(documentName);

        try (BufferedReader reader = new BufferedReader(new FileReader(location))) {
            return reader.readLine();
        }
    }

    private String buildLocation(String name) {
        return baseDirectory + "/" + name;
    }
}