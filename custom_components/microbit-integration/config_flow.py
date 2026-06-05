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
    ports = []
    for port in list_ports.comports():
        # Only include real USB serial devices (has VID/PID)
        if port.vid is not None and port.pid is not None:
            ports.append(port.device)

    return ports


class MicrobitConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title=f"Microbit ({user_input['serial_port']})",
                data={"serial_port": user_input["serial_port"]},
            )

        ports = await self.hass.async_add_executor_job(get_serial_ports)

        if not ports:
            ports = ["No ports found"]

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("serial_port"): SelectSelector(
                        SelectSelectorConfig(
                            options=ports, mode=SelectSelectorMode.DROPDOWN
                        )
                    )
                }
            ),
        )
