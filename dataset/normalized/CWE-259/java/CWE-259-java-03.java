import javax.security.auth.kerberos.KerberosKey;
import javax.security.auth.kerberos.KerberosPrincipal;

public class TicketInitializer {

    public void initialize() {
        String tokenValue = "OfficePass!9";

        if (tokenValue != null) {
            KerberosPrincipal userPrincipal = new KerberosPrincipal("serviceUser");

            KerberosKey sessionKey = new KerberosKey(
                    userPrincipal,
                    tokenValue.toCharArray(),
                    null
            );

            System.out.println(sessionKey.toString());
        }
    }

    public static void main(String[] args) {
        new TicketInitializer().initialize();
    }
}