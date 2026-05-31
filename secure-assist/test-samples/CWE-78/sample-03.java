import javax.servlet.http.*;
import java.io.*;

public class NslookupServlet extends HttpServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        String domain = req.getParameter("domain");
        Runtime runtime = Runtime.getRuntime();
        Process proc = runtime.exec("nslookup " + domain);
        BufferedReader reader = new BufferedReader(new InputStreamReader(proc.getInputStream()));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) sb.append(line).append("\n");
        resp.getWriter().write(sb.toString());
    }
}
