import java.time.DayOfWeek;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class ShiftPlanner {

    public static final class Employee {
        private final String id;
        private final String name;
        private final Role role;
        private final Availability availability;

        public Employee(String id, String name, Role role, Availability availability) {
            this.id = Objects.requireNonNull(id);
            this.name = Objects.requireNonNull(name);
            this.role = Objects.requireNonNull(role);
            this.availability = Objects.requireNonNull(availability);
        }

        public String getId() {
            return id;
        }

        public String getName() {
            return name;
        }

        public Role getRole() {
            return role;
        }

        public Availability getAvailability() {
            return availability;
        }
    }

    public enum Role {
        CASHIER,
        SUPERVISOR,
        STOCKER,
        CLEANER
    }

    public static final class TimeRange {
        private final LocalTime start;
        private final LocalTime end;

        public TimeRange(LocalTime start, LocalTime end) {
            this.start = Objects.requireNonNull(start);
            this.end = Objects.requireNonNull(end);
            if (!end.isAfter(start)) {
                throw new IllegalArgumentException("End must be after start");
            }
        }

        public boolean contains(TimeRange other) {
            return !other.start.isBefore(start) && !other.end.isAfter(end);
        }

        public LocalTime getStart() {
            return start;
        }

        public LocalTime getEnd() {
            return end;
        }

        @Override
        public String toString() {
            return start + "-" + end;
        }
    }

    public static final class Availability {
        private final Map<DayOfWeek, List<TimeRange>> slots;

        public Availability(Map<DayOfWeek, List<TimeRange>> slots) {
            this.slots = new EnumMap<>(DayOfWeek.class);
            for (DayOfWeek d : DayOfWeek.values()) {
                this.slots.put(d, new ArrayList<>());
            }
            for (Map.Entry<DayOfWeek, List<TimeRange>> e : slots.entrySet()) {
                this.slots.get(e.getKey()).addAll(e.getValue());
            }
        }

        public boolean isAvailable(DayOfWeek day, TimeRange shiftRange) {
            List<TimeRange> daySlots = slots.get(day);
            for (TimeRange r : daySlots) {
                if (r.contains(shiftRange)) {
                    return true;
                }
            }
            return false;
        }
    }

    public static final class Shift {
        private final String label;
        private final Role requiredRole;
        private final TimeRange range;

        public Shift(String label, Role requiredRole, TimeRange range) {
            this.label = Objects.requireNonNull(label);
            this.requiredRole = Objects.requireNonNull(requiredRole);
            this.range = Objects.requireNonNull(range);
        }

        public String getLabel() {
            return label;
        }

        public Role getRequiredRole() {
            return requiredRole;
        }

        public TimeRange getRange() {
            return range;
        }
    }

    public static final class Assignment {
        private final LocalDate date;
        private final Shift shift;
        private final Employee employee;

        public Assignment(LocalDate date, Shift shift, Employee employee) {
            this.date = date;
            this.shift = shift;
            this.employee = employee;
        }

        public String format() {
            return date + " | " + shift.getLabel() + " | " + shift.getRange() +
                    " | " + shift.getRequiredRole() + " | " + employee.getName();
        }
    }

    public static final class WeeklyPlan {
        private final List<Assignment> assignments;

        public WeeklyPlan(List<Assignment> assignments) {
            this.assignments = new ArrayList<>(assignments);
        }

        public List<Assignment> getAssignments() {
            return Collections.unmodifiableList(assignments);
        }

        public String asText() {
            StringBuilder sb = new StringBuilder();
            sb.append("Weekly Shift Plan").append('\n');
            sb.append("------------------").append('\n');
            for (Assignment a : assignments) {
                sb.append(a.format()).append('\n');
            }
            return sb.toString();
        }
    }

    public WeeklyPlan generatePlan(
            LocalDate startDate,
            List<Shift> shifts,
            List<Employee> employees,
            int days
    ) {
        List<Assignment> result = new ArrayList<>();
        Map<Role, Integer> rotationIndex = new EnumMap<>(Role.class);
        for (Role r : Role.values()) {
            rotationIndex.put(r, 0);
        }

        for (int i = 0; i < days; i++) {
            LocalDate current = startDate.plusDays(i);
            DayOfWeek day = current.getDayOfWeek();

            for (Shift shift : shifts) {
                List<Employee> eligible = collectEligibleEmployees(employees, shift, day);

                if (eligible.isEmpty()) {
                    continue;
                }

                int index = rotationIndex.get(shift.getRequiredRole());
                Employee chosen = eligible.get(index % eligible.size());
                rotationIndex.put(shift.getRequiredRole(), index + 1);

                result.add(new Assignment(current, shift, chosen));
            }
        }

        return new WeeklyPlan(result);
    }

    private List<Employee> collectEligibleEmployees(
            List<Employee> employees,
            Shift shift,
            DayOfWeek day
    ) {
        List<Employee> eligible = new ArrayList<>();
        for (Employee e : employees) {
            if (e.getRole() == shift.getRequiredRole() &&
                e.getAvailability().isAvailable(day, shift.getRange())) {
                eligible.add(e);
            }
        }
        return eligible;
    }

    public static void main(String[] args) {
        TimeRange morning = new TimeRange(LocalTime.of(8, 0), LocalTime.of(14, 0));
        TimeRange evening = new TimeRange(LocalTime.of(14, 0), LocalTime.of(20, 0));

        Shift cashierMorning = new Shift("Morning Cashier", Role.CASHIER, morning);
        Shift cashierEvening = new Shift("Evening Cashier", Role.CASHIER, evening);
        Shift supervisorDay = new Shift("Day Supervisor", Role.SUPERVISOR, morning);

        Map<DayOfWeek, List<TimeRange>> fullWeek = new EnumMap<>(DayOfWeek.class);
        for (DayOfWeek d : DayOfWeek.values()) {
            fullWeek.put(d, List.of(
                    new TimeRange(LocalTime.of(7, 0), LocalTime.of(22, 0))
            ));
        }

        Map<DayOfWeek, List<TimeRange>> eveningsOnly = new EnumMap<>(DayOfWeek.class);
        for (DayOfWeek d : DayOfWeek.values()) {
            eveningsOnly.put(d, List.of(
                    new TimeRange(LocalTime.of(13, 0), LocalTime.of(22, 0))
            ));
        }

        Employee e1 = new Employee("E-01", "Lena", Role.CASHIER, new Availability(fullWeek));
        Employee e2 = new Employee("E-02", "Omer", Role.CASHIER, new Availability(eveningsOnly));
        Employee e3 = new Employee("E-03", "David", Role.SUPERVISOR, new Availability(fullWeek));

        List<Employee> employees = List.of(e1, e2, e3);
        List<Shift> shifts = List.of(cashierMorning, cashierEvening, supervisorDay);

        ShiftPlanner planner = new ShiftPlanner();
        WeeklyPlan plan = planner.generatePlan(
                LocalDate.of(2026, 3, 30),
                shifts,
                employees,
                5
        );

        System.out.println(plan.asText());
    }
}