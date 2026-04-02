import java.io.IOException;

public class RepoDeployer {

    public static void main(String[] args) throws IOException {

        if (args.length == 0) {
            System.out.println("Usage: java RepoDeployer <repositoryUrl>");
            return;
        }

        String repoUrl = args[0];

        String cmd = "git clone " + repoUrl;

        Process process = Runtime.getRuntime().exec(cmd);

        System.out.println("Deployment started for repository: " + repoUrl);
    }
}