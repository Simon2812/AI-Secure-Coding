import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Collections;
import java.util.DoubleSummaryStatistics;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

public class GradebookAnalyzer {

    public static final class Student {
        private final String id;
        private final String name;

        public Student(String id, String name) {
            this.id = Objects.requireNonNull(id);
            this.name = Objects.requireNonNull(name);
        }

        public String getId() {
            return id;
        }

        public String getName() {
            return name;
        }
    }

    public static final class Course {
        private final String code;
        private final String title;

        public Course(String code, String title) {
            this.code = Objects.requireNonNull(code);
            this.title = Objects.requireNonNull(title);
        }

        public String getCode() {
            return code;
        }

        public String getTitle() {
            return title;
        }
    }

    public enum AssessmentType {
        EXAM,
        QUIZ,
        HOMEWORK,
        PROJECT
    }

    public static final class GradeEntry {
        private final Student student;
        private final Course course;
        private final AssessmentType type;
        private final double score;
        private final LocalDate date;

        public GradeEntry(Student student, Course course, AssessmentType type, double score, LocalDate date) {
            this.student = Objects.requireNonNull(student);
            this.course = Objects.requireNonNull(course);
            this.type = Objects.requireNonNull(type);
            this.date = Objects.requireNonNull(date);

            if (score < 0.0 || score > 100.0) {
                throw new IllegalArgumentException("Score must be between 0 and 100");
            }
            this.score = score;
        }

        public Student getStudent() {
            return student;
        }

        public Course getCourse() {
            return course;
        }

        public AssessmentType getType() {
            return type;
        }

        public double getScore() {
            return score;
        }

        public LocalDate getDate() {
            return date;
        }
    }

    public static final class StudentReport {
        private final Student student;
        private final double average;
        private final double min;
        private final double max;
        private final String performanceLabel;

        public StudentReport(Student student, double average, double min, double max, String performanceLabel) {
            this.student = student;
            this.average = average;
            this.min = min;
            this.max = max;
            this.performanceLabel = performanceLabel;
        }

        public String format() {
            return student.getName() +
                    " | avg=" + round(average) +
                    " | min=" + round(min) +
                    " | max=" + round(max) +
                    " | " + performanceLabel;
        }

        private String round(double v) {
            return String.format("%.2f", v);
        }
    }

    public static final class CourseReport {
        private final Course course;
        private final double average;
        private final int count;

        public CourseReport(Course course, double average, int count) {
            this.course = course;
            this.average = average;
            this.count = count;
        }

        public String format() {
            return course.getCode() +
                    " (" + course.getTitle() + ")" +
                    " | avg=" + String.format("%.2f", average) +
                    " | entries=" + count;
        }
    }

    public static final class GradebookSummary {
        private final List<StudentReport> studentReports;
        private final List<CourseReport> courseReports;

        public GradebookSummary(List<StudentReport> studentReports, List<CourseReport> courseReports) {
            this.studentReports = new ArrayList<>(studentReports);
            this.courseReports = new ArrayList<>(courseReports);
        }

        public String render() {
            StringBuilder sb = new StringBuilder();

            sb.append("Student Performance").append('\n');
            sb.append("-------------------").append('\n');
            for (StudentReport r : studentReports) {
                sb.append(r.format()).append('\n');
            }

            sb.append('\n');
            sb.append("Course Overview").append('\n');
            sb.append("----------------").append('\n');
            for (CourseReport r : courseReports) {
                sb.append(r.format()).append('\n');
            }

            return sb.toString();
        }
    }

    public GradebookSummary analyze(List<GradeEntry> entries) {
        Map<String, List<GradeEntry>> byStudent = new HashMap<>();
        Map<String, List<GradeEntry>> byCourse = new HashMap<>();

        for (GradeEntry entry : entries) {
            byStudent
                    .computeIfAbsent(entry.getStudent().getId(), k -> new ArrayList<>())
                    .add(entry);

            byCourse
                    .computeIfAbsent(entry.getCourse().getCode(), k -> new ArrayList<>())
                    .add(entry);
        }

        List<StudentReport> studentReports = new ArrayList<>();
        for (List<GradeEntry> studentEntries : byStudent.values()) {
            DoubleSummaryStatistics stats = studentEntries.stream()
                    .mapToDouble(GradeEntry::getScore)
                    .summaryStatistics();

            Student student = studentEntries.get(0).getStudent();

            studentReports.add(new StudentReport(
                    student,
                    stats.getAverage(),
                    stats.getMin(),
                    stats.getMax(),
                    classify(stats.getAverage())
            ));
        }

        List<CourseReport> courseReports = new ArrayList<>();
        for (List<GradeEntry> courseEntries : byCourse.values()) {
            DoubleSummaryStatistics stats = courseEntries.stream()
                    .mapToDouble(GradeEntry::getScore)
                    .summaryStatistics();

            Course course = courseEntries.get(0).getCourse();

            courseReports.add(new CourseReport(
                    course,
                    stats.getAverage(),
                    (int) stats.getCount()
            ));
        }

        studentReports.sort((a, b) -> Double.compare(b.average, a.average));
        courseReports.sort((a, b) -> Double.compare(b.average, a.average));

        return new GradebookSummary(studentReports, courseReports);
    }

    private String classify(double avg) {
        if (avg >= 90) return "Excellent";
        if (avg >= 75) return "Good";
        if (avg >= 60) return "Satisfactory";
        return "Needs Improvement";
    }

    public static void main(String[] args) {
        Student s1 = new Student("S-01", "Maya");
        Student s2 = new Student("S-02", "Noam");
        Student s3 = new Student("S-03", "Eli");

        Course c1 = new Course("CS101", "Intro to Programming");
        Course c2 = new Course("MATH201", "Linear Algebra");

        List<GradeEntry> entries = List.of(
                new GradeEntry(s1, c1, AssessmentType.EXAM, 88, LocalDate.of(2026, 2, 10)),
                new GradeEntry(s1, c1, AssessmentType.HOMEWORK, 92, LocalDate.of(2026, 2, 5)),
                new GradeEntry(s1, c2, AssessmentType.PROJECT, 95, LocalDate.of(2026, 3, 1)),

                new GradeEntry(s2, c1, AssessmentType.EXAM, 70, LocalDate.of(2026, 2, 10)),
                new GradeEntry(s2, c2, AssessmentType.EXAM, 65, LocalDate.of(2026, 2, 20)),

                new GradeEntry(s3, c1, AssessmentType.QUIZ, 78, LocalDate.of(2026, 2, 3)),
                new GradeEntry(s3, c2, AssessmentType.PROJECT, 82, LocalDate.of(2026, 3, 2))
        );

        GradebookAnalyzer analyzer = new GradebookAnalyzer();
        GradebookSummary summary = analyzer.analyze(entries);

        System.out.println(summary.render());
    }
}