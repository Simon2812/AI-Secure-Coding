import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class DescriptorCatalog {

    private static final String repositoryRoot = "/data/descriptors";

    public String readDescriptor(String descriptorName) throws IOException {

        String path = repositoryRoot + "/" + descriptorName + ".desc";

        Scanner scanner = new Scanner(new File(path));
        return scanner.nextLine();
    }
}