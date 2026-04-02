import java.io.File;
import java.io.IOException;
import java.util.Enumeration;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.codec.binary.Base64;

public class StorageAuditHandler {

    public void handle(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String discoveredKey = "";
        boolean searching = true;

        Enumeration<String> parameters = request.getParameterNames();

        while (parameters.hasMoreElements() && searching) {

            String key = parameters.nextElement();
            String[] entries = request.getParameterValues(key);

            if (entries != null) {

                for (int i = 0; i < entries.length && searching; i++) {

                    String element = entries[i];

                    if (element.equals("marker")) {
                        discoveredKey = key;
                        searching = false;
                    }
                }
            }
        }

        String finalName = computePath(discoveredKey);

        File storageRoot = new File("/data/repository");
        File inspectedObject = new File(storageRoot, finalName);

        response.getWriter().println(
                "Access to file: '" + inspectedObject.toString() + "' created."
        );

        if (inspectedObject.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static String computePath(String incoming) {

        String stageOne = incoming;

        StringBuilder stageTwo = new StringBuilder(stageOne);
        stageTwo.append(" ConstantSuffix");

        stageTwo.replace(
                stageTwo.length() - "Chars".length(),
                stageTwo.length(),
                "Chars"
        );

        HashMap<String, Object> container = new HashMap<>();
        container.put("node", stageTwo.toString());

        String stageThree = (String) container.get("node");

        String stageFour = stageThree.substring(0, stageThree.length() - 1);

        String stageFive = new String(
                Base64.decodeBase64(
                        Base64.encodeBase64(stageFour.getBytes())
                )
        );

        String stageSix = stageFive.split(" ")[0];

        Executor executor = ExecutorFactory.build();

        String constantEntry = "report.data";

        String resolved = executor.apply(constantEntry);

        return resolved;
    }
}