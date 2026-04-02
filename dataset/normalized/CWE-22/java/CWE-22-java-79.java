import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArtifactLocator {

    public void inspect(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String clientToken = request.getParameter("entry");
        if (clientToken == null) clientToken = "";

        String resolvedSegment = selectSegment(clientToken);

        String prefix = "";
        String os = System.getProperty("os.name");

        if (os != null && os.contains("Windows"))
            prefix = "/";
        else
            prefix = "//";

        try {

            URI artifactUri = new URI(
                    "file",
                    null,
                    prefix + "/var/archive/".replace('\\', File.separatorChar).replace(' ', '_') + resolvedSegment,
                    null,
                    null
            );

            File artifactFile = new File(artifactUri);

            response.getWriter().println(
                    "Access to file: '" + artifactFile.toString() + "' created."
            );

            if (artifactFile.exists())
                response.getWriter().println(" And file already exists.");
            else
                response.getWriter().println(" But file doesn't exist yet.");

        } catch (Exception e) {
            throw new IOException(e);
        }
    }

    private static String selectSegment(String externalValue) {

        String chosen = "seed.bin";

        if (externalValue != null) {

            List<String> holder = new ArrayList<>();
            holder.add("anchor");
            holder.add(externalValue);
            holder.add("seed.bin");

            holder.remove(0);

            chosen = holder.get(1);
        }

        return chosen;
    }
}