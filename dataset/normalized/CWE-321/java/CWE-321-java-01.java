import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class DataProtectionHandler extends AbstractTestCase
{
    public void execute() throws Throwable
    {
        String configuredValue = "23 ~j;asn!@#/>as";

        if (configuredValue != null)
        {
            String message = "What's upp?";
            byte[] input = message.getBytes("UTF-8");
            SecretKeySpec secretKey = new SecretKeySpec(configuredValue.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, secretKey);
            byte[] result = cipher.doFinal(input);
            IO.writeLine(IO.toHex(result));
        }
    }

    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}