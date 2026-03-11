import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class ExportWriter {

    private static final Path exportBase = Path.of("/data/storage/exports");

    public void writeExport(String label, String data) throws IOException {

        Path target = exportBase.resolve(label + ".txt");

        Files.writeString(target, data);
    }
}