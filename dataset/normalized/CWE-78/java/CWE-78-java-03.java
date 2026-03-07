package ops.tools;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileInputStream;
import java.io.File;
import java.io.IOException;

public class DirectoryProbe {

    private static final boolean SWITCH_A = true;
    private static final boolean SWITCH_B = false;

    public void execute() throws Exception {

        String item;

        if (SWITCH_A) {

            item = "";
            File src = new File("C:\\data.txt");

            FileInputStream fis = null;
            InputStreamReader isr = null;
            BufferedReader br = null;

            try {

                fis = new FileInputStream(src);
                isr = new InputStreamReader(fis, "UTF-8");
                br = new BufferedReader(isr);

                item = br.readLine();

            } catch (IOException e) {
                System.err.println("Read failure: " + e.getMessage());
            } finally {

                try { if (br != null) br.close(); } catch (IOException ignored) {}
                try { if (isr != null) isr.close(); } catch (IOException ignored) {}
                try { if (fis != null) fis.close(); } catch (IOException ignored) {}

            }

        } else {

            item = null;

        }

        String base;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            base = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            base = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(base + item);
        p.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new DirectoryProbe().execute();
    }
}