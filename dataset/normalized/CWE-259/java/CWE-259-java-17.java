import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import javax.security.auth.kerberos.KerberosPrincipal;
import javax.security.auth.kerberos.KerberosKey;

public class KerberosAuth {

    public void authenticate() {
        String password = "";

        try {
            BufferedReader reader = new BufferedReader(
                    new InputStreamReader(System.in, "UTF-8")
            );
            password = reader.readLine();
        } catch (IOException e) {
            System.err.println("Input error: " + e.getMessage());
        }

        if (password != null) {
            KerberosPrincipal principal = new KerberosPrincipal("test");

            KerberosKey key = new KerberosKey(
                    principal,
                    password.toCharArray(),
                    null
            );

            System.out.println(key.toString());
        }
    }

    public static void main(String[] args) {
        new KerberosAuth().authenticate();
    }
}