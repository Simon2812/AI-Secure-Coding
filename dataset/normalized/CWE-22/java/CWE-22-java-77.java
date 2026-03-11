import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DiskProbeAgent {

    public void run(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String clientValue = request.getParameter("item");
        if (clientValue == null) clientValue = "";

        String resolvedName = selectEntry(clientValue);

        File probe = new File(resolvedName);

        response.getWriter().println(
                "Access to file: '" + probe.toString() + "' created."
        );

        if (probe.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String selectEntry(String externalInput) {

        String candidate;

        int offset = 86;

        if ((7 * 42) - offset > 200)
            candidate = "report.log";
        else
            candidate = externalInput;

        return candidate;
    }
}