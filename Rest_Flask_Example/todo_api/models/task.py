from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.a import A
from models.base_model_ import Model
import util


class Task(Model):

    def __init__(self, id: int=None, title: str=None, description: str=None, done: bool=None, randomObject: A=None):

        self.swagger_types = {
            'id': int,
            'title': str,
            'description': str,
            'done': bool,
            'randomObject': A,
        }

        self.attribute_map = {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'done': 'done',
            'random_Object': 'randomObject'
        }

        self._id = id
        self._title = title
        self._description = description
        self._done = done
        self._randomObject = randomObject

    @classmethod
    def from_dict(cls, dikt) -> 'Task':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Pet of this Pet.  # noqa: E501
        :rtype: Pet
        """
        return util.deserialize_model(dikt, cls)

    def a() -> int:
        pass

    @property
    def id(self) -> int:
        """Gets the id of this Task.


        :return: The id of this Task.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id: int):
        """Sets the id of this Task.


        :param id: The id of this Task.
        :type id: int
        """

        self._id = id

    @property
    def title(self) -> str:
        """Gets the title of this Task.


        :return: The title of this Task.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Task.


        :param title: The title of this Task.
        :type title: str
        """

        self._title = title

    @property
    def description(self) -> str:
        """Gets the description of this Task.


        :return: The description of this Task.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description: str):
        """Sets the description of this Task.


        :param description: The description of this Task.
        :type description: str
        """

        self._description = description

    @property
    def done(self) -> str:
        """Gets the done of this Task.


        :return: The done of this Task.
        :rtype: int
        """
        return self._done

    @done.setter
    def done(self, done: bool):
        """Sets the done of this Task.


        :param done: The done of this Task.
        :type done: int
        """

        self._done = done

    @property
    def randomObject(self) -> str:
        """Gets the randomObject of this Task.


        :return: The randomObject of this Task.
        :rtype: A
        """
        return self._randomObject

    @randomObject.setter
    def randomObject(self, randomObject: A):
        """Sets the randomObject of this Task.


        :param done: The randomObject of this Task.
        :type done: A
        """

        self._randomObject = randomObject
