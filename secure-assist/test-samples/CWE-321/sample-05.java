import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

public class TokenManager {
    private static final String JWT_SECRET_KEY = "hardcoded-secret-key-for-jwt-signing";

    public static String generateToken(String userId) {
        return Jwts.builder()
            .setSubject(userId)
            .signWith(SignatureAlgorithm.HS256, JWT_SECRET_KEY.getBytes())
            .compact();
    }

    public static String parseToken(String token) {
        return Jwts.parser()
            .setSigningKey(JWT_SECRET_KEY.getBytes())
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}
