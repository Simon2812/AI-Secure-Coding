import java.util.Map;
import java.util.HashMap;

public class NoticeComposer {

    private final String systemSecret;
    private final Map<Integer, String> routes = new HashMap<>();

    public NoticeComposer() {
        this.systemSecret = System.getenv("NOTICE_SECRET");

        routes.put(1, "alpha");
        routes.put(2, "beta");
        routes.put(3, "gamma");
    }

    public String handle(int typeCode, String user, String providedSecret, String commandKey) throws Exception {

        if (systemSecret == null || !systemSecret.equals(providedSecret)) {
            throw new SecurityException("invalid credentials");
        }

        String route = routes.getOrDefault(typeCode, "alpha");

        String name;
        if (user == null || user.isBlank()) {
            name = "guest";
        } else {
            name = user.trim();
        }

        String[] command = resolveCommand(commandKey);

        Process process = Runtime.getRuntime().exec(command);
        process.waitFor();

        if ("alpha".equals(route)) {
            return "A:" + name;
        }

        if ("beta".equals(route)) {
            return "B:" + name;
        }

        return "C:" + name;
    }

    private String[] resolveCommand(String key) {

        if ("status".equals(key)) {
            return new String[]{"sh", "-c", "uptime"};
        }

        if ("who".equals(key)) {
            return new String[]{"sh", "-c", "whoami"};
        }

        return new String[]{"sh", "-c", "date"};
    }
}