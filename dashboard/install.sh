#!/usr/bin/env bash
# Install the IH-53 EV dashboard as a systemd service and open Chromium
# fullscreen on :10000 at desktop login. Enables PiCAN 3 (can0 @ 250 kbps).
# Run from this directory: sudo ./install.sh
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
	echo "Run as root, e.g.: sudo $0" >&2
	exit 1
fi

APP_USER="${SUDO_USER:-}"
if [[ -z "${APP_USER}" || "${APP_USER}" == root ]]; then
	APP_USER=pi
fi

INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_HOME="$(getent passwd "${APP_USER}" | cut -d: -f6)"
if [[ -z "${USER_HOME}" || ! -d "${USER_HOME}" ]]; then
	echo "Home directory for user '${APP_USER}' not found." >&2
	exit 1
fi
APP_UID="$(id -u "${APP_USER}")"

CONFIG_TXT="/boot/firmware/config.txt"
if [[ ! -f "${CONFIG_TXT}" ]]; then
	echo "Error: ${CONFIG_TXT} not found (not a Raspberry Pi OS boot partition?)." >&2
	exit 1
fi

CONFIG_NEEDS_REBOOT=0

ensure_config_line() {
	local line="$1"
	if grep -qF "${line}" "${CONFIG_TXT}"; then
		return 0
	fi
	echo "${line}" >> "${CONFIG_TXT}"
	echo "Added to ${CONFIG_TXT}: ${line}"
	CONFIG_NEEDS_REBOOT=1
}

configure_boot() {
	echo "Configuring boot (PiCAN 3 / MCP2515)..."
	ensure_config_line "dtparam=spi=on"
	ensure_config_line "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25"
}

# Control Centre "Left" (90). Use 270 for "Right" if the dash is mirrored.
DISPLAY_TRANSFORM=90

connected_dsi() {
	local path name
	for path in /sys/class/drm/card*-DSI-*; do
		[[ -f "${path}/status" ]] || continue
		if [[ "$(cat "${path}/status")" == connected ]]; then
			name="$(basename "${path}")"
			echo "${name#*-}"
			return 0
		fi
	done
	return 1
}

touch_device_name() {
	awk -F\" '
		/^N: Name=/ { n = $2 }
		n ~ /[Ii][Ll][Ii]|[Tt]ouch|[Gg]oodix|[Ff][Tt]5/ { print n; exit }
	' /proc/bus/input/devices 2>/dev/null || true
}

ensure_key() {
	local file="$1" key="$2" value="$3"
	mkdir -p "$(dirname "${file}")"
	if [[ -f "${file}" ]] && grep -q "^${key}=" "${file}"; then
		sed -i "s|^${key}=.*|${key}=${value}|" "${file}"
	else
		printf '%s=%s\n' "${key}" "${value}" >> "${file}"
	fi
}

ensure_touch_map() {
	local rc="${USER_HOME}/.config/labwc/rc.xml"
	local output="$1"
	local dev="$2"
	mkdir -p "${USER_HOME}/.config/labwc"
	if [[ -z "${dev}" ]]; then
		return 0
	fi
	if [[ ! -f "${rc}" ]]; then
		cat > "${rc}" << EOF
<?xml version="1.0"?>
<openbox_config xmlns="http://openbox.org/3.4/rc">
	<touch deviceName="${dev}" mapToOutput="${output}" mouseEmulation="yes"/>
</openbox_config>
EOF
		return 0
	fi
	if grep -q '<touch ' "${rc}"; then
		sed -i -E "s/mapToOutput=\"[^\"]*\"/mapToOutput=\"${output}\"/" "${rc}"
	else
		sed -i "s|</openbox_config>|	<touch deviceName=\"${dev}\" mapToOutput=\"${output}\" mouseEmulation=\"yes\"/>\\n</openbox_config>|" "${rc}"
	fi
}

