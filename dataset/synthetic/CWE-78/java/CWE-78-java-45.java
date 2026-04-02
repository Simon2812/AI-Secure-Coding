import java.io.IOException;

public class ContainerInspector {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java ContainerInspector <container>");
            return;
        }

        String containerId = args[0];

        String command = String.format("docker inspect %s", containerId);

        Process process = Runtime.getRuntime().exec(command);

        System.out.println("Inspecting container: " + containerId);
    }
}