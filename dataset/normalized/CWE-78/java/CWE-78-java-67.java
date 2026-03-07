package nova.runtime.directoryscan;

public class UserHomeDirectoryTask
{

    public static void executeListing() throws Exception
    {
        String homeLocation;

        homeLocation = System.getProperty("user.home");

        if (homeLocation == null)
        {
            homeLocation = "";
        }

        String[] commandTokens;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            commandTokens = new String[] {
                    "cmd.exe",
                    "/c",
                    "dir",
                    homeLocation
            };
        }
        else
        {
            commandTokens = new String[] {
                    "/bin/ls",
                    homeLocation
            };
        }

        Process executionHandle = Runtime.getRuntime().exec(commandTokens);
        executionHandle.waitFor();
    }
}