configure_desktop() {
	echo "Configuring landscape display and large-screen defaults..."
	local dsi touch_dev desktop_font
	dsi="$(connected_dsi || true)"
	touch_dev="$(touch_device_name)"
	if fc-list 2>/dev/null | grep -q 'Nunito Sans'; then
		desktop_font="Nunito Sans Light 16"
	else
		desktop_font="PibotoLt 16"
	fi

	install -d -o "${APP_USER}" -g "${APP_USER}" \
		"${USER_HOME}/.config/kanshi" \
		"${USER_HOME}/.config/labwc" \
		"${USER_HOME}/.config/gtk-3.0" \
		"${USER_HOME}/.config/wf-panel-pi" \
		"${USER_HOME}/.config/pcmanfm/default"

	# Separate profiles so either CAM/DISP port matches.
	cat > "${USER_HOME}/.config/kanshi/config" << EOF
# Landscape — Control Centre Orientation Left (${DISPLAY_TRANSFORM}).
# Use 270 for Right if the image is sideways the wrong way.
profile {
	output DSI-1 enable transform ${DISPLAY_TRANSFORM}
}
profile {
	output DSI-2 enable transform ${DISPLAY_TRANSFORM}
}
EOF

	ensure_touch_map "${dsi:-DSI-1}" "${touch_dev}"
	ensure_key "${USER_HOME}/.config/labwc/environment" XCURSOR_SIZE 36

	local gtk_ini="${USER_HOME}/.config/gtk-3.0/settings.ini"
	if [[ ! -f "${gtk_ini}" ]]; then
		printf '[Settings]\n' > "${gtk_ini}"
	fi
	if grep -q '^gtk-font-name=' "${gtk_ini}"; then
		sed -i "s|^gtk-font-name=.*|gtk-font-name=${desktop_font}|" "${gtk_ini}"
	else
		printf 'gtk-font-name=%s\n' "${desktop_font}" >> "${gtk_ini}"
	fi

	local wf_ini="${USER_HOME}/.config/wf-panel-pi/wf-panel-pi.ini"
	if [[ ! -s "${wf_ini}" && -f /etc/xdg/wf-panel-pi/wf-panel-pi.ini ]]; then
		cp /etc/xdg/wf-panel-pi/wf-panel-pi.ini "${wf_ini}"
	fi
	ensure_key "${wf_ini}" icon_size 52
	ensure_key "${wf_ini}" window-list_max_width 300

	local desk_conf="${USER_HOME}/.config/pcmanfm/default/desktop-items-0.conf"
	if [[ ! -f "${desk_conf}" && -f /etc/xdg/pcmanfm/default/desktop-items-0.conf ]]; then
		cp /etc/xdg/pcmanfm/default/desktop-items-0.conf "${desk_conf}"
	fi
	if [[ -f "${desk_conf}" ]]; then
		ensure_key "${desk_conf}" desktop_font "${desktop_font}"
	fi

	chown -R "${APP_USER}:${APP_USER}" \
		"${USER_HOME}/.config/kanshi" \
		"${USER_HOME}/.config/labwc" \
		"${USER_HOME}/.config/gtk-3.0" \
		"${USER_HOME}/.config/wf-panel-pi" \
		"${USER_HOME}/.config/pcmanfm"

	if [[ -n "${dsi}" && -S "/run/user/${APP_UID}/wayland-0" ]]; then
		sudo -u "${APP_USER}" env \
			XDG_RUNTIME_DIR="/run/user/${APP_UID}" \
			WAYLAND_DISPLAY=wayland-0 \
			wlr-randr --output "${dsi}" --transform "${DISPLAY_TRANSFORM}" \
			>/dev/null 2>&1 || true
		pkill -HUP -u "${APP_USER}" kanshi >/dev/null 2>&1 || true
	fi
}

configure_boot
configure_desktop

echo "Installing dependencies..."
apt-get update -qq
deps=(curl can-utils)
if ! command -v go >/dev/null 2>&1; then
	deps+=(golang-go)
fi
if ! command -v chromium >/dev/null 2>&1 && ! command -v chromium-browser >/dev/null 2>&1; then
	deps+=(chromium)
fi
apt-get install -y "${deps[@]}"

