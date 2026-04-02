import juliet.support.AbstractTestCase;
import juliet.support.IO;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class PayloadCipherManager extends AbstractTestCase
{
    private static final int CONTROL_FLAG = 5;

    public void runPrimary() throws Throwable
    {
        String material;
        if (CONTROL_FLAG == 5)
        {
            material = "k9D31pLm2Qa7sX0r";
        }
        else
        {
            material = null;
        }

        if (material != null)
        {
            String content = "Secret message...";
            byte[] input = content.getBytes("UTF-8");
            SecretKeySpec key = new SecretKeySpec(material.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);
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