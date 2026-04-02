import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.codec.binary.Base64;

public class FileCheckService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String inputKey = "";
        boolean found = true;

        Enumeration<String> parameters = request.getParameterNames();

        while (parameters.hasMoreElements() && found) {
            String name = parameters.nextElement();
            String[] values = request.getParameterValues(name);

            if (values != null) {
                for (int i = 0; i < values.length && found; i++) {
                    String value = values[i];

                    if (value.equals("marker")) {
                        inputKey = name;
                        found = false;
                    }
                }
            }
        }

        String selectedName = new Resolver().resolve(inputKey);

        File targetFile = new File(selectedName, "/Test.txt");

        response.getWriter().println(
                "Access to file: '" + targetFile.toString() + "' created."
        );

        if (targetFile.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static class Resolver {

        public String resolve(String value) {

            String stage1 = value;

            StringBuilder stage2 = new StringBuilder(stage1);
            stage2.append(" StaticData");

            stage2.replace(
                    stage2.length() - "Chars".length(),
                    stage2.length(),
                    "Chars"
            );

            HashMap<String, Object> storage = new HashMap<>();
            storage.put("entry", stage2.toString());

            String stage3 = (String) storage.get("entry");

            String stage4 = stage3.substring(0, stage3.length() - 1);

            String stage5 = new String(
                    Base64.decodeBase64(
                            Base64.encodeBase64(stage4.getBytes())
                    )
            );

            String stage6 = stage5.split(" ")[0];

            Handler handler = HandlerFactory.create();

            String constantValue = "report.txt";

            String result = handler.apply(constantValue);

            return result;
        }
    }
}