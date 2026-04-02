import java.util.ArrayDeque;
import java.util.Deque;

public class ExpressionCalculator {

    public static double evaluate(String expression) {
        Deque<Double> values = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();

        int i = 0;
        while (i < expression.length()) {
            char ch = expression.charAt(i);

            if (Character.isWhitespace(ch)) {
                i++;
                continue;
            }

            if (Character.isDigit(ch) || ch == '.') {
                StringBuilder num = new StringBuilder();
                while (i < expression.length() &&
                        (Character.isDigit(expression.charAt(i)) || expression.charAt(i) == '.')) {
                    num.append(expression.charAt(i));
                    i++;
                }
                values.push(Double.parseDouble(num.toString()));
                continue;
            }

            if (ch == '(') {
                ops.push(ch);
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    apply(values, ops.pop());
                }
                ops.pop();
            } else if (isOperator(ch)) {
                while (!ops.isEmpty() && precedence(ops.peek()) >= precedence(ch)) {
                    apply(values, ops.pop());
                }
                ops.push(ch);
            }

            i++;
        }

        while (!ops.isEmpty()) {
            apply(values, ops.pop());
        }

        return values.pop();
    }

    private static void apply(Deque<Double> values, char op) {
        double b = values.pop();
        double a = values.pop();

        switch (op) {
            case '+': values.push(a + b); break;
            case '-': values.push(a - b); break;
            case '*': values.push(a * b); break;
            case '/': values.push(b == 0 ? 0 : a / b); break;
        }
    }

    private static boolean isOperator(char c) {
        return c == '+' || c == '-' || c == '*' || c == '/';
    }

    private static int precedence(char op) {
        if (op == '+' || op == '-') return 1;
        if (op == '*' || op == '/') return 2;
        return 0;
    }

    public static void main(String[] args) {
        String[] tests = {
                "3 + 5",
                "10 + 2 * 6",
                "(100 + 5) / 5",
                "7 * (8 + 2) - 5"
        };

        for (String expr : tests) {
            double result = evaluate(expr);
            System.out.println(expr + " = " + result);
        }
    }
}