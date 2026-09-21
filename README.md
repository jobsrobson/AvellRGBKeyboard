# Avell RGB Keyboard

A native Linux application for controlling the **per-key RGB keyboard and front Lightbar of the Avell A60 MUV (also known as XMG/TUXEDO Fusion 15)**.

Built with **Python, GTK4 and libadwaita**, Avell RGB Keyboard provides a graphical interface for the RGB hardware exposed by the Linux `ite_8291` driver from the TUXEDO Drivers project.

> [!IMPORTANT]
> This project was developed and tested specifically on the **Avell A60 MUV running Linux**.
>
> Other Avell/Clevo/Tongfang models using compatible ITE 8291 hardware may work, but are currently **untested and unsupported**.

## Features

- Per-key RGB color control
- Visual keyboard layout
- Global keyboard brightness control
- Front Lightbar RGB control
- Native Lightbar animation toggle
- Live visual preview
- Custom lighting profiles
- GTK4/libadwaita interface
- Native GNOME integration
- No root privileges required during normal use after installing the included udev rules

## Hardware support

Currently tested on:

| Hardware | Status |
| --- | --- |
| Avell A60 MUV | ✅ Tested |
| ITE Tech. ITE 8291 RGB controller (`048d:ce00`) | ✅ Tested |
| Per-key RGB keyboard | ✅ Working |
| Front RGB Lightbar | ✅ Working |
| Other Avell/XMG/TUXEDO models | ⚠️ Untested |

The application expects the keyboard to be handled by the Linux `ite_8291` driver.

The tested keyboard exposes per-key LEDs through:

```text
/sys/class/leds/rgb:kbd_backlight
/sys/class/leds/rgb:kbd_backlight_1
...
/sys/class/leds/rgb:kbd_backlight_125
```

The Lightbar is exposed through:

```text
/sys/class/leds/lightbar_rgb:1:status
/sys/class/leds/lightbar_rgb:2:status
/sys/class/leds/lightbar_rgb:3:status
/sys/class/leds/lightbar_animation::status
```

## Requirements

Avell RGB Keyboard currently targets Linux systems with:

- Python 3
- GTK 4
- libadwaita
- PyGObject
- TUXEDO Drivers with `ite_8291` support
- A compatible ITE 8291 RGB keyboard

On Debian 13, the graphical dependencies can be installed with:

```bash
sudo apt install \
    python3 \
    python3-gi \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    meson \
    ninja-build
```

The TUXEDO `ite_8291` kernel driver must already be installed and working.

You can verify that the keyboard has been detected with:

```bash
ls /sys/class/leds/ | grep kbd_backlight
```

## Installation

Clone the repository:

```bash
git clone https://github.com/jobsr/AvellRGBKeyboard.git
cd AvellRGBKeyboard
```

Configure the build:

```bash
meson setup build --prefix=/usr
```

Install:

```bash
sudo meson install -C build
```

Reload the included udev rules:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Your user must belong to the `video` group:

```bash
sudo usermod -aG video "$USER"
```

Log out and log back in if the group was just added.

The application can then be launched from the desktop application menu or with:

```bash
avell-rgb-control
```

## Running from source

During development, the application can be launched directly from the repository:

```bash
./avell-rgb-control
```

## Permissions

RGB controls are exposed by the kernel through sysfs and are normally writable only by root.

The project includes:

```text
data/99-avell-rgb-control.rules
```

This udev rule grants members of the `video` group access to the required keyboard and Lightbar controls.

The application itself does **not** need to run as root.

## Profiles

Profiles are stored per user under:

```text
~/.config/avell-rgb-control/profiles/
```

A profile can store:

- Per-key RGB colors
- Keyboard brightness
- Lightbar state
- Lightbar color
- Lightbar animation state

## Project structure

```text
AvellRGBKeyboard/
├── data/
│   ├── 99-avell-rgb-control.rules
│   ├── io.github.jobsr.AvellRGBControl.desktop
│   ├── io.github.jobsr.AvellRGBControl.metainfo.xml
│   └── io.github.jobsr.AvellRGBControl.svg
├── scripts/
│   └── avell-rgb-control
├── src/
│   ├── pages/
│   │   ├── keyboard_page.py
│   │   ├── lightbar_page.py
│   │   └── profiles_page.py
│   ├── hardware.py
│   ├── keyboard.py
│   ├── lightbar.py
│   ├── main.py
│   ├── profiles.py
│   └── window.py
├── avell-rgb-control
├── meson.build
├── LICENSE
└── README.md
```

## How it works

The application does not implement a custom kernel driver.

Instead, it uses the interfaces exposed by the TUXEDO `ite_8291` driver.

The Avell A60 MUV keyboard provides a 6 × 21 RGB matrix, for a total of 126 LED channels. Each key color can be controlled through the Linux LED subsystem using its `multi_intensity` attribute.

RGB updates can be buffered through:

```text
controls/buffer_input
```

This allows multiple key colors to be prepared before committing the complete keyboard state.

Keyboard brightness is controlled independently through the LED subsystem's `brightness` attribute.

## Limitations

This is currently a hardware-specific project.

The physical key-to-LED mapping is based on the **Avell A60 MUV (with ABNT keyboard layout)**, and compatibility with other laptops has not yet been verified.

Native keyboard animation effects exposed internally by the ITE 8291 controller are not currently available in the application.

## Contributing

Testing on other Avell/XMG/TUXEDO notebooks using an ITE 8291 RGB controller is welcome.

If you test the application on another model, please include:

- Exact notebook model
- Linux distribution
- Kernel version
- USB ID of the RGB controller
- TUXEDO Drivers version
- Output of `ls /sys/class/leds/`

Hardware mappings may differ between notebook models, so do not assume that an apparently compatible controller uses the same physical key mapping.

## License

This project is licensed under the **GNU General Public License v3.0 or later**.

See [LICENSE](LICENSE) for details.

## Disclaimer

Avell RGB Keyboard is an independent community project.

It is not affiliated with, endorsed by, or supported by Avell or TUXEDO Computers.

Use it at your own risk.