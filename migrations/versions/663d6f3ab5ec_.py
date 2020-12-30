"""empty message

Revision ID: 663d6f3ab5ec
Revises: 054d10e7dbe6
Create Date: 2020-12-27 18:34:19.621946

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '663d6f3ab5ec'
down_revision = '054d10e7dbe6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quran_text_ayah_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('identifier', sa.String(length=120), nullable=False),
    sa.Column('surah_number', sa.Integer(), nullable=False),
    sa.Column('surah_ar_name', sa.String(length=500), nullable=False),
    sa.Column('surah_en_name', sa.String(length=120), nullable=False),
    sa.Column('surah_en_name_translation', sa.String(length=200), nullable=False),
    sa.Column('revelation_type', sa.String(length=120), nullable=False),
    sa.Column('ayah_number', sa.Integer(), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.Column('juz', sa.Integer(), nullable=False),
    sa.Column('manzil', sa.Integer(), nullable=False),
    sa.Column('page', sa.Integer(), nullable=False),
    sa.Column('ruku', sa.Integer(), nullable=False),
    sa.Column('hizb_quarter', sa.Integer(), nullable=False),
    sa.Column('sajda', sa.Boolean(), nullable=False),
    sa.Column('sajda_id', sa.Integer(), nullable=True),
    sa.Column('sajda_recommended', sa.Boolean(), nullable=True),
    sa.Column('sajda_obligatory', sa.Boolean(), nullable=True),
    sa.Column('language', sa.String(length=120), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('transelator_en_name', sa.String(length=120), nullable=False),
    sa.Column('format', sa.String(length=120), nullable=False),
    sa.Column('type', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('quran_text_ayah_info')
    # ### end Alembic commands ###
