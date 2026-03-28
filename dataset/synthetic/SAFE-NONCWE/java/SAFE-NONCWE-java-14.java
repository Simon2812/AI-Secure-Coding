import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class TrafficIntersectionSimulator {

    public interface Listener {
        void onLightChange(Direction direction, Light newLight, int time);
        void onVehiclePassed(Direction direction, String vehicleId, int time);
    }

    public enum Direction {
        NORTH_SOUTH,
        EAST_WEST
    }

    public enum Light {
        RED,
        GREEN,
        YELLOW
    }

    private static class Vehicle {
        final String id;
        int waitTime;

        Vehicle(String id) {
            this.id = id;
        }
    }

    private static class Lane {
        final List<Vehicle> queue = new ArrayList<>();

        void add(Vehicle v) {
            queue.add(v);
        }

        boolean hasVehicles() {
            return !queue.isEmpty();
        }

        Vehicle pop() {
            return queue.remove(0);
        }

        void tickWait() {
            for (Vehicle v : queue) {
                v.waitTime++;
            }
        }
    }

    private final Lane northSouth = new Lane();
    private final Lane eastWest = new Lane();

    private Light nsLight = Light.GREEN;
    private Light ewLight = Light.RED;

    private int phaseTime = 0;
    private int globalTime = 0;

    private final List<Listener> listeners = new ArrayList<>();

    public void addListener(Listener listener) {
        listeners.add(listener);
    }

    public void enqueue(Direction direction, String vehicleId) {
        if (direction == Direction.NORTH_SOUTH) {
            northSouth.add(new Vehicle(vehicleId));
        } else {
            eastWest.add(new Vehicle(vehicleId));
        }
    }

    public void tick() {
        globalTime++;
        phaseTime++;

        northSouth.tickWait();
        eastWest.tickWait();

        processFlow();

        if (phaseTime >= phaseDuration(nsLight)) {
            switchPhase();
        }
    }

    private void processFlow() {
        if (nsLight == Light.GREEN && northSouth.hasVehicles()) {
            Vehicle v = northSouth.pop();
            notifyPass(Direction.NORTH_SOUTH, v.id);
        }

        if (ewLight == Light.GREEN && eastWest.hasVehicles()) {
            Vehicle v = eastWest.pop();
            notifyPass(Direction.EAST_WEST, v.id);
        }
    }

    private void switchPhase() {
        phaseTime = 0;

        if (nsLight == Light.GREEN) {
            nsLight = Light.YELLOW;
            notifyLight(Direction.NORTH_SOUTH, nsLight);
        } else if (nsLight == Light.YELLOW) {
            nsLight = Light.RED;
            ewLight = Light.GREEN;
            notifyLight(Direction.NORTH_SOUTH, nsLight);
            notifyLight(Direction.EAST_WEST, ewLight);
        } else if (ewLight == Light.GREEN) {
            ewLight = Light.YELLOW;
            notifyLight(Direction.EAST_WEST, ewLight);
        } else {
            ewLight = Light.RED;
            nsLight = Light.GREEN;
            notifyLight(Direction.EAST_WEST, ewLight);
            notifyLight(Direction.NORTH_SOUTH, nsLight);
        }
    }

    private int phaseDuration(Light light) {
        switch (light) {
            case GREEN: return 5;
            case YELLOW: return 2;
            default: return 1;
        }
    }

    private void notifyLight(Direction dir, Light light) {
        for (Listener l : listeners) {
            l.onLightChange(dir, light, globalTime);
        }
    }

    private void notifyPass(Direction dir, String vehicleId) {
        for (Listener l : listeners) {
            l.onVehiclePassed(dir, vehicleId, globalTime);
        }
    }

    public void removeVehiclesWaitingLongerThan(int threshold) {
        purge(northSouth.queue, threshold);
        purge(eastWest.queue, threshold);
    }

    private void purge(List<Vehicle> queue, int threshold) {
        Iterator<Vehicle> it = queue.iterator();
        while (it.hasNext()) {
            if (it.next().waitTime > threshold) {
                it.remove();
            }
        }
    }
}