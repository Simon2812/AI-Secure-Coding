import java.net.PasswordAuthentication;

public class Property {

    public void auth() {
        String runtimeKey = System.getProperty("app.secret");

        if (runtimeKey != null) {
            PasswordAuthentication auth = new PasswordAuthentication(
                    "runtimeUser",
                    runtimeKey.toCharArray()
            );

            System.out.println(auth.toString());
        } else {
            System.err.println("Missing system property: app.secret");
        }
    }

    public static void main(String[] args) {
        new Property().auth();
    }
}