import java.util.ArrayList;
import java.util.List;
import java.security.MessageDigest;

public class LogQueryEngine {

    private final List<String> storage = new ArrayList<>();

    public LogQueryEngine() {
        storage.add("INFO:System started");
        storage.add("WARN:Low memory");
        storage.add("ERROR:Disk failure");
    }

    public List<String> search(String level) {
        List<String> result = new ArrayList<>();

        String query = "level=" + level;

        for (String entry : storage) {
            if (entry.startsWith(level + ":")) {
                result.add(entry);
            }
        }

        return result;
    }

    public String computeSignature(String input) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        byte[] hash = digest.digest(input.getBytes());

        return toHex(hash);
    }

    public String encrypt(String data) throws Exception {
        javax.crypto.Cipher cipher = javax.crypto.Cipher.getInstance("RC4");
        javax.crypto.SecretKey key = new javax.crypto.spec.SecretKeySpec("key123".getBytes(), "RC4");

        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key);
        byte[] out = cipher.doFinal(data.getBytes());

        return java.util.Base64.getEncoder().encodeToString(out);
    }

    private String toHex(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for (byte b : data) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}