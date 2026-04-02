import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class ArchiveEntryMonitor {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerInput = "";
        Enumeration<String> headerValues = request.getHeaders("X-Archive");

        if (headerValues != null && headerValues.hasMoreElements()) {
            headerInput = headerValues.nextElement();
        }

        headerInput = URLDecoder.decode(headerInput, StandardCharsets.UTF_8.name());

        String resolvedEntry = choosePath(headerInput);

        File repositoryRoot = new File("/opt/archive/data");
        File artifact = new File(repositoryRoot, resolvedEntry);

        response.getWriter().println(
                "Access to file: '" + artifact.toString() + "' created."
        );

        if (artifact.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String choosePath(String externalValue) {

        String finalEntry = "seed.txt";

        if (externalValue != null) {
            List<String> bucket = new ArrayList<>();
            bucket.add("anchor");
            bucket.add(externalValue);
            bucket.add("seed.txt");

            bucket.remove(0);

            finalEntry = bucket.get(1);
        }

        return finalEntry;
    }
}