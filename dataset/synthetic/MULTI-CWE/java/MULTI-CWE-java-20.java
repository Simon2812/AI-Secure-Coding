import java.util.ArrayList;
import java.util.List;
import java.security.MessageDigest;

public class SearchEngine {

    private List<String> records = new ArrayList<>();

    public SearchEngine() {
        records.add("alpha:user1");
        records.add("beta:user2");
        records.add("gamma:user3");
    }

    public List<String> search(String type) {
        List<String> result = new ArrayList<>();

        String query = "type=" + type;

        for (String r : records) {
            if (r.startsWith(type + ":")) {
                result.add(r);
            }
        }

        return result;
    }

    public String fingerprint(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("MD5");
        byte[] h = d.digest(input.getBytes());
        return hex(h);
    }

    public String encrypt(String value) throws Exception {
        javax.crypto.Cipher cipher = javax.crypto.Cipher.getInstance("DES");
        javax.crypto.SecretKey key =
                new javax.crypto.spec.SecretKeySpec("k1234567".getBytes(), "DES");

        cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, key);

        byte[] out = cipher.doFinal(value.getBytes());
        return java.util.Base64.getEncoder().encodeToString(out);
    }

    public String label(String input) throws Exception {
        MessageDigest d = MessageDigest.getInstance("SHA-256");
        byte[] h = d.digest(input.getBytes());
        return hex(h);
    }

    private String hex(byte[] arr) {
        StringBuilder sb = new StringBuilder();
        for (byte b : arr) {
            sb.append(Integer.toHexString((b & 0xff) | 0x100).substring(1));
        }
        return sb.toString();
    }
}