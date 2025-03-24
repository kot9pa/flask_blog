"""Add test

Revision ID: 51e954a19a51
Revises: 66ef9524352b
Create Date: 2025-03-21 17:31:43.547631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51e954a19a51'
down_revision = '66ef9524352b'
branch_labels = None
depends_on = None

# Create an ad-hoc table to use for the insert statement.
users_table = sa.table(
    "users",
    sa.column("id", sa.Integer),
    sa.column("username", sa.String),
    sa.column("password_hash", sa.String),
)

posts_table = sa.table(
    "posts",
    sa.column("id", sa.Integer),
    sa.column("title", sa.String),
    sa.column("content", sa.String),
)

def upgrade():
    op.bulk_insert(
        users_table,
        [
            {
                "id": 1,
                "username": "username",
                "password_hash": "scrypt:32768:8:1$J7mLBruNnYJhf9D5$067e302ede66dc976387f8acb3938265a6bfbaa0f501d4e6290e43f5f7cfcb72d958810edd42ff8c2d2cd018fb1cd3b4c8e50440a5ca591479b5da42798c9265"
            },
        ],
    )
    op.bulk_insert(
        posts_table,
        [
            {
                "id": 1,
                "title": "First Post",
                "content": "Content for the first post"
            },
                        {
                "id": 2,
                "title": "Second Post",
                "content": "Content for the second post"
            },
        ],
    )
    op.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")
    op.execute("SELECT setval('posts_id_seq', (SELECT MAX(id) FROM posts))")


def downgrade():
    op.execute("DELETE FROM users WHERE id=1")
    op.execute("DELETE FROM posts WHERE id IN (1, 2)")
