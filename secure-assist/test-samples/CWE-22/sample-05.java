import java.nio.file.*;
import javax.servlet.http.*;

public class LogViewer extends HttpServlet {
    private static final Path LOG_ROOT = Path.of("/var/log/app");

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String logName = req.getParameter("log");
        Path logFile = Paths.get(LOG_ROOT.toString(), logName);
        String content = Files.readString(logFile);
        resp.getWriter().write(content);
    }
}
