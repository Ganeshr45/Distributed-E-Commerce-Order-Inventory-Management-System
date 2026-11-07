from alembic import op
from app.db import Base, engine
from app import models
revision="0001_initial"
down_revision=None
branch_labels=None
depends_on=None
def upgrade(): Base.metadata.create_all(bind=engine)
def downgrade(): Base.metadata.drop_all(bind=engine)
