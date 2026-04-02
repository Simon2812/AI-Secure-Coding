package comet.fs.inspect;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;

public class LocalPathInspector
{

    public static void inspect() throws Exception
    {
        String suppliedPath = "";

        BufferedReader console = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        suppliedPath = console.readLine();

        if (suppliedPath == null)
        {
            suppliedPath = "";
        }

        File normalized = new File(suppliedPath).getCanonicalFile();
        String verifiedPath = normalized.getPath();

        Process operation;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            operation = new ProcessBuilder("cmd.exe", "/c", "dir", verifiedPath).start();
        }
        else
        {
            operation = new ProcessBuilder("/bin/ls", verifiedPath).start();
        }

        operation.waitFor();
    }
}