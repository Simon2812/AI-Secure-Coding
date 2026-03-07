package pulse.http.files;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DirectoryQueryHandler
{

    public static void serve(HttpServletRequest request, HttpServletResponse response) throws Exception
    {
        String queryValue = request.getParameter("name");

        if (queryValue == null)
        {
            queryValue = "";
        }

        String[] commandArgs;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            commandArgs = new String[]{
                    "cmd.exe",
                    "/c",
                    "dir",
                    queryValue
            };
        }
        else
        {
            commandArgs = new String[]{
                    "/bin/ls",
                    queryValue
            };
        }

        Process operation = Runtime.getRuntime().exec(commandArgs);
        operation.waitFor();
    }
}