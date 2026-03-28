import java.util.Map;
import java.util.HashMap;

public class ConfigAuthenticator {

    private Map<String, String> settings = new HashMap<>();

    public ConfigAuthenticator() {
        settings.put("mode", "prod");
        settings.put("featureX", "enabled");
    }

    public boolean verify(String user, String password) {
        String expectedUser = "admin";
        String expectedPassword = "configPass99";

        if (!expectedUser.equals(user)) {
            return false;
        }

        return expectedPassword.equals(password);
    }

    public String encrypt(String value) throws Exception {
        String key = "fixedKeyValue";

        javax.crypto.SecretKey secret =
                new javax.crypto.spec.SecretKeySpec(key.getBytes(), "AES");

        javax.crypto.Cipher cipher =
                javax.crypto.Cipher.getInstance("AES");

        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, secret);

        byte[] out = cipher.doFinal(value.getBytes());

        return java.util.Base64.getEncoder().encodeToString(out);
    }

    public String readSetting(String key) {
        return settings.getOrDefault(key, "undefined");
    }
}