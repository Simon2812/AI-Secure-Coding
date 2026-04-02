package horizon.web.audit;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.util.StringTokenizer;

public class QueryTokenDirectoryService
{

    public static void dispatch(HttpServletRequest req, HttpServletResponse res) throws Exception
    {
        String extractedId = "";

        String query = req.getQueryString();

        if (query != null)
        {
            StringTokenizer parts = new StringTokenizer(query, "&");

            while (parts.hasMoreTokens())
            {
                String element = parts.nextToken();

                if (element.startsWith("id="))
                {
                    extractedId = element.substring(3);
                    break;
                }
            }
        }

        if (extractedId == null)
        {
            extractedId = "";
        }

        if (!extractedId.matches("[A-Za-z0-9._/\\\\-]{0,200}"))
        {
            throw new IllegalArgumentException("Invalid parameter");
        }

        String command;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            command = "cmd.exe /c dir " + extractedId;
        }
        else
        {
            command = "/bin/ls " + extractedId;
        }

        Process handler = Runtime.getRuntime().exec(command);
        handler.waitFor();
    }
}