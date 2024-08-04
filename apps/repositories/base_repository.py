import abc
from abc import ABC

from django.db import models


class BaseRepositoryInterface(ABC):

    @abc.abstractmethod
    def _get_all(self) -> models.QuerySet:
        pass

    @abc.abstractmethod
    def _get_by_id(self, id: int | str) -> models.Model:
        pass


class BaseRepository(BaseRepositoryInterface):
    __slots__ = (
        "_model"
    )

    def __init__(self, model: models.Model):
        self._model = model

    def _get_all(self):
        return self._model.objects.all()

    def _get_by_id(self, id: int | str):
        item = self._model.objects.get(pk=id)
        return item
