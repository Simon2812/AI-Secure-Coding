public class TeamKpiSnapshot {

    private final java.sql.DataSource ds;

    public TeamKpiSnapshot(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.Map<String, Object> snapshot(String team, String month, String sort) throws Exception {
        java.util.HashMap<String, Object> out = new java.util.HashMap<>();
        String order = safeSort(sort);

        out.put("team", team);
        out.put("month", month);
        out.put("topAgents", topAgents(team, month, order));
        out.put("openTickets", openTickets(team, month));
        return out;
    }

    private String safeSort(String sort) {
        if (sort == null) return "resolved_count";
        return switch (sort) {
            case "resolved" -> "resolved_count";
            case "sla" -> "sla_breaches";
            case "name" -> "agent_name";
            default -> "resolved_count";
        };
    }

    private java.util.List<String> topAgents(String team, String month, String order) throws Exception {
        String sql = "SELECT agent_name, resolved_count, sla_breaches FROM team_kpi WHERE team=? AND month=? ORDER BY " + order + " DESC";

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {

            ps.setString(1, team);
            ps.setString(2, month);

            try (java.sql.ResultSet rs = ps.executeQuery()) {
                int n = 0;
                while (rs.next() && n < 10) {
                    out.add(rs.getString(1) + ":" + rs.getInt(2) + ":" + rs.getInt(3));
                    n++;
                }
            }
        }

        return out;
    }

    private long openTickets(String team, String month) throws Exception {
        String sql = "SELECT COUNT(*) FROM tickets WHERE team=? AND month=? AND status=?";
        try (java.sql.Connection c = ds.getConnection();
             java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, team);
            ps.setString(2, month);
            ps.setString(3, "OPEN");
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getLong(1);
            }
        }
    }
}