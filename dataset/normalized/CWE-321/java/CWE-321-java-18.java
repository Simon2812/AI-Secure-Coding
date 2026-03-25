import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class ConsoleKeyProcessor extends AbstractTestCase
{
    private int selector = 5;

    public void executeFlow() throws Throwable
    {
        String keyMaterial;
        if (selector != 5)
        {
            keyMaterial = null;
        }
        else
        {
            keyMaterial = "";
            try
            {
                InputStreamReader stream = new InputStreamReader(System.in, "UTF-8");
                BufferedReader reader = new BufferedReader(stream);
                keyMaterial = reader.readLine();
            }
            catch (IOException e)
            {
                IO.logger.log(Level.WARNING, "Error with stream reading", e);
            }
        }

        if (keyMaterial != null)
        {
            String message = "My message";
            byte[] payload = message.getBytes("UTF-8");

            SecretKeySpec key = new SecretKeySpec(keyMaterial.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);

            byte[] result = cipher.doFinal(payload);
            IO.writeLine(IO.toHex(result));
        }
    }

    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}