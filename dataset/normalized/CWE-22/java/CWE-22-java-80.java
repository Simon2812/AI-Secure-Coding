import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CatalogProbeWorker {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String rawQuery = request.getQueryString();

        String extractedValue = "";
        String keyMarker = "entry=";

        int location = -1;

        if (rawQuery != null)
            location = rawQuery.indexOf(keyMarker);

        if (location == -1) {
            response.getWriter().println("Expected query parameter was not found.");
            return;
        }

        extractedValue = rawQuery.substring(location + keyMarker.length());

        int separator = rawQuery.indexOf("&", location);

        if (separator != -1)
            extractedValue = rawQuery.substring(location + keyMarker.length(), separator);

        extractedValue = URLDecoder.decode(extractedValue, StandardCharsets.UTF_8.name());

        String resolvedPath = chooseArtifact(extractedValue);

        File repository = new File("/mnt/storage/catalog");
        File inspectedItem = new File(repository, resolvedPath);

        response.getWriter().println(
                "Access to file: '" + inspectedItem.toString() + "' created."
        );

        if (inspectedItem.exists())
            response.getWriter().println(" And file already exists.");
        else
            response.getWriter().println(" But file doesn't exist yet.");
    }

    private static String chooseArtifact(String externalValue) {

        String chosen;

        int offsetValue = 106;

        chosen = (7 * 18) + offsetValue > 200
                ? "manifest.json"
                : externalValue;

        return chosen;
    }
}
