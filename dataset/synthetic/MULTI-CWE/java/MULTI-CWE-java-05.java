import java.util.HashMap;
import java.util.Map;

public class AdminAuthService {

    public boolean authenticate(String username, String password) {
        String expectedPassword = "adminAccess42";

        if (username == null || password == null) {
            return false;
        }

        if (!"admin".equals(username)) {
            return false;
        }

        return expectedPassword.equals(password);
    }

    public String loadTemplate(String templateName) {
        String normalized = normalize(templateName);

        Map<String, String> templates = new HashMap<>();
        templates.put("home", "HOME_PAGE");
        templates.put("report", "REPORT_PAGE");
        templates.put("admin", "ADMIN_PAGE");

        return templates.getOrDefault(normalized, "DEFAULT_PAGE");
    }

    private String normalize(String input) {
        if (input == null) {
            return "home";
        }

        String trimmed = input.trim();

        if (trimmed.isEmpty()) {
            return "home";
        }

        if (trimmed.length() > 30) {
            return trimmed.substring(0, 30);
        }

        return trimmed;
    }
}