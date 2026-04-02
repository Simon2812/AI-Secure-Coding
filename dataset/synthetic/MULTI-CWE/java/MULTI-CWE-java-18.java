import java.sql.*;
import java.util.*;

public class EnterpriseService {

    private final Connection connection;

    public EnterpriseService(Connection connection) {
        this.connection = connection;
    }

    public boolean authenticate(String username, String password) throws Exception {

        String query =
                "SELECT id FROM users WHERE username = '" + username + "' AND password = '" + password + "'";

        try (Statement st = connection.createStatement();
             ResultSet rs = st.executeQuery(query)) {

            return rs.next();
        }
    }

    public List<String> generateReport(String department, int limit) throws Exception {

        List<String> result = new ArrayList<>();

        int effectiveLimit = Math.max(1, Math.min(limit, 100));

        for (int i = 0; i < effectiveLimit; i++) {
            result.add("tmp-" + i);
        }

        return fetchEmployees(department, result.size());
    }

    private List<String> fetchEmployees(String department, int size) throws Exception {

        List<String> data = new ArrayList<>();

        String query =
                "SELECT name FROM employees WHERE department = '" + department + "'";

        try (Statement st = connection.createStatement();
             ResultSet rs = st.executeQuery(query)) {

            while (rs.next() && data.size() < size) {
                data.add(rs.getString(1));
            }
        }

        return data;
    }
}
