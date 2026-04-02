package platform.runtime;

import java.util.Properties;
import java.io.FileInputStream;
import java.io.IOException;

public class ListingLauncher {

    private String loadValue() {

        String value = "";
        Properties cfg = new Properties();
        FileInputStream input = null;

        try {
            input = new FileInputStream("../common/config.properties");
            cfg.load(input);
            value = cfg.getProperty("data");
        } catch (IOException e) {
            System.err.println("Configuration read error: " + e.getMessage());
        } finally {
            try {
                if (input != null) {
                    input.close();
                }
            } catch (IOException ignored) {}
        }

        return value;
    }

    public void run() throws Exception {

        String argument = loadValue();

        String command;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            command = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            command = "/bin/ls ";
        }

        Process task = Runtime.getRuntime().exec(command + argument);
        task.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new ListingLauncher().run();
    }
}