import java.util.ArrayList;
import java.util.List;

public class PlainTextDiff {

    public static List<String> diff(List<String> left, List<String> right) {
        int n = left.size();
        int m = right.size();

        int[][] dp = new int[n + 1][m + 1];

        for (int i = n - 1; i >= 0; i--) {
            for (int j = m - 1; j >= 0; j--) {
                if (left.get(i).equals(right.get(j))) {
                    dp[i][j] = 1 + dp[i + 1][j + 1];
                } else {
                    dp[i][j] = Math.max(dp[i + 1][j], dp[i][j + 1]);
                }
            }
        }

        List<String> result = new ArrayList<>();
        int i = 0, j = 0;

        while (i < n && j < m) {
            if (left.get(i).equals(right.get(j))) {
                result.add("  " + left.get(i));
                i++;
                j++;
            } else if (dp[i + 1][j] >= dp[i][j + 1]) {
                result.add("- " + left.get(i));
                i++;
            } else {
                result.add("+ " + right.get(j));
                j++;
            }
        }

        while (i < n) {
            result.add("- " + left.get(i));
            i++;
        }

        while (j < m) {
            result.add("+ " + right.get(j));
            j++;
        }

        return result;
    }

    public static void print(List<String> diff) {
        for (String line : diff) {
            System.out.println(line);
        }
    }

    public static void main(String[] args) {
        List<String> v1 = List.of(
                "class User {",
                "  String name;",
                "  int age;",
                "}"
        );

        List<String> v2 = List.of(
                "class User {",
                "  String name;",
                "  int age;",
                "  String email;",
                "}"
        );

        List<String> result = diff(v1, v2);
        print(result);
    }
}