import java.util.*;

public final class RouteExplorer {

    private RouteExplorer() {
    }

    public static Map<String, List<String>> shortestPaths(
            Map<String, List<String>> graph,
            String source
    ) {
        Map<String, String> parent = new HashMap<>();
        Map<String, Integer> distance = new HashMap<>();

        Deque<String> queue = new ArrayDeque<>();

        queue.add(source);
        distance.put(source, 0);

        while (!queue.isEmpty()) {
            String current = queue.removeFirst();

            List<String> neighbors = graph.getOrDefault(current, Collections.emptyList());
            for (String next : neighbors) {
                if (!distance.containsKey(next)) {
                    distance.put(next, distance.get(current) + 1);
                    parent.put(next, current);
                    queue.addLast(next);
                }
            }
        }

        Map<String, List<String>> paths = new HashMap<>();
        for (String node : distance.keySet()) {
            paths.put(node, buildPath(node, parent));
        }

        return paths;
    }

    private static List<String> buildPath(String target, Map<String, String> parent) {
        LinkedList<String> path = new LinkedList<>();
        String current = target;

        while (current != null) {
            path.addFirst(current);
            current = parent.get(current);
        }

        return path;
    }

    public static Set<String> reachableWithin(
            Map<String, List<String>> graph,
            String source,
            int maxSteps
    ) {
        Set<String> visited = new HashSet<>();
        Map<String, Integer> depth = new HashMap<>();

        Deque<String> queue = new ArrayDeque<>();
        queue.add(source);
        depth.put(source, 0);

        while (!queue.isEmpty()) {
            String node = queue.removeFirst();

            int d = depth.get(node);
            if (d > maxSteps) {
                continue;
            }

            visited.add(node);

            for (String next : graph.getOrDefault(node, Collections.emptyList())) {
                if (!depth.containsKey(next)) {
                    depth.put(next, d + 1);
                    queue.addLast(next);
                }
            }
        }

        return visited;
    }

    public static Map<Integer, List<String>> groupByDistance(
            Map<String, List<String>> graph,
            String source
    ) {
        Map<Integer, List<String>> layers = new HashMap<>();
        Map<String, Integer> distance = new HashMap<>();

        Deque<String> queue = new ArrayDeque<>();
        queue.add(source);
        distance.put(source, 0);

        while (!queue.isEmpty()) {
            String node = queue.removeFirst();
            int d = distance.get(node);

            layers.computeIfAbsent(d, k -> new ArrayList<>()).add(node);

            for (String next : graph.getOrDefault(node, Collections.emptyList())) {
                if (!distance.containsKey(next)) {
                    distance.put(next, d + 1);
                    queue.addLast(next);
                }
            }
        }

        return layers;
    }
}