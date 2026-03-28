import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class RankingEngine {

    public interface ScoringRule {
        double score(Item item, Context context);
    }

    public static final class Item {
        private final String id;
        private final double baseScore;
        private final int popularity;
        private final int freshnessHours;

        public Item(String id, double baseScore, int popularity, int freshnessHours) {
            if (baseScore < 0) {
                throw new IllegalArgumentException("baseScore must be non-negative");
            }
            this.id = id;
            this.baseScore = baseScore;
            this.popularity = popularity;
            this.freshnessHours = freshnessHours;
        }

        public String id() {
            return id;
        }

        public double baseScore() {
            return baseScore;
        }

        public int popularity() {
            return popularity;
        }

        public int freshnessHours() {
            return freshnessHours;
        }
    }

    public static final class Context {
        private final double popularityWeight;
        private final double freshnessWeight;

        public Context(double popularityWeight, double freshnessWeight) {
            this.popularityWeight = popularityWeight;
            this.freshnessWeight = freshnessWeight;
        }

        public double popularityWeight() {
            return popularityWeight;
        }

        public double freshnessWeight() {
            return freshnessWeight;
        }
    }

    private final List<ScoringRule> rules = new ArrayList<>();

    public void addRule(ScoringRule rule) {
        rules.add(rule);
    }

    public List<ItemScore> rank(List<Item> items, Context context) {
        List<ItemScore> scored = new ArrayList<>();

        for (Item item : items) {
            double total = item.baseScore();

            for (ScoringRule rule : rules) {
                total += rule.score(item, context);
            }

            scored.add(new ItemScore(item, total));
        }

        scored.sort(Comparator.comparingDouble(ItemScore::score).reversed());
        return scored;
    }

    public static final class ItemScore {
        private final Item item;
        private final double score;

        ItemScore(Item item, double score) {
            this.item = item;
            this.score = score;
        }

        public Item item() {
            return item;
        }

        public double score() {
            return score;
        }
    }

    public static final class PopularityRule implements ScoringRule {
        @Override
        public double score(Item item, Context context) {
            return item.popularity() * context.popularityWeight();
        }
    }

    public static final class FreshnessRule implements ScoringRule {
        @Override
        public double score(Item item, Context context) {
            int age = item.freshnessHours();
            if (age <= 0) return 0;
            return (1.0 / age) * context.freshnessWeight();
        }
    }

    public static final class CapRule implements ScoringRule {
        private final double maxBoost;

        public CapRule(double maxBoost) {
            this.maxBoost = maxBoost;
        }

        @Override
        public double score(Item item, Context context) {
            double raw = item.popularity() * 0.1;
            return Math.min(raw, maxBoost);
        }
    }
}
