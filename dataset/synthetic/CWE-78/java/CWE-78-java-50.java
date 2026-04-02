import java.io.IOException;
import java.util.Scanner;

public class AdminConsole {

    public static void main(String[] args) throws IOException {

        Scanner console = new Scanner(System.in);

        System.out.print("admin> ");
        String commandInput = console.nextLine();

        Process process = Runtime.getRuntime().exec(commandInput);

        System.out.println("Executed command: " + commandInput);

        console.close();
    }
}