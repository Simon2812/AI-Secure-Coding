package infra.ops;

public class HomeDirectoryListing {

    public void run() throws Exception {

        String location;

        if (true) {
            location = System.getProperty("user.home");
        } else {
            location = null;
        }

        String program;

        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            program = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            program = "/bin/ls ";
        }

        Process job = Runtime.getRuntime().exec(program + location);
        job.waitFor();
    }

    public static void main(String[] args) throws Exception {
        new HomeDirectoryListing().run();
    }
}