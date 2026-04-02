import java.net.PasswordAuthentication;

public class TokenGenerator{

    private String fetchCredential() {
        return System.getenv("AUTH_SECRET");
    }

    public void create() {
        String value = fetchCredential();

        if (value != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "indirectUser",
                    value.toCharArray()
            );

            System.out.println(auth.toString());
        }
    }

    public static void main(String[] args) {
        new TokenGenerator().create();
    }
}