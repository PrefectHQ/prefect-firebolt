import pytest
from prefect.testing.utilities import AsyncMock

import prefect_firebolt.database
from prefect_firebolt import FireboltDatabase
from prefect_firebolt.credentials import FireboltCredentials


@pytest.mark.parametrize(
    "engine_name,engine_url",
    [
        ("thomas", None),
        (None, "http://firebolt.io/thomas"),
        ("thomas", "http://firebolt.io/thomas"),
    ],
)
def test_valid_engine_parameters(engine_name, engine_url):
    if engine_name and engine_url:
        with pytest.raises(ValueError):
            FireboltDatabase(
                database="prod",
                credentials=FireboltCredentials(token="abc123"),
                engine_name=engine_name,
                engine_url=engine_url,
            )
    else:
        FireboltDatabase(
            database="prod",
            credentials=FireboltCredentials(token="abc123"),
            engine_name=engine_name,
            engine_url=engine_url,
        )


@pytest.mark.parametrize(
    "credentials",
    [
        (FireboltCredentials(username="me@example.com", password="hunter2")),
        (FireboltCredentials(token="abc123")),
    ],
)
async def test_get_connection(credentials, monkeypatch):
    connect_mock = AsyncMock()
    monkeypatch.setattr(prefect_firebolt.database, "connect", connect_mock)
    await FireboltDatabase(
        database="prod",
        credentials=credentials,
    ).get_connection()
    connect_mock.assert_called_once()

    call_kwargs = connect_mock.call_args.kwargs
    auth = call_kwargs.pop("auth")

    if credentials.token:
        assert auth.token == credentials.token.get_secret_value()
    else:
        assert auth.username == credentials.username
        assert auth.password == credentials.password.get_secret_value()
    assert call_kwargs == {
        "database": "prod",
        "engine_name": None,
        "engine_url": None,
        "api_endpoint": "api.app.firebolt.io",
        "additional_parameters": {},
    }
