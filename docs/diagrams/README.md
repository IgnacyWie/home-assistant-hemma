# Automation diagram

This diagram documents setup-specific automation behavior in the repository:

| Diagram | Purpose | Editable source |
| --- | --- | --- |
| [Automation and safety control plane](automation-control-plane.svg) | Shows representative humidity, household-action, and cinema-mode paths from event to guarded action. | [`automation-control-plane.excalidraw`](automation-control-plane.excalidraw) |

The `.excalidraw` files are the source of truth and can be edited in the Excalidraw app or at [excalidraw.com](https://excalidraw.com/). The SVG files are generated previews for GitHub and documentation.

## Regenerating previews

With [`excalidraw-cli`](https://www.npmjs.com/package/excalidraw-cli) and [`@moona3k/excalidraw-export`](https://www.npmjs.com/package/@moona3k/excalidraw-export) installed:

```bash
excalidraw --version
excalidraw-export docs/diagrams/automation-control-plane.excalidraw \
  --svg -o docs/diagrams/automation-control-plane.svg
```
