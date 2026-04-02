import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class LedgerArchive {

    private static final String ROOT = "/srv/ledgers";

    public String openLedger(String ledgerId) throws IOException {

        Path ledgerPath = Path.of(ROOT + "/" + ledgerId + "/index.txt");

        BufferedReader reader = Files.newBufferedReader(ledgerPath);
        return reader.readLine();
    }
}