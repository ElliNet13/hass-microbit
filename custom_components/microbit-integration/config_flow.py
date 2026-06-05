import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers.selector import (
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from serial.tools import list_ports

DOMAIN = "microbit_integration"


def get_serial_ports():
    """Return list of (label, device) tuples."""
    ports = []

    for port in list_ports.comports():
        # Only real USB serial devices
        if port.vid is None or port.pid is None:
            continue

        # Build friendly label
        if port.manufacturer and port.product:
            label = f"{port.manufacturer} {port.product}"
        elif port.product:
            label = port.product
        else:
            label = port.description

        label = f"{label} ({port.device})"

        ports.append((label, port.device))

    return ports


class MicrobitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        ports = await self.hass.async_add_executor_job(get_serial_ports)

        # Build selector options (Home Assistant format)
        if ports:
            options = [{"label": label, "value": value} for label, value in ports]
        else:
            options = [{"label": "No micro:bit devices found", "value": ""}]

        if user_input is not None:
            return self.async_create_entry(
                title=f"Microbit ({user_input['serial_port']})",
                data={"serial_port": user_input["serial_port"]},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("serial_port"): SelectSelector(
                        SelectSelectorConfig(
                            options=options,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )