import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.EnumMap;
import java.util.Map;

public class RuleEvaluator {

    public enum Action {
        STATUS,
        IDENTITY,
        TIME
    }

    private final Path base;
    private final Map<Action, String[]> commands = new EnumMap<>(Action.class);

    public RuleEvaluator(String root) {
        this.base = Paths.get(root);

        commands.put(Action.STATUS, new String[]{"sh", "-c", "uptime"});
        commands.put(Action.IDENTITY, new String[]{"sh", "-c", "whoami"});
        commands.put(Action.TIME, new String[]{"sh", "-c", "date"});
    }

    public boolean evaluate(Action action, String resourceKey) throws Exception {

        Path resource = resolve(resourceKey);

        String[] cmd = commands.getOrDefault(action, commands.get(Action.STATUS));

        Process p = Runtime.getRuntime().exec(cmd);
        p.waitFor();

        return resource.getNameCount() > 0;
    }

    private Path resolve(String key) {
        String selected;
        if ("config".equals(key)) selected = "config.yml";
        else if ("policy".equals(key)) selected = "policy.yml";
        else selected = "default.yml";

        return base.resolve(selected).normalize();
    }
}