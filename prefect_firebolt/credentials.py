"""This is an example blocks module"""

from prefect.blocks.core import Block
from pydantic import Field, SecretStr


class FireboltCredentials(Block):
    """
    Store credentials for authenticating with Firebolt.

    Attributes:
        username: The email address associated with your Firebolt user.
        password: The password used for connecting to Firebolt.
    """

    _block_type_name = "Firebolt Credentials"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/3loU17IXqVIWl4aWQfqc78/3c7eefe5e8cf4eec870856f10d7fdcce/5e8a264ceaf4870c90478037_Favicon_128.svg.png?h=250"  # noqa

    username: str = Field(
        ..., description="The email address associated with your Firebolt user."
    )
    password: SecretStr = Field(
        ..., description="The password used for connecting to Firebolt."
    )
