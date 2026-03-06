"""Sensor platform for CAME Domotic Unofficial."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import CameDomoticUnofficialConfigEntry
from .const import ICON
from .entity import CameDomoticUnofficialEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CameDomoticUnofficialConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor platform."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities([CameDomoticUnofficialSensor(coordinator, "sensor")])


class CameDomoticUnofficialSensor(CameDomoticUnofficialEntity, SensorEntity):
    """CAME Domotic Unofficial Sensor class."""

    _attr_translation_key = "sensor"
    _attr_icon = ICON

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        return self.coordinator.data.get("body")
