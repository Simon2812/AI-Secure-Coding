import java.net.PasswordAuthentication;

public class TokenGenerator {

    public void create() {
        String base = "coreAccess";
        String authToken = base + "!";

        if (authToken != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "tokenUser",
                    authToken.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new TokenGenerator().create();
    }
}