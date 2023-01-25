from sqlalchemy import Table, MetaData
from sqlalchemy.exc import ProgrammingError

import app
from app import models, db
from run_import import run_all


def check_db():
    with app.application.app_context():
        try:
            # Test if databases exist
            models.Huisvuil.query.count()
            models.Grofvuil.query.count()
        except ProgrammingError:
            models.recreate_db()
            models.db.session.rollback()
            models.db.drop_all()
            models.db.create_all()

        # Simple migration strategy. If more migrations occur please consider using flask-migrate
        meta = MetaData()
        messages = Table('grofvuil', meta, autoload=True, autoload_with=db.engine)
        if not 'tijd_vanaf' in [c.name for c in messages.columns]:
            models.db.create_all()

        if not (models.Huisvuil.query.count() and models.Grofvuil.query.count()):
            run_all()


if __name__ == '__main__':
    check_db()
