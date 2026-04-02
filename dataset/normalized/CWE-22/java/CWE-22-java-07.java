import java.io.File;
import java.io.IOException;
import java.util.Map;
import java.util.Base64;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class EntryReader {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        Map<String,String[]> params = request.getParameterMap();
        String input = "";
        if (!params.isEmpty()) {
            String[] values = params.get("entry");
            if (values != null) {
                input = values[0];
            }
        }

        String name = "";
        if (input != null) {
            name = new String(
                    Base64.getDecoder().decode(
                            Base64.getEncoder().encode(input.getBytes())
                    )
            );
        }

        File baseDir = new File("/opt/service/files/");
        File target = new File(baseDir, name);

        response.getWriter().println("Access to file: '" + target.toString() + "' created.");

        if (target.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }
}