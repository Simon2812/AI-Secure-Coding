import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.codec.binary.Base64;

public class ResourceInspector {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String inputValue = request.getParameter("item");

        String selectedName = new Resolver().resolve(inputValue);

        File targetFile = new File("/srv/storage", selectedName);

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

            String stageA = value;

            StringBuilder stageB = new StringBuilder(stageA);
            stageB.append(" StaticContent");

            stageB.replace(
                    stageB.length() - "Chars".length(),
                    stageB.length(),
                    "Chars"
            );

            HashMap<String, Object> container = new HashMap<>();
            container.put("entry", stageB.toString());

            String stageC = (String) container.get("entry");

            String stageD = stageC.substring(0, stageC.length() - 1);

            String stageE = new String(
                    Base64.decodeBase64(
                            Base64.encodeBase64(stageD.getBytes())
                    )
            );

            String stageF = stageE.split(" ")[0];

            Processor processor = ProcessorFactory.create();

            String constantValue = "report.txt";

            String result = processor.apply(constantValue);

            return result;
        }
    }
}