import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class FilePreview {

    public void execute(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String query = request.getQueryString();
        String key = "doc=";
        int pos = -1;

        if (query != null) {
            pos = query.indexOf(key);
        }

        if (pos == -1) {
            response.getWriter().println("Parameter not found.");
            return;
        }

        String input = query.substring(pos + key.length());

        int amp = query.indexOf("&", pos);
        if (amp != -1) {
            input = query.substring(pos + key.length(), amp);
        }

        input = URLDecoder.decode(input, StandardCharsets.UTF_8.name());

        String value = "placeholder";

        HashMap<String,Object> store = new HashMap<>();
        store.put("a", "value");
        store.put("b", input);
        store.put("c", "data");

        value = (String) store.get("b");

        String path = null;
        FileInputStream stream = null;

        try {

            path = "/srv/app/files/" + value;
            stream = new FileInputStream(new File(path));

            byte[] buffer = new byte[1000];
            int size = stream.read(buffer);

            response.getWriter().println("The beginning of file: '" + path + "' is:\n\n");
            response.getWriter().println(new String(buffer,0,size));

        } catch (Exception e) {

            System.out.println("Failed to open file: '" + path + "'");
            response.getWriter().println("Problem reading file: " + e.getMessage());

        } finally {

            if (stream != null) {
                try {
                    stream.close();
                    stream = null;
                } catch (Exception e) {
                }
            }
        }
    }
}