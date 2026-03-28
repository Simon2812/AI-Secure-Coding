import java.util.ArrayList;
import java.util.List;

public class SimpleGameOfLife {

    public static void step(boolean[][] grid) {
        int rows = grid.length;
        int cols = grid[0].length;

        boolean[][] next = new boolean[rows][cols];

        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                int alive = countNeighbors(grid, r, c);

                if (grid[r][c]) {
                    next[r][c] = (alive == 2 || alive == 3);
                } else {
                    next[r][c] = (alive == 3);
                }
            }
        }

        for (int r = 0; r < rows; r++) {
            System.arraycopy(next[r], 0, grid[r], 0, cols);
        }
    }

    private static int countNeighbors(boolean[][] grid, int r, int c) {
        int count = 0;

        for (int dr = -1; dr <= 1; dr++) {
            for (int dc = -1; dc <= 1; dc++) {
                if (dr == 0 && dc == 0) continue;

                int nr = r + dr;
                int nc = c + dc;

                if (nr >= 0 && nr < grid.length &&
                    nc >= 0 && nc < grid[0].length &&
                    grid[nr][nc]) {
                    count++;
                }
            }
        }

        return count;
    }

    public static List<String> render(boolean[][] grid) {
        List<String> lines = new ArrayList<>();

        for (boolean[] row : grid) {
            StringBuilder sb = new StringBuilder();
            for (boolean cell : row) {
                sb.append(cell ? "?" : " ");
            }
            lines.add(sb.toString());
        }

        return lines;
    }

    public static void print(boolean[][] grid) {
        for (String line : render(grid)) {
            System.out.println(line);
        }
        System.out.println();
    }

    public static void main(String[] args) throws InterruptedException {
        boolean[][] grid = new boolean[10][20];

        grid[4][5] = true;
        grid[5][6] = true;
        grid[6][4] = true;
        grid[6][5] = true;
        grid[6][6] = true;

        for (int i = 0; i < 15; i++) {
            print(grid);
            step(grid);
            Thread.sleep(200);
        }
    }
}