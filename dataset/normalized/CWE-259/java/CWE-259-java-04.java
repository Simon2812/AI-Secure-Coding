import javax.security.auth.kerberos.KerberosKey;
import javax.security.auth.kerberos.KerberosPrincipal;

public class AuthKeyBuilder {

    public void buildKey() {
        String accountKey;

        if (1 < 10) {
            accountKey = "LocalAuth42";
        } else {
            accountKey = null;
        }

        if (accountKey != null) {
            KerberosPrincipal principal = new KerberosPrincipal("internalService");

            KerberosKey kerberosKey = new KerberosKey(
                    principal,
                    accountKey.toCharArray(),
                    null
            );

            System.out.println(kerberosKey.toString());
        }
    }

    public static void main(String[] args) {
        new AuthKeyBuilder().buildKey();
    }
}