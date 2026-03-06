"""
Custom integration to integrate CAME Domotic Unofficial with Home Assistant.

For more details about this integration, please refer to
https://github.com/camedomotic-unofficial/came-domotic-unofficial
"""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import CameDomoticUnofficialApiClient
from .coordinator import CameDomoticUnofficialDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR, Platform.SWITCH]

type CameDomoticUnofficialConfigEntry = ConfigEntry[RuntimeData]


@dataclass
class RuntimeData:
    """Class to hold runtime data."""

    coordinator: DataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: CameDomoticUnofficialConfigEntry
) -> bool:
    """Set up this integration using UI."""
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    session = async_get_clientsession(hass)
    client = CameDomoticUnofficialApiClient(username, password, session)

    coordinator = CameDomoticUnofficialDataUpdateCoordinator(
        hass, client=client, config_entry=entry
    )
    await coordinator.async_config_entry_first_refresh()

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    entry.runtime_data = RuntimeData(coordinator)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def _async_update_listener(
    hass: HomeAssistant, entry: CameDomoticUnofficialConfigEntry
) -> None:
    """Handle config options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: ConfigEntry, device_entry: DeviceEntry
) -> bool:
    """Delete device if selected from UI."""
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: CameDomoticUnofficialConfigEntry
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
