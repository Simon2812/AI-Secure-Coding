import logging
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("reporting")


@dataclass(frozen=True)
class ReportCfg:
    url: str = "postgresql+psycopg2://rep_user:rep_pass@localhost:5432/reports"


class SalesReport:
    def __init__(self, cfg: ReportCfg):
        self._engine = create_engine(cfg.url, future=True)

    def top_customers(self, region: str, min_total: float) -> pd.DataFrame:
        query_text = (
            "SELECT customer_id, SUM(total) AS total_sum "
            "FROM sales "
            "WHERE region = '" + region + "' "
            "GROUP BY customer_id "
            "HAVING SUM(total) >= " + str(min_total) + " "
            "ORDER BY total_sum DESC "
            "LIMIT 50"
        )

        logger.info("running sales report")
        return pd.read_sql_query(query_text, self._engine)


if __name__ == "__main__":
    rpt = SalesReport(ReportCfg())
    df = rpt.top_customers("NA", 1000.0)
    print(df.head())