from factory import Sequence, alchemy, fuzzy
from geoalchemy2.shape import from_shape
from shapely.geometry import Polygon, Point

from app import models

polygon = Polygon([(0, 0), (40, 0), (40, 40), (0, 40), (0, 0)])
point = Point((30, 30))


class HuisvuilFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: n)
    type = fuzzy.FuzzyText()
    geometrie = from_shape(polygon, srid=28992)

    class Meta:
        model = models.Huisvuil
        sqlalchemy_session = models.db.session


class GrofvuilFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: n)
    naam = fuzzy.FuzzyText()
    geometrie = from_shape(polygon, srid=28992)

    class Meta:
        model = models.Grofvuil
        sqlalchemy_session = models.db.session


class KleinChemischFactory(alchemy.SQLAlchemyModelFactory):
    id = Sequence(lambda n: n)
    type = fuzzy.FuzzyText()
    geometrie = from_shape(point, srid=28992)

    class Meta:
        model = models.KleinChemisch
        sqlalchemy_session = models.db.session
