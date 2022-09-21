"""Module for interacting with Firebolt databases"""
from typing import Dict, Optional

from firebolt.async_db.connection import Connection, connect
from firebolt.client.auth import Token, UsernamePassword
from prefect.blocks.core import Block
from pydantic import Field, root_validator

from prefect_firebolt.credentials import FireboltCredentials


class FireboltDatabase(Block):
    """
    Connects to a Firebolt database.

    Provide either `engine_name` or `engine_url`. Providing both will result in an
    error. If neither `engine_name` nor `engine_url` is provided, the default engine
    for the configured database will be used.

    Attributes:
        credentials: Credentials to use to connect to the Firebase database.
        database_name: The name of the database to connect to.
        engine_name: Name of the engine to connect to.
        engine_url: The engine endpoint to use.
        additional_parameters: Additional configuration to pass to the Firebolt
            connection.
    """

    _block_type_name = "Firebolt Database"
    _logo_url = "https://images.ctfassets.net/gm98wzqotmnx/3loU17IXqVIWl4aWQfqc78/3c7eefe5e8cf4eec870856f10d7fdcce/5e8a264ceaf4870c90478037_Favicon_128.svg.png?h=250"  # noqa
    _description = "Connects to a Firebolt database."

    credentials: FireboltCredentials
    database: str = Field(
        default=...,
        title="Database Name",
        description="The name of the database to connect to.",
    )
    engine_name: Optional[str] = Field(
        None,
        description="Name of the engine to connect to. May not be used with "
        "engine_url. If neither engine_name nor engine_url is provided, the "
        "default engine for the configured database will be used.",
    )
    engine_url: Optional[str] = Field(
        None,
        title="Engine URL",
        description="The engine endpoint to use. May not be used with engine_name. "
        "If neither engine_name nor engine_url is provided, the "
        "default engine for the configured database will be used.",
    )
    additional_parameters: Optional[Dict] = Field(
        default_factory=dict,
        description="Additional configuration to pass to the Firebolt connection.",
    )

    @root_validator(pre=True)
    def _not_both_engine_name_and_engine_url(cls, values):
        """Ensures that engine_name and engine_url are not both provided"""
        if (
            values.get("engine_name") is not None
            and values.get("engine_url") is not None
        ):
            raise ValueError(
                "You have provided a value for both engine_name and engine_url. "
                "Please provide either engine_name or engine_url, but not both."
            )
        return values

    async def get_connection(self) -> Connection:
        """
        Creates and returns an authenticated Firebolt connection for the
        configured database.
        """
        if self.credentials.token:
            auth = Token(token=self.credentials.token.get_secret_value())
        elif self.credentials.username and self.credentials.password:
            auth = UsernamePassword(
                username=self.credentials.username,
                password=self.credentials.password.get_secret_value(),
            )
        else:
            raise ValueError(
                "Unable to initialize Firebolt auth. Expected username "
                "and password or token, but received neither."
            )

        return await connect(
            database=self.database,
            auth=auth,
            engine_name=self.engine_name,
            engine_url=self.engine_url,
            api_endpoint=self.credentials.api_endpoint,
            additional_parameters=self.additional_parameters,
        )