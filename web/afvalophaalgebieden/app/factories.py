from factory import Sequence, alchemy, fuzzy

from app import models


class HuisvuilFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: n)
    type = fuzzy.FuzzyText()

    class Meta:
        model = models.Huisvuil
        sqlalchemy_session = models.db.session


class GrofvuilFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: n)
    naam = fuzzy.FuzzyText()

    class Meta:
        model = models.Grofvuil
        sqlalchemy_session = models.db.session
