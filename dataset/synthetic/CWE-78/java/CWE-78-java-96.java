import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class NodeInspector {

    public static void main(String[] args) throws IOException {

        BufferedReader reader = new BufferedReader(new FileReader("nodes.txt"));
        String node = reader.readLine();
        reader.close();

        if (node == null || !node.matches("[a-zA-Z0-9.-]+")) {
            throw new IllegalArgumentException("Invalid node");
        }

        ProcessBuilder pb = new ProcessBuilder("ssh", node, "hostname");
        Process process = pb.start();

        System.out.println("Node inspection started for " + node);
    }
}