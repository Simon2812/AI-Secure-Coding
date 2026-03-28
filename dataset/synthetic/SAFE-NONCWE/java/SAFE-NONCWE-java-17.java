import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class EditableNoteSession {

    public interface EditCommand {
        void apply(NoteBuffer buffer);
        void revert(NoteBuffer buffer);
        String name();
    }

    public static final class NoteBuffer {
        private final List<String> lines = new ArrayList<>();
        private String title = "";
        private boolean dirty;

        public String getTitle() {
            return title;
        }

        public List<String> snapshotLines() {
            return new ArrayList<>(lines);
        }

        public boolean isDirty() {
            return dirty;
        }

        void setTitleInternal(String title) {
            this.title = title;
            this.dirty = true;
        }

        void insertLineInternal(int index, String value) {
            if (index < 0 || index > lines.size()) {
                throw new IllegalArgumentException("Line index out of range");
            }
            lines.add(index, value);
            this.dirty = true;
        }

        String removeLineInternal(int index) {
            if (index < 0 || index >= lines.size()) {
                throw new IllegalArgumentException("Line index out of range");
            }
            this.dirty = true;
            return lines.remove(index);
        }

        String replaceLineInternal(int index, String value) {
            if (index < 0 || index >= lines.size()) {
                throw new IllegalArgumentException("Line index out of range");
            }
            this.dirty = true;
            return lines.set(index, value);
        }

        void markClean() {
            this.dirty = false;
        }

        public String joinedText() {
            return String.join("\n", lines);
        }
    }

    public static final class SetTitleCommand implements EditCommand {
        private final String newTitle;
        private String previousTitle;

        public SetTitleCommand(String newTitle) {
            this.newTitle = newTitle;
        }

        @Override
        public void apply(NoteBuffer buffer) {
            previousTitle = buffer.getTitle();
            buffer.setTitleInternal(newTitle);
        }

        @Override
        public void revert(NoteBuffer buffer) {
            buffer.setTitleInternal(previousTitle);
        }

        @Override
        public String name() {
            return "SetTitle";
        }
    }

    public static final class InsertLineCommand implements EditCommand {
        private final int index;
        private final String value;

        public InsertLineCommand(int index, String value) {
            this.index = index;
            this.value = value;
        }

        @Override
        public void apply(NoteBuffer buffer) {
            buffer.insertLineInternal(index, value);
        }

        @Override
        public void revert(NoteBuffer buffer) {
            buffer.removeLineInternal(index);
        }

        @Override
        public String name() {
            return "InsertLine";
        }
    }

    public static final class ReplaceLineCommand implements EditCommand {
        private final int index;
        private final String value;
        private String previousValue;

        public ReplaceLineCommand(int index, String value) {
            this.index = index;
            this.value = value;
        }

        @Override
        public void apply(NoteBuffer buffer) {
            previousValue = buffer.replaceLineInternal(index, value);
        }

        @Override
        public void revert(NoteBuffer buffer) {
            buffer.replaceLineInternal(index, previousValue);
        }

        @Override
        public String name() {
            return "ReplaceLine";
        }
    }

    public static final class DeleteLineCommand implements EditCommand {
        private final int index;
        private String removedValue;

        public DeleteLineCommand(int index) {
            this.index = index;
        }

        @Override
        public void apply(NoteBuffer buffer) {
            removedValue = buffer.removeLineInternal(index);
        }

        @Override
        public void revert(NoteBuffer buffer) {
            buffer.insertLineInternal(index, removedValue);
        }

        @Override
        public String name() {
            return "DeleteLine";
        }
    }

    private final NoteBuffer buffer = new NoteBuffer();
    private final Deque<EditCommand> undoStack = new ArrayDeque<>();
    private final Deque<EditCommand> redoStack = new ArrayDeque<>();
    private final List<String> auditTrail = new ArrayList<>();

    public void execute(EditCommand command) {
        command.apply(buffer);
        undoStack.push(command);
        redoStack.clear();
        auditTrail.add("EXECUTE " + command.name());
    }

    public boolean canUndo() {
        return !undoStack.isEmpty();
    }

    public boolean canRedo() {
        return !redoStack.isEmpty();
    }

    public void undo() {
        if (undoStack.isEmpty()) {
            return;
        }

        EditCommand command = undoStack.pop();
        command.revert(buffer);
        redoStack.push(command);
        auditTrail.add("UNDO " + command.name());
    }

    public void redo() {
        if (redoStack.isEmpty()) {
            return;
        }

        EditCommand command = redoStack.pop();
        command.apply(buffer);
        undoStack.push(command);
        auditTrail.add("REDO " + command.name());
    }

    public NoteBuffer getBuffer() {
        return buffer;
    }

    public List<String> historySnapshot() {
        return new ArrayList<>(auditTrail);
    }

    public int undoDepth() {
        return undoStack.size();
    }

    public int redoDepth() {
        return redoStack.size();
    }

    public void markSaved() {
        buffer.markClean();
        auditTrail.add("MARK_SAVED");
    }

    public static EditableNoteSession createDraftSession() {
        EditableNoteSession session = new EditableNoteSession();

        session.execute(new SetTitleCommand("Quarterly Planning Notes"));
        session.execute(new InsertLineCommand(0, "Open risks from previous sprint"));
        session.execute(new InsertLineCommand(1, "Hiring update for backend team"));
        session.execute(new InsertLineCommand(2, "Office relocation checklist"));
        session.execute(new ReplaceLineCommand(1, "Hiring update for backend and data teams"));
        session.undo();
        session.redo();
        session.execute(new DeleteLineCommand(0));

        return session;
    }
}