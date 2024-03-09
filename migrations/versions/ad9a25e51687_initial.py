"""initial

Revision ID: ad9a25e51687
Revises: 
Create Date: 2024-03-08 09:41:39.444638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad9a25e51687'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articleshistory',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('article', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_articleshistory_article'), 'articleshistory', ['article'], unique=False)
    op.create_index(op.f('ix_articleshistory_id'), 'articleshistory', ['id'], unique=False)
    op.create_index(op.f('ix_articleshistory_user_id'), 'articleshistory', ['user_id'], unique=False)
    op.create_table('articleusersubscribes',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('article', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('user_id', 'article')
    )
    op.create_index(op.f('ix_articleusersubscribes_article'), 'articleusersubscribes', ['article'], unique=False)
    op.create_index(op.f('ix_articleusersubscribes_user_id'), 'articleusersubscribes', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_articleusersubscribes_user_id'), table_name='articleusersubscribes')
    op.drop_index(op.f('ix_articleusersubscribes_article'), table_name='articleusersubscribes')
    op.drop_table('articleusersubscribes')
    op.drop_index(op.f('ix_articleshistory_user_id'), table_name='articleshistory')
    op.drop_index(op.f('ix_articleshistory_id'), table_name='articleshistory')
    op.drop_index(op.f('ix_articleshistory_article'), table_name='articleshistory')
    op.drop_table('articleshistory')
    # ### end Alembic commands ###