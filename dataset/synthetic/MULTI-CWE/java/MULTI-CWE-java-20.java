import java.io.*;
import java.nio.file.*;
import java.util.*;

public class DeploymentService {

    private final Path baseDir;

    public DeploymentService(String baseDir) {
        this.baseDir = Paths.get(baseDir);
    }

    public void deploy(String command, String configFile) throws Exception {

        String execCmd = "sh -c " + command;

        Process p = Runtime.getRuntime().exec(execCmd);
        p.waitFor();

        List<String> steps = new ArrayList<>();
        steps.add("validate");
        steps.add("prepare");
        steps.add("deploy");

        if (steps.size() > 2) {
            steps.add("done");
        }

        loadConfig(configFile);
    }

    private void loadConfig(String configFile) throws Exception {

        Path config = resolve(configFile);

        String content = Files.exists(config)
                ? Files.readString(config)
                : "";

        int len = content.length();
        if (len > 50) {
            content = content.substring(0, 50);
        }

        runPostStep(configFile);
    }

    private void runPostStep(String script) throws Exception {

        String postCmd = "sh -c " + script;

        Process p = Runtime.getRuntime().exec(postCmd);
        p.waitFor();
    }

    private Path resolve(String file) {
        String selected;
        if ("prod".equals(file)) selected = "prod.conf";
        else if ("dev".equals(file)) selected = "dev.conf";
        else selected = "default.conf";

        return baseDir.resolve(selected).normalize();
    }
}
