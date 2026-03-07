import java.io.IOException;

public class ScriptLauncher {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java ScriptLauncher <scriptName>");
            return;
        }

        String scriptName = args[0];

        String command = "sh " + scriptName;

        Process process = Runtime.getRuntime().exec(command);

        System.out.println("Launching script: " + scriptName);
    }
}