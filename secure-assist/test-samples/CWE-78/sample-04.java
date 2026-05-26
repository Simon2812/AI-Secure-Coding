import javax.servlet.http.*;
import java.io.*;

public class ConvertServlet extends HttpServlet {
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String inputFile = req.getParameter("input");
        String outputFile = req.getParameter("output");
        String cmd = "convert " + inputFile + " " + outputFile;
        Process p = new ProcessBuilder(cmd).start();
        p.waitFor();
        resp.getWriter().write("done");
    }
}
