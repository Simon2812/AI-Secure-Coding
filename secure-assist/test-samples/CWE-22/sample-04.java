import java.io.*;
import javax.servlet.http.*;

public class FileReaderServlet extends HttpServlet {
    private static final String BASE = "/var/data/reports/";

    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        String name = req.getParameter("report");
        File file = new File(BASE + name);
        BufferedReader reader = new BufferedReader(new FileReader(file));
        String line;
        StringBuilder sb = new StringBuilder();
        while ((line = reader.readLine()) != null) sb.append(line);
        reader.close();
        resp.getWriter().write(sb.toString());
    }
}
