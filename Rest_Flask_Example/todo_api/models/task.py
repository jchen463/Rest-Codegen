import json
from models.a import A


class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()


class Task(JsonSerializable):
    def __init__(self, id: int, title: str, description: str, done: str):
        self._id = id
        self._title = title
        self._description = description
        self._done = done
        self._randomObject = A()

    def serialize(self):
        return {
            'id': self._id,
            'title': self._title,
            'description': self._description,
            'done': self._done,
            'randomObject': self._randomObject.serialize()
        }

    #
    # def __repr__(self):
    #     return self.serialize()

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
        """Gets the id of this Task.


        :return: The id of this Task.
        :rtype: int
        """
        return self._title

    @id.setter
    def id(self, title: str):
        """Sets the id of this Task.


        :param id: The id of this Task.
        :type id: int
        """

        self._title = title

    @property
    def id(self) -> str:
        """Gets the id of this Task.


        :return: The id of this Task.
        :rtype: int
        """
        return self._description

    @id.setter
    def id(self, id: str):
        """Sets the id of this Task.


        :param id: The id of this Task.
        :type id: int
        """

        self._description = description

    @property
    def id(self) -> str:
        """Gets the id of this Task.


        :return: The id of this Task.
        :rtype: int
        """
        return self._done

    @id.setter
    def id(self, id: str):
        """Sets the id of this Task.


        :param id: The id of this Task.
        :type id: int
        """

        self._done = done
