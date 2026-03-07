import java.io.IOException;

class DiagnosticService {

    public void probeNode(String node) throws IOException {

        String cmd = "ping -c 2 " + node;

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Probing node " + node);
    }
}

public class ClusterDiagnostics {

    public static void main(String[] args) throws IOException {

        String nodeName = System.getenv("CLUSTER_NODE");

        if (nodeName == null) {
            System.out.println("Environment variable CLUSTER_NODE not set");
            return;
        }

        DiagnosticService service = new DiagnosticService();
        service.probeNode(nodeName);
    }
}