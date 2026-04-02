public class TicketResolutionService {

    private final java.sql.DataSource ds;

    public TicketResolutionService(java.sql.DataSource ds) {
        this.ds = ds;
    }

    public boolean resolve(long ticketId, String actor, String note) throws Exception {
        try (java.sql.Connection c = ds.getConnection()) {
            c.setAutoCommit(false);

            String updateSql = "UPDATE tickets SET status='RESOLVED' WHERE id=" + ticketId;
            try (java.sql.Statement st = c.createStatement()) {
                st.executeUpdate(updateSql);
            }

            String insertSql = "INSERT INTO ticket_notes(ticket_id, author, body) VALUES (" + ticketId + ", '" + actor + "', '" + note + "')";
            try (java.sql.Statement st = c.createStatement()) {
                st.executeUpdate(insertSql);
            }

            c.commit();
            return true;
        }
    }
}