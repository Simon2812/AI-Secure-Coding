import java.util.*;

public class SpatialIndex {

    public static final class Point {
        public final double x;
        public final double y;

        public Point(double x, double y) {
            this.x = x;
            this.y = y;
        }
    }

    public static final class Entity {
        public final String id;
        public final Point position;
        public final String type;

        public Entity(String id, Point position, String type) {
            this.id = id;
            this.position = position;
            this.type = type;
        }
    }

    private static final class CellKey {
        final int gx;
        final int gy;

        CellKey(int gx, int gy) {
            this.gx = gx;
            this.gy = gy;
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof CellKey k)) return false;
            return k.gx == gx && k.gy == gy;
        }

        @Override
        public int hashCode() {
            return gx * 31 + gy;
        }
    }

    private final Map<CellKey, List<Entity>> grid = new HashMap<>();
    private final double cellSize;

    public SpatialIndex(double cellSize) {
        if (cellSize <= 0) {
            throw new IllegalArgumentException("cellSize must be positive");
        }
        this.cellSize = cellSize;
    }

    public void insert(Entity entity) {
        CellKey key = keyFor(entity.position);
        grid.computeIfAbsent(key, k -> new ArrayList<>()).add(entity);
    }

    public boolean remove(String entityId) {
        for (List<Entity> bucket : grid.values()) {
            Iterator<Entity> it = bucket.iterator();
            while (it.hasNext()) {
                if (it.next().id.equals(entityId)) {
                    it.remove();
                    return true;
                }
            }
        }
        return false;
    }

    public List<Entity> queryRadius(Point center, double radius) {
        List<Entity> result = new ArrayList<>();

        int minX = toGrid(center.x - radius);
        int maxX = toGrid(center.x + radius);
        int minY = toGrid(center.y - radius);
        int maxY = toGrid(center.y + radius);

        double r2 = radius * radius;

        for (int gx = minX; gx <= maxX; gx++) {
            for (int gy = minY; gy <= maxY; gy++) {
                List<Entity> bucket = grid.get(new CellKey(gx, gy));
                if (bucket == null) continue;

                for (Entity e : bucket) {
                    if (distanceSquared(center, e.position) <= r2) {
                        result.add(e);
                    }
                }
            }
        }

        return result;
    }

    public List<Entity> queryBox(Point min, Point max) {
        List<Entity> result = new ArrayList<>();

        int minX = toGrid(min.x);
        int maxX = toGrid(max.x);
        int minY = toGrid(min.y);
        int maxY = toGrid(max.y);

        for (int gx = minX; gx <= maxX; gx++) {
            for (int gy = minY; gy <= maxY; gy++) {
                List<Entity> bucket = grid.get(new CellKey(gx, gy));
                if (bucket == null) continue;

                for (Entity e : bucket) {
                    if (insideBox(e.position, min, max)) {
                        result.add(e);
                    }
                }
            }
        }

        return result;
    }

    private CellKey keyFor(Point p) {
        return new CellKey(toGrid(p.x), toGrid(p.y));
    }

    private int toGrid(double value) {
        return (int) Math.floor(value / cellSize);
    }

    private double distanceSquared(Point a, Point b) {
        double dx = a.x - b.x;
        double dy = a.y - b.y;
        return dx * dx + dy * dy;
    }

    private boolean insideBox(Point p, Point min, Point max) {
        return p.x >= min.x && p.x <= max.x &&
               p.y >= min.y && p.y <= max.y;
    }

    public int bucketCount() {
        return grid.size();
    }

    public int totalEntities() {
        int total = 0;
        for (List<Entity> bucket : grid.values()) {
            total += bucket.size();
        }
        return total;
    }

    public static SpatialIndex sampleWorld() {
        SpatialIndex index = new SpatialIndex(10.0);

        index.insert(new Entity("E1", new Point(12.5, 7.2), "vehicle"));
        index.insert(new Entity("E2", new Point(18.1, 9.4), "vehicle"));
        index.insert(new Entity("E3", new Point(35.0, 40.0), "building"));
        index.insert(new Entity("E4", new Point(11.9, 6.8), "pedestrian"));
        index.insert(new Entity("E5", new Point(50.0, 10.0), "vehicle"));

        return index;
    }
}