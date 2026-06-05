"""
Custom integration to integrate integration_blueprint with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/integration_blueprint
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING
import serial

from homeassistant.config_entries import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.const import Platform
from homeassistant.loader import async_get_loaded_integration

from .api import IntegrationBlueprintApiClient
from .const import DOMAIN, LOGGER
from .coordinator import BlueprintDataUpdateCoordinator
from .data import IntegrationBlueprintData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import IntegrationBlueprintConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.LIGHT,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Set up this integration using UI."""

    # Validate serial port quick
    if (
        entry.data["serial_port"] is None
        or entry.data["serial_port"] == "No ports found"
    ):
        raise ConfigEntryAuthFailed("No valid serial port found")

    # Check if it exists on the filesystem and is accessible
    if not os.path.exists(entry.data["serial_port"]) or not os.access(entry.data["serial_port"], os.R_OK | os.W_OK):  # noqa: ASYNC240, PTH110
        raise ConfigEntryNotReady(
            f"Serial port {entry.data['serial_port']} does not exist or is not accessible. Please make sure your micro:bit is connected and you have dialout permissions and try again."
        )

    # Setup the entry
    coordinator = BlueprintDataUpdateCoordinator(hass=hass, logger=LOGGER, name=DOMAIN)
    entry.runtime_data = IntegrationBlueprintData(
        client=IntegrationBlueprintApiClient(
            serial_port=serial.Serial(entry.data["serial_port"], baudrate=115200, timeout=1)
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
