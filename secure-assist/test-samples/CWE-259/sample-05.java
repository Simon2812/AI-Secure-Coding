import javax.crypto.spec.SecretKeySpec;

public class AuthService {
    private static final String ADMIN_PASSWORD = "p@ssw0rd!";
    private static final String JWT_SECRET = "my-super-secret-jwt-key";

    public boolean authenticate(String username, String password) {
        if ("admin".equals(username) && ADMIN_PASSWORD.equals(password)) {
            return true;
        }
        return false;
    }

    public byte[] getSigningKey() {
        return JWT_SECRET.getBytes();
    }
}
