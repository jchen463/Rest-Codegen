from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from models.base_model_ import Model
import util


class A(Model):
    def __init__(self, b: int=None, c: int=None):
        self.swagger_types = {
            'b': int,
            'c': int
        }

        self.attribute_map = {
            'b': 'b',
            'c': 'c'
        }

        self._b = b
        self._c = b

    @classmethod
    def from_dict(cls, dikt) -> 'A':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Pet of this Pet.  # noqa: E501
        :rtype: Pet
        """
        return util.deserialize_model(dikt, cls)

    @property
    def b(self) -> int:
        """Gets the b of this A.


        :return: The b of this A.
        :rtype: int
        """
        return self._b

    @b.setter
    def b(self, b: int):
        """Sets the b of this A.


        :param b: The b of this A.
        :type b: int
        """

        self._b = b

    @property
    def c(self) -> int:
        """Gets the c of this A.


        :return: The c of this A.
        :rtype: int
        """
        return self._c

    @c.setter
    def c(self, c: int):
        """Sets the c of this A.


        :param c: The c of this A.
        :type c: int
        """

        self._c = c
