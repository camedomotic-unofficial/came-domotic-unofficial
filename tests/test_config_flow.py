"""Test CAME Domotic Unofficial config flow."""
from unittest.mock import patch

import pytest
from custom_components.came_domotic_unofficial.api import (
    CameDomoticUnofficialApiClientAuthenticationError,
    CameDomoticUnofficialApiClientCommunicationError,
    CameDomoticUnofficialApiClientError,
)
from custom_components.came_domotic_unofficial.const import DOMAIN
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResultType
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import MOCK_CONFIG


@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.came_domotic_unofficial.async_setup_entry",
        return_value=True,
    ):
        yield


async def test_successful_config_flow(hass, bypass_get_data):
    """Test a successful config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "test_username"
    assert result["data"] == MOCK_CONFIG
    assert result["result"]


async def test_config_flow_cannot_connect(hass):
    """Test config flow with connection error shows cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientCommunicationError("Timeout"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_config_flow_invalid_auth(hass):
    """Test config flow with authentication error shows invalid_auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientAuthenticationError("Bad creds"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}


async def test_config_flow_unknown_error(hass):
    """Test config flow with unexpected exception shows unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=Exception("Unexpected"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}


async def test_config_flow_single_entry_abort(hass, bypass_get_data):
    """Test that only one config entry is allowed (single_config_entry)."""
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG)
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_reconfigure_flow_success(hass, bypass_get_data):
    """Test successful reconfigure flow updates credentials."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
        unique_id="test_username",
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    new_config = {CONF_USERNAME: "new_user", CONF_PASSWORD: "new_pass"}
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=new_config
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert entry.data[CONF_USERNAME] == "new_user"
    assert entry.data[CONF_PASSWORD] == "new_pass"


async def _init_reconfigure_flow(hass, entry):
    """Start a reconfigure flow and return the form result."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={
            "source": config_entries.SOURCE_RECONFIGURE,
            "entry_id": entry.entry_id,
        },
    )
    assert result["type"] is FlowResultType.FORM
    return result


async def test_reconfigure_flow_cannot_connect(hass):
    """Test reconfigure flow with connection error shows cannot_connect."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, unique_id="test_username"
    )
    entry.add_to_hass(hass)
    result = await _init_reconfigure_flow(hass, entry)

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientCommunicationError("Timeout"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_reconfigure_flow_invalid_auth(hass):
    """Test reconfigure flow with auth error shows invalid_auth."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, unique_id="test_username"
    )
    entry.add_to_hass(hass)
    result = await _init_reconfigure_flow(hass, entry)

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientAuthenticationError("Bad creds"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "invalid_auth"}


async def test_reconfigure_flow_unknown_error(hass):
    """Test reconfigure flow with unexpected error shows unknown."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, unique_id="test_username"
    )
    entry.add_to_hass(hass)
    result = await _init_reconfigure_flow(hass, entry)

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=Exception("Unexpected"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}


async def test_config_flow_generic_api_error(hass):
    """Test that base ApiClientError (non-comm, non-auth) maps to cannot_connect."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientError("Parse error"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=MOCK_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}


async def test_options_flow(hass, bypass_get_data):
    """Test options flow for scan interval."""
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entry.add_to_hass(hass)

    await hass.config_entries.async_setup(entry.entry_id)
    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_SCAN_INTERVAL: 60},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert entry.options == {CONF_SCAN_INTERVAL: 60}
