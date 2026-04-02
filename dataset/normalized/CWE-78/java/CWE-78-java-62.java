package stellar.guard.exec;

public class EnvironmentListProbe
{

    public static void execute() throws Exception
    {
        String envToken;

        envToken = System.getenv("ADD");

        if (envToken == null)
        {
            envToken = "";
        }

        Process jobHandle;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            jobHandle = new ProcessBuilder(
                    "cmd.exe",
                    "/c",
                    "dir",
                    envToken
            ).start();
        }
        else
        {
            jobHandle = new ProcessBuilder(
                    "/bin/ls",
                    envToken
            ).start();
        }

        jobHandle.waitFor();
    }
}