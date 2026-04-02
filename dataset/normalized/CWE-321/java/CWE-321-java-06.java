import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class RequestCipherExecutor extends AbstractTestCase
{
    public void handleRequest() throws Throwable
    {
        String selectedValue;
        if (IO.staticTrue)
        {
            selectedValue = "zX7pL2mQ9vT4sR8w";
        }
        else
        {
            selectedValue = null;
        }

        if (selectedValue != null)
        {
            String text = "Very interesting text";
            byte[] input = text.getBytes("UTF-8");
            SecretKeySpec key = new SecretKeySpec(selectedValue.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] output = cipher.doFinal(input);
            IO.writeLine(IO.toHex(output));
        }
    }

    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}