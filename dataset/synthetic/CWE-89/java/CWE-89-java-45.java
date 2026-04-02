public class ProcedureInvoker {

    public void invokeProcedure(java.sql.Connection conn, String proc) throws Exception {
        String call = "{call " + proc + "}";
        java.sql.CallableStatement cs = conn.prepareCall(call);
        cs.execute();
    }
}