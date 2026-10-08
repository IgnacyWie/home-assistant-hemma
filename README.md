# Home Assistant Hemma Setup

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.9%2B-18BCF2?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![Hemma](https://img.shields.io/badge/dashboard-Hemma-111111)](https://github.com/willsanderson/Hemma)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

My responsive Home Assistant setup built on [Hemma](https://github.com/willsanderson/Hemma), with an Apple Home-inspired room layout, physical TV controls, Jellyfin Now Playing, custom lighting tiles, energy monitoring, and phone/desktop layouts from one YAML dashboard.

![Desktop and mobile dashboard](docs/screenshots/hero.jpg)

## Highlights

- Five room views with shared text-and-underline navigation
- Responsive desktop, tablet, and phone layouts
- Jellyfin playback metadata, artwork, progress, and transport controls
- Separate physical TV power controls and Android TV app launchers
- Custom HomeKit TV wrapper with iPhone Remote key forwarding
- Smart light-group toggles that restore the previous member state
- Energy monitoring with a monotonic utility meter
- Wake-up alarm controls and a dedicated stop action
- IKEA BILRESA bedside remote with progressive night lighting and whole-home bedtime shutdown
- Apple-first typography using the native San Francisco system font where available
- Custom SVG icon set and room artwork

## Screenshots

### Desktop

![Living Room desktop dashboard](docs/screenshots/desktop-living-room.jpg)

### Phone

<p align="center">
  <img src="docs/screenshots/mobile-living-room.jpg" width="360" alt="Living Room phone dashboard">
</p>

## Repository layout

```text
config/
├── automations.yaml             # Household automations and physical remote mappings
├── custom_components/hemma/   # Hemma integration snapshot with local tweaks
├── dashboards/
│   ├── hemma/hemma.yaml       # Room and entity configuration
│   └── templates/             # Cards, badges, popups and responsive layouts
├── packages/
│   ├── hemma_helpers.yaml     # Helpers, scripts and dashboard automations
│   └── homekit_tv.yaml        # TV wrapper and remote-key forwarding
├── themes/hemma/              # Hemma theme and typography
└── www/hemma/                 # Icons and room images
```

## Automations

[`config/automations.yaml`](config/automations.yaml) is the source-controlled
copy of the active `/config/automations.yaml` file. It currently contains:

- **Bathroom Fan - Delay** — turns off the bathroom fan 20 minutes after it is
  switched on.
- **Wake up with music - Zeppelin** — switches on the Lelit espresso machine,
  then plays *Guten Morgen Sonnenschein* at the configured wake-up time when
  the wake-up helper is enabled.
- **Stop wake-up music** — stops only the Zeppelin from the dashboard stop
  button; the espresso machine remains on.
- **Bedroom - BILRESA bedside remote** — maps the IKEA `09B9` ZHA remote:
  - Single ON from 06:00 through 22:59 keeps the daytime behavior: Bed Lamp and
    LED Bed first, then Bedroom Accent.
  - Single ON from 23:00 through 05:59 progressively enables LED Bed, Bed Lamp,
    and Bedroom Accent.
  - Single OFF turns off all three bedroom lights.
  - Double ON turns on all three bedroom lights.
  - Double OFF performs the bedtime shutdown for enabled, visible household
    devices: dashboard lights, the Lelit espresso machine, the bathroom fan,
    Zeppelin playback, and the living-room TV. Hidden, disabled, diagnostic,
    and infrastructure entities are intentionally excluded.
  - While the configured wake-up alarm is playing, any mapped button press
    stops only the alarm without changing lights, running the bedtime shutdown,
    or switching off the espresso machine.

## Kitchen dashboard

The Kitchen view is included in the shared room navigation on desktop, tablet,
and phone. It contains a dedicated **Lelit Espresso Machine** switch tile using
an espresso-maker silhouette. The tile controls the IKEA GRILLPLATS plug and
reports its current on/off state.

## Configuration change workflow

For every Home Assistant automation or other YAML change:

1. Back up the live file and edit a fresh copy from `/config`.
2. Update the matching file in this repository and document changed behavior
   in this README.
3. Deploy the reviewed YAML and run `ha core check`.
4. Reload the affected domain or restart Home Assistant, then verify the live
   entity or automation.
5. Scan the repository for secrets, commit only the intended files, and push to
   `IgnacyWie/home-assistant-hemma` on `main`.

## Requirements

- Home Assistant **2026.9.0 or newer**
- [HACS](https://hacs.xyz/)
- [UIX](https://github.com/Lint-Free-Technology/uix) — required
- [button-card](https://github.com/custom-cards/button-card) — required
- [apexcharts-card](https://github.com/RomRider/apexcharts-card) — used by chart popups
- [Kiosk Mode](https://github.com/NemesisRE/kiosk-mode) — used by the YAML dashboard
- The Date & Time integration with a time sensor, if you want the room clock

> [!IMPORTANT]
> This is a real configuration snapshot, not a drop-in generic dashboard. Replace every example entity ID in `config/dashboards/hemma/hemma.yaml` and the package files with entities from your own Home Assistant instance before enabling it.

## Installation

### 1. Back up Home Assistant

Create a Home Assistant backup before copying any files.

### 2. Install frontend dependencies

Install UIX, button-card, apexcharts-card, and Kiosk Mode through HACS. Do not install `card-mod` alongside UIX unless you have separately verified that combination.

### 3. Copy the configuration

Copy the contents of this repository's `config/` directory into `/config/` on Home Assistant. Review changes first if those folders already exist.

The vendored `custom_components/hemma/` directory reproduces the dashboard shown here. If you prefer to track upstream Hemma through HACS, install [willsanderson/Hemma](https://github.com/willsanderson/Hemma) instead and port only the dashboard/theme overrides you need.

### 4. Enable packages, themes, and the YAML dashboard

Merge the relevant sections from [`configuration.example.yaml`](configuration.example.yaml) into your own `/config/configuration.yaml`.

### 5. Replace entity IDs

At minimum, review:

- `config/dashboards/hemma/hemma.yaml`
- `config/packages/homekit_tv.yaml`
- the energy entities in `config/packages/hemma_helpers.yaml`
- room images and view names
- Android TV package/activity IDs used by the Jellyfin and YouTube launch buttons

The published dashboard uses `person.example_user` as a privacy-safe placeholder.

### 6. Validate and restart

```bash
ha core check
ha core restart
```

After Home Assistant returns, select the **Hemma** theme from your profile and open the **Home** dashboard.

## TV architecture

The setup intentionally separates two responsibilities:

- `media_player.living_room_tv_2` controls physical television power and app launching.
- `media_player.tv_w_salonie_4` is the Jellyfin session used by Now Playing for reliable title, progress, episode metadata, and transport state.

The HomeKit wrapper exposes a stable TV source list and forwards Apple's standard remote keys to the Android TV remote entity.

## Security and privacy

No `.storage` files, databases, authentication data, tokens, internal URLs, or `secrets.yaml` are included. Personal presence entities were replaced with examples, and the one-time energy-meter calibration from the live system was intentionally removed.

Run your own secret scanner before publishing changes. Never commit Home Assistant backups, databases, `.storage`, `secrets.yaml`, access tokens, webhook IDs, or private certificates.

## Upstream and attribution

This repository is a personalized configuration built on [Hemma](https://github.com/willsanderson/Hemma) by [Will Sanderson](https://github.com/willsanderson), which is licensed under the MIT License. Hemma itself credits [Homio](https://github.com/iamtherufus/Homio) as the original concept and base implementation.

Local configuration and dashboard customizations are maintained by Ignacy Wielogórski. See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE).
