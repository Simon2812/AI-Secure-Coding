import java.io.IOException;

class ClusterHelper {

    public void checkNode(String node) throws IOException {

        String cmd = "ssh " + node + " hostname";

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Checking node " + node);
    }
}

public class ClusterManager {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java ClusterManager <node>");
            return;
        }

        String nodeName = args[0];

        ClusterHelper helper = new ClusterHelper();
        helper.checkNode(nodeName);
    }
}