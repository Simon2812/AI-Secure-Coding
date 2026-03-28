import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

public class DashboardFlowLayout {

    public interface Widget {
        String id();
        int preferredWidth();
        int preferredHeight();
        int minWidth();
        boolean stretchable();
    }

    public static final class StatCard implements Widget {
        private final String id;
        private final String title;
        private final int preferredWidth;
        private final int preferredHeight;
        private final boolean stretchable;

        public StatCard(String id, String title, int preferredWidth, int preferredHeight, boolean stretchable) {
            if (preferredWidth <= 0 || preferredHeight <= 0) {
                throw new IllegalArgumentException("Invalid widget size");
            }
            this.id = Objects.requireNonNull(id);
            this.title = Objects.requireNonNull(title);
            this.preferredWidth = preferredWidth;
            this.preferredHeight = preferredHeight;
            this.stretchable = stretchable;
        }

        @Override
        public String id() {
            return id;
        }

        public String title() {
            return title;
        }

        @Override
        public int preferredWidth() {
            return preferredWidth;
        }

        @Override
        public int preferredHeight() {
            return preferredHeight;
        }

        @Override
        public int minWidth() {
            return Math.max(120, preferredWidth / 2);
        }

        @Override
        public boolean stretchable() {
            return stretchable;
        }
    }

    public static final class Spacer implements Widget {
        private final String id;
        private final int width;

        public Spacer(String id, int width) {
            if (width <= 0) {
                throw new IllegalArgumentException("Spacer width must be positive");
            }
            this.id = Objects.requireNonNull(id);
            this.width = width;
        }

        @Override
        public String id() {
            return id;
        }

        @Override
        public int preferredWidth() {
            return width;
        }

        @Override
        public int preferredHeight() {
            return 1;
        }

        @Override
        public int minWidth() {
            return width;
        }

        @Override
        public boolean stretchable() {
            return false;
        }
    }

    public static final class Placement {
        private final String widgetId;
        private final int x;
        private final int y;
        private final int width;
        private final int height;

        public Placement(String widgetId, int x, int y, int width, int height) {
            this.widgetId = widgetId;
            this.x = x;
            this.y = y;
            this.width = width;
            this.height = height;
        }

        public String widgetId() {
            return widgetId;
        }

        public int x() {
            return x;
        }

        public int y() {
            return y;
        }

        public int width() {
            return width;
        }

        public int height() {
            return height;
        }
    }

    public static final class Layout {
        private final int canvasWidth;
        private final int totalHeight;
        private final List<Placement> placements;

        Layout(int canvasWidth, int totalHeight, List<Placement> placements) {
            this.canvasWidth = canvasWidth;
            this.totalHeight = totalHeight;
            this.placements = placements;
        }

        public int canvasWidth() {
            return canvasWidth;
        }

        public int totalHeight() {
            return totalHeight;
        }

        public List<Placement> placements() {
            return Collections.unmodifiableList(placements);
        }

        public Placement find(String widgetId) {
            for (Placement placement : placements) {
                if (placement.widgetId().equals(widgetId)) {
                    return placement;
                }
            }
            return null;
        }
    }

    private final List<Widget> widgets = new ArrayList<>();
    private int horizontalGap = 12;
    private int verticalGap = 12;
    private int paddingLeft = 16;
    private int paddingTop = 16;
    private int paddingRight = 16;
    private int paddingBottom = 16;

    public void add(Widget widget) {
        widgets.add(Objects.requireNonNull(widget));
    }

    public void setGaps(int horizontalGap, int verticalGap) {
        if (horizontalGap < 0 || verticalGap < 0) {
            throw new IllegalArgumentException("Gaps must not be negative");
        }
        this.horizontalGap = horizontalGap;
        this.verticalGap = verticalGap;
    }

    public void setPadding(int left, int top, int right, int bottom) {
        if (left < 0 || top < 0 || right < 0 || bottom < 0) {
            throw new IllegalArgumentException("Padding must not be negative");
        }
        this.paddingLeft = left;
        this.paddingTop = top;
        this.paddingRight = right;
        this.paddingBottom = bottom;
    }

    public Layout arrange(int availableWidth) {
        if (availableWidth <= paddingLeft + paddingRight) {
            throw new IllegalArgumentException("Available width is too small");
        }

        List<Placement> output = new ArrayList<>();
        List<Widget> row = new ArrayList<>();

        int innerWidth = availableWidth - paddingLeft - paddingRight;
        int rowUsedWidth = 0;
        int cursorY = paddingTop;

        for (Widget widget : widgets) {
            int required = row.isEmpty()
                    ? widget.preferredWidth()
                    : rowUsedWidth + horizontalGap + widget.preferredWidth();

            if (!row.isEmpty() && required > innerWidth) {
                cursorY = placeRow(row, innerWidth, cursorY, output);
                row.clear();
                rowUsedWidth = 0;
            }

            row.add(widget);
            rowUsedWidth = row.isEmpty()
                    ? widget.preferredWidth()
                    : rowUsedWidth == 0
                        ? widget.preferredWidth()
                        : rowUsedWidth + horizontalGap + widget.preferredWidth();
        }

        if (!row.isEmpty()) {
            cursorY = placeRow(row, innerWidth, cursorY, output);
        }

        return new Layout(availableWidth, cursorY + paddingBottom, output);
    }

    private int placeRow(List<Widget> row, int innerWidth, int cursorY, List<Placement> output) {
        int preferredTotal = 0;
        int tallest = 0;
        int stretchCount = 0;

        for (Widget widget : row) {
            preferredTotal += widget.preferredWidth();
            tallest = Math.max(tallest, widget.preferredHeight());
            if (widget.stretchable()) {
                stretchCount++;
            }
        }

        preferredTotal += horizontalGap * Math.max(0, row.size() - 1);
        int extra = Math.max(0, innerWidth - preferredTotal);

        int cursorX = paddingLeft;
        int remainder = extra;

        for (int i = 0; i < row.size(); i++) {
            Widget widget = row.get(i);

            int width = widget.preferredWidth();
            if (stretchCount > 0 && widget.stretchable()) {
                int share = remainder / stretchCount;
                width += share;
                remainder -= share;
                stretchCount--;
            }

            if (width < widget.minWidth()) {
                width = widget.minWidth();
            }

            output.add(new Placement(
                    widget.id(),
                    cursorX,
                    cursorY,
                    width,
                    widget.preferredHeight()
            ));

            cursorX += width;
            if (i < row.size() - 1) {
                cursorX += horizontalGap;
            }
        }

        return cursorY + tallest + verticalGap;
    }
}