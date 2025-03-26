"""Zero migration

Revision ID: a9e38e578620
Revises:
Create Date: 2025-03-24 22:17:12.661450

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9e38e578620"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "learning_texts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.Integer(), nullable=True),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("transcription", sa.Text(), nullable=False),
        sa.CheckConstraint("difficulty >= 0", name="check_text_difficulty_is_positive"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_index(
        "learning_text_title_idx",
        "learning_texts",
        ["title"],
        unique=False,
        postgresql_using="hash",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("learning_text_title_idx", table_name="learning_texts", postgresql_using="hash")
    op.drop_table("learning_texts")
    # ### end Alembic commands ###
