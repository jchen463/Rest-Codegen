from flask.json import JSONEncoder
import six

from models.base_model_ import Model


class JSONEncoder(JSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            print(o)
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                print("attr is " + attr)
                value = getattr(o, attr)
                print(value)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return JSONEncoder.default(self, o)
