public class LeaderboardView {

    private final java.sql.DataSource ds;

    public LeaderboardView(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public java.util.Map<String, Object> top(String category, String sort, int limit) throws Exception {
        if (limit < 1) limit = 10;
        if (limit > 100) limit = 100;

        String order = safeSort(sort);

        java.util.HashMap<String, Object> out = new java.util.HashMap<>();
        out.put("category", category);

        try (java.sql.Connection c = ds.getConnection()) {
            java.util.List<String> rows = fetch(c, category, order, limit);
            long total = count(c, category);

            out.put("total", total);
            out.put("rows", rows);
        }

        return out;
    }

    private java.util.List<String> fetch(java.sql.Connection c, String category, String order, int limit) throws Exception {
        String sql = "SELECT username, score FROM leaderboard WHERE category=? ORDER BY " + order + " DESC LIMIT " + limit;

        java.util.ArrayList<String> out = new java.util.ArrayList<>();

        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, category);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    out.add(rs.getString(1) + ":" + rs.getInt(2));
                }
            }
        }

        return out;
    }

    private long count(java.sql.Connection c, String category) throws Exception {
        String sql = "SELECT COUNT(*) FROM leaderboard WHERE category=?";
        try (java.sql.PreparedStatement ps = c.prepareStatement(sql)) {
            ps.setString(1, category);
            try (java.sql.ResultSet rs = ps.executeQuery()) {
                rs.next();
                return rs.getLong(1);
            }
        }
    }

    private String safeSort(String sort) {
        if (sort == null) return "score";
        return switch (sort) {
            case "score" -> "score";
            case "name" -> "username";
            default -> "score";
        };
    }
}
