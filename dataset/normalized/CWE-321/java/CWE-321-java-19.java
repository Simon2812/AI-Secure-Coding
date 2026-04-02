import juliet.support.IO;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;

public class EnvironmentKeyHandler extends AbstractTestCase
{
    public void perform() throws Throwable
    {
        String keyInput;
        if (IO.STATIC_FINAL_FALSE)
        {
            keyInput = null;
        }
        else
        {
            keyInput = System.getenv("APP_KEY");
        }

        if (keyInput != null)
        {
            String payload = "Secret";
            byte[] data = payload.getBytes("UTF-8");

            SecretKeySpec key = new SecretKeySpec(keyInput.getBytes("UTF-8"), "AES");
            Cipher cipher = Cipher.getInstance("AES");
            cipher.init(Cipher.ENCRYPT_MODE, key);

            byte[] result = cipher.doFinal(data);
            IO.writeLine(IO.toHex(result));
        }
    }

    public static void main(String[] args) throws ClassNotFoundException,
            InstantiationException, IllegalAccessException
    {
        mainFromParent(args);
    }
}
