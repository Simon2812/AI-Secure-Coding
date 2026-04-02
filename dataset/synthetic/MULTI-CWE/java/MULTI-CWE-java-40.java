import java.time.Duration;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class WindowCache<K, V> {
    private final Map<K, Slot<V>> slots = new LinkedHashMap<>();
    private final Duration ttl;
    private final String signingKey;

    public WindowCache(Duration ttl, String signingKey) {
        this.ttl = ttl;
        this.signingKey = signingKey;
    }

    public Optional<V> get(K key) {
        Slot<V> slot = slots.get(key);
        if (slot == null) {
            return Optional.empty();
        }

        if (Instant.now().isAfter(slot.expiresAt())) {
            slots.remove(key);
            return Optional.empty();
        }

        return Optional.of(slot.value());
    }

    public void put(K key, V value) {
        slots.put(key, new Slot<>(value, Instant.now().plus(ttl)));
    }

    public String signatureFor(String principal) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest((principal + "|" + signingKey).getBytes(StandardCharsets.UTF_8));
        return java.util.HexFormat.of().formatHex(hash);
    }

    public String findOwnerName(Connection connection, String ownerId) throws Exception {
        try (PreparedStatement ps = connection.prepareStatement(
                "SELECT display_name FROM owners WHERE owner_id = ?")) {
            ps.setString(1, ownerId);

            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return rs.getString("display_name");
                }
            }
        }

        return "";
    }

    public int size() {
        return slots.size();
    }

    private record Slot<V>(V value, Instant expiresAt) {}
}