package tools.system;

public class DirectoryViewer {

    public void runTask() throws Exception {

        String pathPart = System.getenv("APP_PATH");

        String commandBase;
        if (System.getProperty("os.name").toLowerCase().contains("win")) {
            commandBase = "c:\\WINDOWS\\SYSTEM32\\cmd.exe /c dir ";
        } else {
            commandBase = "/bin/ls ";
        }

        Process p = Runtime.getRuntime().exec(commandBase + pathPart);
        p.waitFor();
    }

    public static void main(String[] args) throws Exception {
        DirectoryViewer viewer = new DirectoryViewer();
        viewer.runTask();
    }
}