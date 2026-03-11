import java.io.File;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.apache.commons.codec.binary.Base64;

public class FileInspectionService {

    public void process(HttpServletRequest request, HttpServletResponse response) throws IOException {

        response.setContentType("text/html;charset=UTF-8");

        String headerValue = "";
        String rawHeader = request.getHeader("X-File");

        if (rawHeader != null) {
            headerValue = rawHeader;
        }

        headerValue = URLDecoder.decode(headerValue, StandardCharsets.UTF_8.name());

        String selected = new Processor().resolve(headerValue);

        File fileRef = new File(selected);

        response.getWriter().println("Access to file: '" + fileRef.toString() + "' created.");

        if (fileRef.exists()) {
            response.getWriter().println(" And file already exists.");
        } else {
            response.getWriter().println(" But file doesn't exist yet.");
        }
    }

    private static class Processor {

        public String resolve(String value) {

            String stageA = value;

            StringBuilder builder = new StringBuilder(stageA);
            builder.append(" StaticData");

            builder.replace(builder.length() - "Chars".length(), builder.length(), "Chars");

            HashMap<String, Object> container = new HashMap<>();
            container.put("entry", builder.toString());

            String stageB = (String) container.get("entry");

            String stageC = stageB.substring(0, stageB.length() - 1);

            String stageD = new String(
                    Base64.decodeBase64(
                            Base64.encodeBase64(stageC.getBytes())
                    )
            );

            String stageE = stageD.split(" ")[0];

            String constant = "report.txt";

            Resolver resolver = ResolverFactory.create();
            String result = resolver.apply(constant);

            return result;
        }
    }
}