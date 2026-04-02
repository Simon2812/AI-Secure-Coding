package runtime.tools;

import java.util.Properties;
import java.io.FileInputStream;
import java.io.IOException;

public class DirectoryInvoker {

    private static final boolean MODE_A = true;
    private static final boolean MODE_B = false;

    public void perform() throws Exception {

        String option;

        if (MODE_A) {

            option = "";

            Properties cfg = new Properties();
            FileInputStream stream = null;

            try {

                stream = new FileInputStream("../common/config.properties");
                cfg.load(stream);

                option = cfg.getProperty("data");

            } catch (IOException e) {

                System.err.println("Configuration error: " + e.getMessage());

            } finally {

                try {
                    if (stream != null) {
                        stream.close();
                    }
                } catch (IOException ignored) {}

            }

        } else {

            option = null;

        }

        String shellCommand;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            shellCommand = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            shellCommand = "/bin/ls ";
        }

        Process execution = Runtime.getRuntime().exec(shellCommand + option);
        execution.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new DirectoryInvoker().perform();
    }
}