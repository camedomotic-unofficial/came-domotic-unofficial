"""Test CAME Domotic Unofficial sensor."""
from __future__ import annotations

from custom_components.came_domotic_unofficial.const import DOMAIN
from homeassistant.const import Platform
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import MOCK_CONFIG


async def test_sensor_state(hass, bypass_get_data):
    """Test sensor returns software_version from coordinator data."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = f"{Platform.SENSOR}.{DOMAIN}"
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == "1.2.3"
