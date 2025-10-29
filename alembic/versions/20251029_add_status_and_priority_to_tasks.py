"""add status and priority to tasks

Revision ID: new_migration
Revises:
Create Date: 2025-10-29
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "new_migration"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create enum types first
    op.execute("CREATE TYPE taskstatus AS ENUM ('todo', 'in_progress', 'completed')")
    op.execute("CREATE TYPE taskpriority AS ENUM ('low', 'medium', 'high')")

    # Add new columns to existing tasks table
    op.add_column(
        "tasks",
        sa.Column(
            "status",
            sa.Enum("todo", "in_progress", "completed", name="taskstatus"),
            nullable=False,
            server_default="todo",
        ),
    )
    op.add_column(
        "tasks",
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="taskpriority"),
            nullable=False,
            server_default="low",
        ),
    )


def downgrade() -> None:
    # Remove columns first
    op.drop_column("tasks", "priority")
    op.drop_column("tasks", "status")

    # Then drop enum types
    op.execute("DROP TYPE taskpriority")
    op.execute("DROP TYPE taskstatus")
