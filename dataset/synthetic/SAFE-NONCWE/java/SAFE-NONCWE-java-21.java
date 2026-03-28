import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class DocumentMergeEngine {

    public static final class Conflict {
        private final int index;
        private final String baseLine;
        private final String leftLine;
        private final String rightLine;

        public Conflict(int index, String baseLine, String leftLine, String rightLine) {
            this.index = index;
            this.baseLine = baseLine;
            this.leftLine = leftLine;
            this.rightLine = rightLine;
        }

        public int getIndex() {
            return index;
        }

        public String getBaseLine() {
            return baseLine;
        }

        public String getLeftLine() {
            return leftLine;
        }

        public String getRightLine() {
            return rightLine;
        }
    }

    public static final class MergeResult {
        private final List<String> merged;
        private final List<Conflict> conflicts;

        public MergeResult(List<String> merged, List<Conflict> conflicts) {
            this.merged = merged;
            this.conflicts = conflicts;
        }

        public List<String> getMerged() {
            return new ArrayList<>(merged);
        }

        public List<Conflict> getConflicts() {
            return new ArrayList<>(conflicts);
        }

        public boolean hasConflicts() {
            return !conflicts.isEmpty();
        }
    }

    public MergeResult merge(
            List<String> base,
            List<String> left,
            List<String> right
    ) {
        Objects.requireNonNull(base);
        Objects.requireNonNull(left);
        Objects.requireNonNull(right);

        int max = Math.max(base.size(), Math.max(left.size(), right.size()));

        List<String> result = new ArrayList<>();
        List<Conflict> conflicts = new ArrayList<>();

        for (int i = 0; i < max; i++) {
            String b = get(base, i);
            String l = get(left, i);
            String r = get(right, i);

            if (equals(l, r)) {
                result.add(l);
                continue;
            }

            if (equals(b, l)) {
                result.add(r);
                continue;
            }

            if (equals(b, r)) {
                result.add(l);
                continue;
            }

            conflicts.add(new Conflict(i, b, l, r));
            result.add(resolveConflict(l, r));
        }

        return new MergeResult(result, conflicts);
    }

    private String get(List<String> list, int index) {
        return index < list.size() ? list.get(index) : null;
    }

    private boolean equals(String a, String b) {
        if (a == null) return b == null;
        return a.equals(b);
    }

    private String resolveConflict(String left, String right) {
        String l = left == null ? "" : left;
        String r = right == null ? "" : right;

        return "<<<<<<< LEFT\n" +
               l + "\n" +
               "=======\n" +
               r + "\n" +
               ">>>>>>> RIGHT";
    }

    public static DocumentMergeEngine sampleEngine() {
        return new DocumentMergeEngine();
    }
}import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

public class DocumentMergeEngine {

    public static final class Conflict {
        private final int index;
        private final String baseLine;
        private final String leftLine;
        private final String rightLine;

        public Conflict(int index, String baseLine, String leftLine, String rightLine) {
            this.index = index;
            this.baseLine = baseLine;
            this.leftLine = leftLine;
            this.rightLine = rightLine;
        }

        public int getIndex() {
            return index;
        }

        public String getBaseLine() {
            return baseLine;
        }

        public String getLeftLine() {
            return leftLine;
        }

        public String getRightLine() {
            return rightLine;
        }
    }

    public static final class MergeResult {
        private final List<String> merged;
        private final List<Conflict> conflicts;

        public MergeResult(List<String> merged, List<Conflict> conflicts) {
            this.merged = merged;
            this.conflicts = conflicts;
        }

        public List<String> getMerged() {
            return new ArrayList<>(merged);
        }

        public List<Conflict> getConflicts() {
            return new ArrayList<>(conflicts);
        }

        public boolean hasConflicts() {
            return !conflicts.isEmpty();
        }
    }

    public MergeResult merge(
            List<String> base,
            List<String> left,
            List<String> right
    ) {
        Objects.requireNonNull(base);
        Objects.requireNonNull(left);
        Objects.requireNonNull(right);

        int max = Math.max(base.size(), Math.max(left.size(), right.size()));

        List<String> result = new ArrayList<>();
        List<Conflict> conflicts = new ArrayList<>();

        for (int i = 0; i < max; i++) {
            String b = get(base, i);
            String l = get(left, i);
            String r = get(right, i);

            if (equals(l, r)) {
                result.add(l);
                continue;
            }

            if (equals(b, l)) {
                result.add(r);
                continue;
            }

            if (equals(b, r)) {
                result.add(l);
                continue;
            }

            conflicts.add(new Conflict(i, b, l, r));
            result.add(resolveConflict(l, r));
        }

        return new MergeResult(result, conflicts);
    }

    private String get(List<String> list, int index) {
        return index < list.size() ? list.get(index) : null;
    }

    private boolean equals(String a, String b) {
        if (a == null) return b == null;
        return a.equals(b);
    }

    private String resolveConflict(String left, String right) {
        String l = left == null ? "" : left;
        String r = right == null ? "" : right;

        return "<<<<<<< LEFT\n" +
               l + "\n" +
               "=======\n" +
               r + "\n" +
               ">>>>>>> RIGHT";
    }

    public static DocumentMergeEngine sampleEngine() {
        return new DocumentMergeEngine();
    }
}