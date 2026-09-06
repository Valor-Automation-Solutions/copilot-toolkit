# Microsoft 365 declarative agent packages

These ZIP files are **Microsoft 365 declarative agent** app packages (Teams/M365
app package format) for sideload or import testing.

They are **NOT** Copilot Studio solution exports (`.zip` solution packages from
Power Platform / Copilot Studio).

## Schema versions chosen (as of 2026 research)

| Layer | Version | Why |
| --- | --- | --- |
| Teams / M365 app manifest | **1.22** | First version that added `copilotAgents` for declarative agents (replaces deprecated `copilotExtensions.declarativeCopilots`). Schema: `https://developer.microsoft.com/json-schemas/teams/v1.22/MicrosoftTeams.schema.json` |
| Declarative agent manifest | **v1.8** | Current documented declarative-agent schema on Microsoft Learn (2026). Schema: `https://developer.microsoft.com/json-schemas/copilot/declarative-agent/v1.8/schema.json` |

Each package contains:

- `manifest.json` — app identity, icons, `copilotAgents.declarativeAgents`
- `declarativeAgent.json` — agent name, instructions file ref, capabilities, starters
- `color.png` (192×192) and `outline.png` (32×32)
- `instructions/system_prompt.md` — Hebrew role instructions (referenced as `$[file('instructions/system_prompt.md')]`)

## What was validated in this environment

For each ZIP we locally verified:

1. Archive lists the five required paths above
2. `json.loads` succeeds on both JSON files (including Hebrew with gershayim `״`, not ASCII `"`)
3. Manifest `id` is a UUID; short name ≤30; full name ≤100
4. Icons exist and match expected pixel sizes
5. Instructions file exists and the `$[file(...)]` path resolves inside the package

## What was NOT validated

- **Live import into Microsoft 365 Copilot / Teams sideload was NOT tested** in this environment.
- Tenant admin policies, Copilot license requirements, and store publication were not exercised.
- SharePoint/OneDrive grounding with real tenant URLs was not configured (capability is declared open-ended).

## Packages

| File | Department |
| --- | --- |
| `finance_agent.zip` | Finance / cashflow |
| `hr_agent.zip` | HR / policy |
| `logistics_agent.zip` | Logistics / SLA |
| `procurement_agent.zip` | Procurement / invoices |
