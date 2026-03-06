"""Test CAME Domotic Unofficial binary sensor."""
from unittest.mock import patch

from custom_components.came_domotic_unofficial.const import DOMAIN
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import MOCK_CONFIG


async def test_binary_sensor_state_on(hass, bypass_get_data):
    """Test binary sensor is on when title is 'foo'."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Entity ID includes translation_key suffix from HA entity naming
    entity_id = f"{Platform.BINARY_SENSOR}.{DOMAIN}_connectivity"
    state = hass.states.get(entity_id)
    assert state is not None
    # MOCK_API_DATA has title="foo", and is_on returns title == "foo" -> on
    assert state.state == "on"


async def test_binary_sensor_state_off(hass):
    """Test binary sensor is off when title is not 'foo'."""
    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        return_value={"userId": 1, "id": 1, "title": "bar", "body": "text"},
    ):
        config_entry = MockConfigEntry(
            domain=DOMAIN, data=MOCK_CONFIG, entry_id="test"
        )
        config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()

    entity_id = f"{Platform.BINARY_SENSOR}.{DOMAIN}_connectivity"
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "off"
