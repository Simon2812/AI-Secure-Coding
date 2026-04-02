import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

public class PolicyLoader {

    private static final Path ROOT = Path.of("/mnt/archive/policies");

    public List<String> readPolicy(String policyName) throws IOException {

        if (!policyName.matches("[A-Za-z0-9_-]+")) {
            throw new IOException("Invalid policy name");
        }

        Path policyFile = ROOT.resolve(policyName + ".policy");

        if (Files.notExists(policyFile)) {
            throw new IOException("Policy not found: " + policyName);
        }

        return Files.readAllLines(policyFile);
    }
}