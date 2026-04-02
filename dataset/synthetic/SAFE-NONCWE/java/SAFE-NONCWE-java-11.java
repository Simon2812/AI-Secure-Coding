import java.util.ArrayList;
import java.util.List;

public class OrgHierarchyEngine {

    abstract static class Node {
        protected final String name;

        Node(String name) {
            this.name = name;
        }

        abstract int totalPeople();
        abstract int depth();
        abstract void print(String indent);
    }

    static class Employee extends Node {
        private final int workloadScore;

        Employee(String name, int workloadScore) {
            super(name);
            this.workloadScore = workloadScore;
        }

        @Override
        int totalPeople() {
            return 1;
        }

        @Override
        int depth() {
            return 1;
        }

        @Override
        void print(String indent) {
            System.out.println(indent + "- " + name + " (load=" + workloadScore + ")");
        }

        public int getWorkloadScore() {
            return workloadScore;
        }
    }

    static class Department extends Node {
        private final List<Node> children = new ArrayList<>();

        Department(String name) {
            super(name);
        }

        void add(Node node) {
            children.add(node);
        }

        @Override
        int totalPeople() {
            int sum = 0;
            for (Node n : children) {
                sum += n.totalPeople();
            }
            return sum;
        }

        @Override
        int depth() {
            int max = 0;
            for (Node n : children) {
                max = Math.max(max, n.depth());
            }
            return max + 1;
        }

        @Override
        void print(String indent) {
            System.out.println(indent + "[Dept] " + name);
            for (Node n : children) {
                n.print(indent + "  ");
            }
        }

        int aggregateLoad() {
            int total = 0;
            for (Node n : children) {
                if (n instanceof Employee e) {
                    total += e.getWorkloadScore();
                } else if (n instanceof Department d) {
                    total += d.aggregateLoad();
                }
            }
            return total;
        }

        List<Employee> flattenEmployees() {
            List<Employee> result = new ArrayList<>();
            collect(this, result);
            return result;
        }

        private void collect(Node node, List<Employee> out) {
            if (node instanceof Employee e) {
                out.add(e);
                return;
            }

            Department d = (Department) node;
            for (Node child : d.children) {
                collect(child, out);
            }
        }
    }

    public static void main(String[] args) {
        Department root = new Department("Company");

        Department engineering = new Department("Engineering");
        Department backend = new Department("Backend");
        Department frontend = new Department("Frontend");

        backend.add(new Employee("Alex", 7));
        backend.add(new Employee("Dana", 5));

        frontend.add(new Employee("Maya", 6));
        frontend.add(new Employee("Noam", 4));

        engineering.add(backend);
        engineering.add(frontend);

        Department hr = new Department("HR");
        hr.add(new Employee("Lior", 3));

        root.add(engineering);
        root.add(hr);

        root.print("");

        System.out.println("\nTotal people: " + root.totalPeople());
        System.out.println("Hierarchy depth: " + root.depth());
        System.out.println("Total workload: " + root.aggregateLoad());

        System.out.println("\nEmployees flattened:");
        for (Employee e : root.flattenEmployees()) {
            System.out.println(" * " + e.name);
        }
    }
}