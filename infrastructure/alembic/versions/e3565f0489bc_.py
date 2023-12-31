"""empty message

Revision ID: e3565f0489bc
Revises: 
Create Date: 2023-08-03 23:24:27.882153

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e3565f0489bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('debts',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('government_id', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('debt_amount', sa.DECIMAL(), nullable=False),
    sa.Column('debt_due_date', sa.Date(), nullable=True),
    sa.Column('debt_identifier', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_debts_debt_identifier'), 'debts', ['debt_identifier'], unique=True)
    op.create_index(op.f('ix_debts_id'), 'debts', ['id'], unique=False)
    op.create_table('bank_slips',
    sa.Column('debt_id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('payment_link', sa.String(), nullable=False),
    sa.Column('barcode', sa.String(), nullable=False),
    sa.Column('paid_at', sa.DateTime(), nullable=True),
    sa.Column('paid_amount', sa.DECIMAL(), nullable=True),
    sa.Column('paid_by', sa.String(), nullable=True),
    sa.Column('notified_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"), nullable=True),
    sa.ForeignKeyConstraint(['debt_id'], ['debts.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('debt_id')
    )
    op.create_index(op.f('ix_bank_slips_id'), 'bank_slips', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bank_slips_id'), table_name='bank_slips')
    op.drop_table('bank_slips')
    op.drop_index(op.f('ix_debts_id'), table_name='debts')
    op.drop_index(op.f('ix_debts_debt_identifier'), table_name='debts')
    op.drop_table('debts')
    # ### end Alembic commands ###
