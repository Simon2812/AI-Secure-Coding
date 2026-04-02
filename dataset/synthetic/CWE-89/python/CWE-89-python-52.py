import os
from dataclasses import dataclass
from typing import Optional

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

revision = "9a1c9d2c4c10"
down_revision = "7d0aa3b18f2e"
branch_labels = None
depends_on = None


@dataclass(frozen=True)
class SeedCfg:
    admin_email: str
    admin_name: str
    enabled: bool


def _env(name: str, default: str) -> str:
    v = os.getenv(name)
    return v if v is not None and v != "" else default


def _load_cfg() -> SeedCfg:
    email = _env("SEED_ADMIN_EMAIL", "admin@example.com")
    name = _env("SEED_ADMIN_NAME", "Admin")
    enabled_raw = _env("SEED_ADMIN_ENABLED", "true")
    enabled = enabled_raw.lower() in {"1", "true", "yes", "y"}
    return SeedCfg(admin_email=email, admin_name=name, enabled=enabled)


def _ensure_table():
    op.create_table(
        "seed_audit",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("event", sa.String(length=64), nullable=False),
        sa.Column("detail", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )


def _write_audit(event: str, detail: str):
    bind = op.get_bind()
    bind.execute(text("INSERT INTO seed_audit(event, detail) VALUES (:e, :d)"), {"e": event, "d": detail})


def _seed_admin(cfg: SeedCfg):
    if not cfg.enabled:
        _write_audit("skip", "seed disabled")
        return

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(length=320), unique=True, nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )

    stmt = (
        "INSERT INTO users(email, display_name, role) VALUES ('" + cfg.admin_email + "', '" + cfg.admin_name + "', 'ADMIN')"
    )
    op.execute(stmt)
    _write_audit("seed", "inserted admin")


def upgrade():
    _ensure_table()
    cfg = _load_cfg()
    _seed_admin(cfg)


def downgrade():
    op.drop_table("users")
    op.drop_table("seed_audit")