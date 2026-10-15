# Architecture diagrams

These diagrams document the repository at three levels:

| Diagram | Purpose | Editable source |
| --- | --- | --- |
| [System architecture](system-architecture.svg) | Shows how clients, Home Assistant Core, Lovelace, the Hemma integration, dashboard YAML, and local assets fit together. | [`system-architecture.excalidraw`](system-architecture.excalidraw) |
| [Network topology and observability](network-observability.svg) | Shows the logical network path and how WAN, ping/status, wired, and Wi-Fi entities feed the Hemma network card and popup. Hardware names are intentionally generic because they are deployment-specific. | [`network-observability.excalidraw`](network-observability.excalidraw) |
| [Automation and safety control plane](automation-control-plane.svg) | Shows representative humidity, household-action, and cinema-mode paths from event to guarded action. | [`automation-control-plane.excalidraw`](automation-control-plane.excalidraw) |

The `.excalidraw` files are the source of truth and can be edited in the Excalidraw app or at [excalidraw.com](https://excalidraw.com/). The SVG files are generated previews for GitHub and documentation.

## Regenerating previews

With [`excalidraw-cli`](https://www.npmjs.com/package/excalidraw-cli) and [`@moona3k/excalidraw-export`](https://www.npmjs.com/package/@moona3k/excalidraw-export) installed:

```bash
excalidraw --version
excalidraw-export docs/diagrams/system-architecture.excalidraw \
  --svg -o docs/diagrams/system-architecture.svg
```

Repeat the export command for the other editable files after changing them.
