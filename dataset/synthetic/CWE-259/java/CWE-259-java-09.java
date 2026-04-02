import java.net.PasswordAuthentication;

public class DirectAuthUsage {

    public void authenticate() {
        PasswordAuthentication auth = new PasswordAuthentication(
                "directUser",
                "blueNodeKey".toCharArray()
        );

        System.out.println(auth.toString());
    }

    public static void main(String[] args) {
        new DirectAuthUsage().authenticate();
    }
}