import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.PreparedStatement;
import java.sql.Connection;
import java.util.ArrayList;
import java.util.List;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.util.Base64;

public class AttachmentCatalog {
    private final Path storageRoot;
    private final SecureRandom random = new SecureRandom();

    public AttachmentCatalog(String storageRoot) {
        this.storageRoot = Paths.get(storageRoot);
    }

    public UploadReceipt register(Connection connection, String category, String attachmentName, byte[] payload) throws Exception {
        String normalizedCategory = category != null && category.matches("[a-zA-Z0-9_]+") ? category : "general";
        Path target = storageRoot.resolve(attachmentName == null ? "default.bin" : attachmentName).normalize();

        String token = protectReference(normalizedCategory + ":" + target.getFileName());

        try (PreparedStatement stmt = connection.prepareStatement(
                "INSERT INTO attachments(category, file_name, ref_token) VALUES (?, ?, ?)")) {
            stmt.setString(1, normalizedCategory);
            stmt.setString(2, target.getFileName().toString());
            stmt.setString(3, token);
            stmt.executeUpdate();
        }

        List<String> notes = new ArrayList<>();
        notes.add("stored:" + target.getFileName());
        notes.add("size:" + payload.length);

        return new UploadReceipt(target.toString(), token, notes);
    }

    private String protectReference(String value) throws Exception {
        byte[] keyBytes = new byte[16];
        byte[] iv = new byte[12];
        random.nextBytes(keyBytes);
        random.nextBytes(iv);

        SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, key, new GCMParameterSpec(128, iv));

        byte[] encrypted = cipher.doFinal(value.getBytes(StandardCharsets.UTF_8));
        return Base64.getEncoder().encodeToString(encrypted);
    }

    public record UploadReceipt(String path, String reference, List<String> notes) {}
}