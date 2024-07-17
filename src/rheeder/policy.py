"""
pydantic-iam-policy

Docs:
https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html
"""
import typing

import pydantic

class PrincipalMapEntry:
    def validate(self):
        # custom validate
        # - keys: ("AWS" | "Federated" | "Service" | "CanonicalUser")
        # - values: [<principal_id_string>, <principal_id_string>, ...]

        # valid principal_id_string:
        # https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns
        pass


class Statement(pydantic.BaseModel):
    # <statement> = {
    #     <sid_block?>,
    #     <principal_block?>,
    #     <effect_block>,
    #     <action_block>,
    #     <resource_block>,
    #     <condition_block?>
    # }

    # <sid_block> = "Sid" : <sid_string>

    # <effect_block> = "Effect" : ("Allow" | "Deny")

    Sid: str = pydantic.Field(pattern=r"[A-Za-z0-9]")
    Effect: typing.Literal['Allow', 'Deny']
    Resource: typing.Union[str, list[str]]
    # XOR
    Principal: str = None
    NotPrincipal: str = None
    # XOR
    Action: typing.Union[str, list[str]] = None
    NotAction: typing.Union[str, list[str]] = None
    # XOR
    Resource: typing.Union[str, list[str]] = None
    NotResource: typing.Union[str, list[str]] = None


    def sid_block(self):
        pass #?

    def principal_block(self):
        # <principal_block> = ("Principal" | "NotPrincipal") : ("*" | <principal_map>)

        # <principal_map> = { <principal_map_entry>, <principal_map_entry>, ... }

        # <principal_map_entry> = ("AWS" | "Federated" | "Service" | "CanonicalUser") :
        #     [<principal_id_string>, <principal_id_string>, ...]

        # XOR
        # Principal: str = None
        # NotPrincipal: str = None
        pass #?

    def effect_block(self):
        pass #

    def action_block(self):
        # <action_block> = ("Action" | "NotAction") :
        #     ("*" | [<action_string>, <action_string>, ...])

        # XOR
        # Action: typing.Union[str, list[str]] = None
        # NotAction: typing.Union[str, list[str]] = None
        pass #

    def resource_block(self):
        # <resource_block> = ("Resource" | "NotResource") :
        #     : ("*" | <resource_string> | [<resource_string>, <resource_string>, ...])

        # XOR
        # Resource: typing.Union[str, list[str]] = None
        # NotResource: typing.Union[str, list[str]] = None
        pass #

    def condition_block(self):
        # <condition_block> = "Condition" : { <condition_map> }
        # <condition_map> = {
        #   <condition_type_string> : { <condition_key_string> : <condition_value_list> },
        #   <condition_type_string> : { <condition_key_string> : <condition_value_list> }, ...
        # }
        # <condition_value_list> = [<condition_value>, <condition_value>, ...]
        # <condition_value> = (<condition_value_string> | <condition_value_string> | <condition_value_string>)
        pass #?



class Policy(pydantic.BaseModel):
    # policy  = {
    #      <version_block?>
    #      <id_block?>
    #      <statement_block>
    # }

    # <version_block> = "Version" : ("2008-10-17" | "2012-10-17")

    # <id_block> = "Id" : <policy_id_string>

    # <statement_block> = "Statement" : [ <statement>, <statement>, ... ]

    Id: str = pydantic.Field(pattern=r"[A-Za-z0-9\_\-]")
    Version: typing.Literal['2008-10-17', '2012-10-17']
    Statement: typing.Union[Statement, list[Statement]]


# data = {
#     'Id': '42',
#     'Version': '2012-10-17',
#     'Statement': {
#         'Sid': '1',
#         'Effect': 'Allow',
#         'Action': 'ec2:*',
#         'Resource': '*',
#     }
# }

# policy = Policy(**data)
# policy
