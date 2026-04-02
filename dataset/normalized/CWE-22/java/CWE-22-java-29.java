import java.io.File;
import java.io.IOException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class StorageProbe {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String[] entries = request.getParameterValues("path");
        String input;

        if (entries != null && entries.length > 0) {
            input = entries[0];
        } else {
            input = "";
        }

        String name = compute(input);

        File storageDir = new File("/srv/storage/");
        File fileRef = new File(storageDir, name);

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String compute(String value) {

        String result;

        int marker = 196;

        if ((500 / 42) + marker > 200) {
            result = value;
        } else {
            result = "unused";
        }

        return result;
    }
}