CHROMIUM="$(command -v chromium || command -v chromium-browser || true)"
if [[ -z "${CHROMIUM}" ]]; then
	echo "chromium not found after package install." >&2
	exit 1
fi

echo "Building dashboard..."
sudo -u "${APP_USER}" env HOME="${USER_HOME}" GOWORK=off bash -c \
	"cd '${INSTALL_DIR}' && go build -o ih53ev-dashboard ./cmd/dashboard"
chown "${APP_USER}:${APP_USER}" "${INSTALL_DIR}/ih53ev-dashboard"

if getent group netdev >/dev/null; then
	usermod -aG netdev "${APP_USER}" 2>/dev/null || true
fi

install -m 0644 "${INSTALL_DIR}/deploy/can0.network" /etc/systemd/network/80-can0.network
systemctl enable systemd-networkd
systemctl restart systemd-networkd || true

cat << BROWSER_SCRIPT > /usr/local/bin/ih53ev-browser.sh
#!/usr/bin/env sh
# Wait for the local dashboard, then open Chromium fullscreen (kiosk).
export DISPLAY="\${DISPLAY:-:0}"
export XDG_RUNTIME_DIR="\${XDG_RUNTIME_DIR:-/run/user/${APP_UID}}"
export WAYLAND_DISPLAY="\${WAYLAND_DISPLAY:-wayland-0}"
URL="http://127.0.0.1:10000"
until curl -sf "\$URL" >/dev/null 2>&1; do sleep 1; done
exec ${CHROMIUM} --kiosk --start-fullscreen --noerrdialogs --disable-infobars \\
	--check-for-update-interval=31536000 --app="\$URL"
BROWSER_SCRIPT
chmod 0755 /usr/local/bin/ih53ev-browser.sh

cat << BROWSER_UNIT > /etc/systemd/system/ih53ev-browser.service
[Unit]
Description=Open Chromium fullscreen for IH-53 EV dashboard
After=network-online.target graphical.target ih53ev-dashboard.service
Wants=network-online.target ih53ev-dashboard.service

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
Environment=DISPLAY=:0
Environment=WAYLAND_DISPLAY=wayland-0
Environment=XDG_RUNTIME_DIR=/run/user/${APP_UID}
Environment=XAUTHORITY=${USER_HOME}/.Xauthority
ExecStart=/usr/local/bin/ih53ev-browser.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical.target
BROWSER_UNIT

cat << UNIT > /etc/systemd/system/ih53ev-dashboard.service
[Unit]
Description=IH-53 EV CAN dashboard
After=network-online.target sys-subsystem-net-devices-can0.device
Wants=network-online.target
# can0 is configured by systemd-networkd (80-can0.network) at 250000 bit/s.

[Service]
Type=simple
User=${APP_USER}
Group=${APP_USER}
SupplementaryGroups=netdev
WorkingDirectory=${INSTALL_DIR}
ExecStart=${INSTALL_DIR}/ih53ev-dashboard --iface can0 --listen :10000 --canmap ${INSTALL_DIR}/canmap.yaml
Restart=always
RestartSec=2
AmbientCapabilities=CAP_NET_RAW
CapabilityBoundingSet=CAP_NET_RAW
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable ih53ev-dashboard.service ih53ev-browser.service
systemctl restart ih53ev-dashboard.service
if systemctl is-active --quiet graphical.target; then
	systemctl restart ih53ev-browser.service
fi

echo
echo "Installed for user ${APP_USER}."
echo "  Service: systemctl status ih53ev-dashboard"
echo "  Browser: systemctl status ih53ev-browser"
echo "  Logs:    journalctl -u ih53ev-dashboard -f"
echo "  URL:     http://127.0.0.1:10000"
if [[ "${CONFIG_NEEDS_REBOOT}" -eq 1 ]]; then
	echo
	echo "Reboot required — boot config changed (PiCAN 3 SPI/CAN)."
	if [[ -t 0 ]]; then
		read -r -p "Reboot now? [Y/n] " ans
		if [[ -z "${ans}" || "${ans}" =~ ^[Yy]$ ]]; then
			reboot
		fi
	fi
	echo "Run: sudo reboot"
fi
