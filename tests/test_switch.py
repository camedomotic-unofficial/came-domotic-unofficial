"""Test CAME Domotic Unofficial switch."""
from unittest.mock import call, patch

from custom_components.came_domotic_unofficial.const import DOMAIN
from homeassistant.components.switch import SERVICE_TURN_OFF, SERVICE_TURN_ON
from homeassistant.const import ATTR_ENTITY_ID, Platform
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import MOCK_CONFIG


async def _setup_switch(hass, config_entry):
    """Set up integration and return switch entity_id."""
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    # Entity ID format: {platform}.{domain}
    return f"{Platform.SWITCH}.{DOMAIN}"


async def test_switch_state(hass, bypass_get_data):
    """Test switch entity state reflects coordinator data."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entity_id = await _setup_switch(hass, config_entry)

    state = hass.states.get(entity_id)
    assert state is not None
    # MOCK_API_DATA has title="foo", and is_on returns title == "foo" -> on
    assert state.state == "on"


async def test_switch_turn_off(hass, bypass_get_data):
    """Test turning off the switch calls API with 'foo'."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entity_id = await _setup_switch(hass, config_entry)

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_set_title"
    ) as title_func:
        await hass.services.async_call(
            Platform.SWITCH,
            SERVICE_TURN_OFF,
            service_data={ATTR_ENTITY_ID: entity_id},
            blocking=True,
        )
        assert title_func.call_args == call("foo")


async def test_switch_turn_on(hass, bypass_get_data):
    """Test turning on the switch calls API with 'bar'."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entity_id = await _setup_switch(hass, config_entry)

    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_set_title"
    ) as title_func:
        await hass.services.async_call(
            Platform.SWITCH,
            SERVICE_TURN_ON,
            service_data={ATTR_ENTITY_ID: entity_id},
            blocking=True,
        )
        assert title_func.call_args == call("bar")
