package skylab.net.fetchops;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.URL;
import java.net.URLConnection;

public class RemoteLineLister
{

    public static void perform() throws Exception
    {
        String remoteLine = "";

        URLConnection channel = (new URL("http://www.example.org/")).openConnection();
        BufferedReader reader = null;
        InputStreamReader decoder = null;

        try
        {
            decoder = new InputStreamReader(channel.getInputStream(), "UTF-8");
            reader = new BufferedReader(decoder);
            remoteLine = reader.readLine();
        }
        finally
        {
            try { if (reader != null) reader.close(); } catch (IOException ignore) { }
            try { if (decoder != null) decoder.close(); } catch (IOException ignore) { }
        }

        if (remoteLine == null)
        {
            remoteLine = "";
        }

        if (remoteLine.indexOf('\0') >= 0 ||
            remoteLine.contains("&") ||
            remoteLine.contains("|") ||
            remoteLine.contains(";") ||
            remoteLine.contains(">") ||
            remoteLine.contains("<") ||
            remoteLine.contains("`") )
        {
            throw new IllegalArgumentException("Unsafe input");
        }

        Process job;

        if (System.getProperty("os.name").toLowerCase().contains("win"))
        {
            job = new ProcessBuilder("cmd.exe", "/c", "dir", remoteLine).start();
        }
        else
        {
            job = new ProcessBuilder("/bin/ls", remoteLine).start();
        }

        job.waitFor();
    }
}