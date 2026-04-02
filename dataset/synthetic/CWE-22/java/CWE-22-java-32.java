import java.io.FileInputStream;
import java.io.IOException;

public class TemplateDepot {

    private static final String baseDirectory = "/opt/templates/";

    public int loadTemplate(String templateKey) throws IOException {
        String path = buildTemplatePath(templateKey);
        FileInputStream in = new FileInputStream(path);
        return in.read();
    }

    private String buildTemplatePath(String key) {
        return baseDirectory + key + ".tpl";
    }
}