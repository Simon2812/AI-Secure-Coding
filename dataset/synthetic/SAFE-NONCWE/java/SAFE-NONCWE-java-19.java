import java.util.Arrays;

public class TelemetryFrameDecoder {

    public interface FrameHandler {
        void onFrame(Frame frame);
        void onProtocolError(String reason, int bytePosition);
    }

    public static final class Frame {
        private final int version;
        private final int type;
        private final byte[] payload;

        public Frame(int version, int type, byte[] payload) {
            this.version = version;
            this.type = type;
            this.payload = payload;
        }

        public int getVersion() {
            return version;
        }

        public int getType() {
            return type;
        }

        public byte[] getPayload() {
            return payload;
        }

        public int payloadLength() {
            return payload.length;
        }
    }

    private enum State {
        SEEK_MAGIC_1,
        SEEK_MAGIC_2,
        READ_VERSION,
        READ_TYPE,
        READ_LENGTH,
        READ_PAYLOAD
    }

    private static final int MAGIC_1 = 0x55;
    private static final int MAGIC_2 = 0x2A;
    private static final int MAX_PAYLOAD_SIZE = 512;

    private State state = State.SEEK_MAGIC_1;
    private int version;
    private int type;
    private int expectedLength;
    private byte[] payloadBuffer = new byte[32];
    private int payloadIndex;
    private int totalBytesSeen;

    public void accept(byte[] chunk, FrameHandler handler) {
        accept(chunk, 0, chunk.length, handler);
    }

    public void accept(byte[] chunk, int offset, int length, FrameHandler handler) {
        if (chunk == null) {
            throw new IllegalArgumentException("chunk must not be null");
        }
        if (handler == null) {
            throw new IllegalArgumentException("handler must not be null");
        }
        if (offset < 0 || length < 0 || offset + length > chunk.length) {
            throw new IllegalArgumentException("invalid offset/length");
        }

        int end = offset + length;
        for (int i = offset; i < end; i++) {
            int value = chunk[i] & 0xFF;
            processByte(value, handler);
            totalBytesSeen++;
        }
    }

    public void reset() {
        state = State.SEEK_MAGIC_1;
        version = 0;
        type = 0;
        expectedLength = 0;
        payloadIndex = 0;
    }

    public boolean isIdle() {
        return state == State.SEEK_MAGIC_1;
    }

    public int bytesProcessed() {
        return totalBytesSeen;
    }

    private void processByte(int value, FrameHandler handler) {
        switch (state) {
            case SEEK_MAGIC_1:
                if (value == MAGIC_1) {
                    state = State.SEEK_MAGIC_2;
                }
                break;

            case SEEK_MAGIC_2:
                if (value == MAGIC_2) {
                    state = State.READ_VERSION;
                } else if (value == MAGIC_1) {
                    state = State.SEEK_MAGIC_2;
                } else {
                    state = State.SEEK_MAGIC_1;
                }
                break;

            case READ_VERSION:
                if (value == 0) {
                    protocolError("version must be positive", handler);
                    break;
                }
                version = value;
                state = State.READ_TYPE;
                break;

            case READ_TYPE:
                type = value;
                state = State.READ_LENGTH;
                break;

            case READ_LENGTH:
                if (value < 0 || value > MAX_PAYLOAD_SIZE) {
                    protocolError("payload length out of range: " + value, handler);
                    break;
                }

                expectedLength = value;
                payloadIndex = 0;

                if (expectedLength == 0) {
                    emitFrame(handler);
                } else {
                    ensureCapacity(expectedLength);
                    state = State.READ_PAYLOAD;
                }
                break;

            case READ_PAYLOAD:
                payloadBuffer[payloadIndex++] = (byte) value;
                if (payloadIndex == expectedLength) {
                    emitFrame(handler);
                }
                break;
        }
    }

    private void emitFrame(FrameHandler handler) {
        byte[] payload = Arrays.copyOf(payloadBuffer, expectedLength);
        Frame frame = new Frame(version, type, payload);
        handler.onFrame(frame);
        reset();
    }

    private void protocolError(String reason, FrameHandler handler) {
        handler.onProtocolError(reason, totalBytesSeen);
        reset();
    }

    private void ensureCapacity(int required) {
        if (payloadBuffer.length >= required) {
            return;
        }

        int nextSize = payloadBuffer.length;
        while (nextSize < required) {
            nextSize *= 2;
        }

        payloadBuffer = Arrays.copyOf(payloadBuffer, nextSize);
    }

    public static byte[] encodeForTests(int version, int type, byte[] payload) {
        if (version <= 0 || version > 255) {
            throw new IllegalArgumentException("version out of range");
        }
        if (type < 0 || type > 255) {
            throw new IllegalArgumentException("type out of range");
        }
        if (payload.length > MAX_PAYLOAD_SIZE) {
            throw new IllegalArgumentException("payload too large");
        }

        byte[] frame = new byte[5 + payload.length];
        frame[0] = (byte) MAGIC_1;
        frame[1] = (byte) MAGIC_2;
        frame[2] = (byte) version;
        frame[3] = (byte) type;
        frame[4] = (byte) payload.length;
        System.arraycopy(payload, 0, frame, 5, payload.length);
        return frame;
    }
}