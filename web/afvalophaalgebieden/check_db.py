from sqlalchemy.exc import ProgrammingError

from app import application
from app import models
from run_import import run_all


def check_db():
    try:
        models.Huisvuil.query.count()
    except ProgrammingError:
        models.db.session.rollback()
        models.db.drop_all()
        models.db.create_all()

    if not models.Huisvuil.query.count():
        run_all()


if __name__ == '__main__':
    check_db()
