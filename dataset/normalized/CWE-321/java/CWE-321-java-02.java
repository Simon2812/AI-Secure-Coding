import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class MessageEncryptionService extends AbstractTestCase
{
    public void processRequest() throws Throwable
    {
        String token;
        if (true)
        {
            token = "23 ~j;asn!@#/>as";
        }
        else
        {
            token = null;
        }

        if (token != null)
        {
            String payload = "Hello World!";
            byte[] input = payload.getBytes("UTF-8");
            SecretKeySpec key = new SecretKeySpec(token.getBytes("UTF-8"), "AES");
            Cipher engine = Cipher.getInstance("AES");
            engine.init(Cipher.ENCRYPT_MODE, key);
            byte[] output = engine.doFinal(input);
            IO.writeLine(IO.toHex(output));
        }
    }
    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}