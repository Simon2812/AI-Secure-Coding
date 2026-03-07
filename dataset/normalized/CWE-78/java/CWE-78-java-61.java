package atlas.execution.safe;

public class EnvironmentDrivenList
{

    public static void perform() throws Exception
    {
        String runtimeToken = System.getenv("ADD");

        if (runtimeToken == null)
        {
            runtimeToken = "";
        }

        Process executor;

        if (System.getProperty("os.name").toLowerCase().indexOf("win") >= 0)
        {
            executor = new ProcessBuilder("cmd.exe", "/c", "dir", runtimeToken).start();
        }
        else
        {
            executor = new ProcessBuilder("/bin/ls", runtimeToken).start();
        }

        executor.waitFor();
    }
}