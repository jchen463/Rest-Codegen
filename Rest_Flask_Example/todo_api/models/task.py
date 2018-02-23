from __future__ import absolute_import
from datetime import date, datetime
from typing import List, Dict

from models.a import A
from models.base_model_ import Model
import util


class Task(Model):
    def __init__(self, id: int=None, title: str=None, description: str=None, done: bool=None, random_object: A=None):

        self.swagger_types = {
            'id': int,
            'title': str,
            'description': str,
            'done': bool,
            'random_object': A,
        }

        self.attribute_map = {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'done': 'done',
            'random_object': 'random_object'
        }

        self._id = id
        self._title = title
        self._description = description
        self._done = done
        self._random_object = random_object

    @classmethod
    def from_dict(cls, dikt) -> 'Task':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Pet of this Pet.  # noqa: E501
        :rtype: Pet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        self._title = title

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, done: bool):
        self._done = done

    @property
    def random_object(self) -> A:
        return self._random_object

    @random_object.setter
    def random_object(self, random_object: A):
        self._random_object = random_object
