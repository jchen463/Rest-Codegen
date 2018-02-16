from .server_variable import ServerVariable
from .schema import Schema
from .callback import Callback
from .response import Response
from .header import Header
from .media_type import MediaType
from .example import Example
from .encoding import Encoding
from .link import Link
from .parameter import Parameter
from .request_body import RequestBody
from .security_scheme import SecurityScheme
from .info import Info
from .contact import Contact
from .license_spec import License
from .paths import Paths
from .operation import Operation
from .external_documentation import ExternalDocumentation
from .components import Components
from .discriminator import Discriminator
from .xml import XML
from .oauth_flows import OAuthFlows
# from .oauth_flow import OAuthFlow
from .server import Server
from .security_requirement import SecurityRequirement
from .tag import Tag


def return_arg(arg):
    return arg


keyword_to_object = {
    # mapping keywords
    'variables': ServerVariable,
    'schemas': Schema,
    'callbacks': Callback,
    'mapping': return_arg,
    'responses': Response,
    'headers': Header,
    'content': MediaType,
    'examples': Example,
    'encoding': Encoding,
    'links': Link,
    'parameters': Parameter,
    'requestBodies': RequestBody,
    'securitySchemes': SecurityScheme,
    'scopes': return_arg,
    'properties': Schema,  # todo: schemas

    # object keywords
    'info': Info,
    'contact': Contact,
    'license': License,
    'paths': Paths,
    'get': Operation,
    'put': Operation,
    'post': Operation,
    'delete': Operation,
    'options': Operation,
    'head': Operation,
    'patch': Operation,
    'trace': Operation,
    'externalDocs': ExternalDocumentation,
    'requestBody': RequestBody,
    'components': Components,
    'discriminator': Discriminator,
    'xml': XML,
    'schema': Schema,
    'flows': OAuthFlows,
    # 'implicit': OAuthFlow,
    # 'password': OAuthFlow,
    # 'clientCredentials': OAuthFlow,
    # 'authorizationCode': OAuthFlow,
    'items': Schema,
    'additionalProperties': Schema,

    # array keywords
    'servers': Server,
    'security': SecurityRequirement,
    'tags': Tag,
    'parameters': Parameter,
    'op_tags': return_arg,  # Operation Object tags
    'allOf': Schema,
    'oneOf': Schema,
    'anyOf': Schema,
    'not': Schema,
    'required': return_arg,
    'enum': return_arg,
}
