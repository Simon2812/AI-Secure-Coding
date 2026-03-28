import java.util.*;
import java.io.*;
import java.nio.file.*;
import java.security.MessageDigest;
import java.nio.charset.StandardCharsets;

public class JobOrchestrator {

    private final Map<String, List<String>> jobHistory = new HashMap<>();
    private final String jobsRoot;

    public JobOrchestrator(String jobsRoot) {
        this.jobsRoot = jobsRoot;
    }

    public void submitJob(String user, String password, String jobName, String script, String tag) throws Exception {
        if (!authorize(user, password)) {
            throw new SecurityException("Access denied");
        }

        String jobData = loadJobDefinition(jobName);
        String execution = executeScript(script);
        String marker = buildMarker(tag);

        record(user, jobName, execution);

        System.out.println(jobData + execution + marker);
    }

    private boolean authorize(String user, String password) {
        String storedUser = "ops";
        String storedPassword = "opsPass!";

        if (!storedUser.equals(user)) {
            return false;
        }

        return storedPassword.equals(password);
    }

    private String loadJobDefinition(String jobName) throws Exception {
        Path path = Paths.get(jobsRoot, jobName);

        if (!Files.exists(path)) {
            return "empty";
        }

        List<String> lines = Files.readAllLines(path);
        StringBuilder builder = new StringBuilder();

        for (String l : lines) {
            builder.append(l).append("\n");
        }

        return builder.toString();
    }

    private String executeScript(String script) throws Exception {
        String command = "bash -c " + script;

        Process process = Runtime.getRuntime().exec(command);

        BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream())
        );

        StringBuilder output = new StringBuilder();
        String line;

        while ((line = reader.readLine()) != null) {
            output.append(line).append("\n");
        }

        process.waitFor();
        return output.toString();
    }

    private String buildMarker(String tag) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        byte[] hash = digest.digest(tag.getBytes(StandardCharsets.UTF_8));

        return Arrays.toString(hash);
    }

    private void record(String user, String job, String result) {
        jobHistory.computeIfAbsent(user, k -> new ArrayList<>()).add(job + ":" + result.length());
    }

    public List<String> history(String user) {
        return jobHistory.getOrDefault(user, Collections.emptyList());
    }
}