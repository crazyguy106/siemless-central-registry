# SIEMLess Central Registry

A community-driven registry of shared knowledge for SIEMLess instances.

## Overview

The Central Registry provides curated, version-controlled configurations that sync to all SIEMLess deployments:

- **Vendor Documentation URLs** - Discovered documentation benefits all users
- **AI Model Configurations** - Task mappings, pricing, family policies
- **Parser Templates** - Pre-built parsers for common vendors (coming soon)
- **SIEM Schema Mappings** - Field transformations per SIEM (coming soon)

## Repository Structure

```
siemless-central-registry/
├── registry.json              # Master index with version + checksums
├── README.md                  # This file
│
├── vendor-docs/               # Curated vendor documentation URLs
│   ├── crowdstrike/
│   │   └── falcon.yaml
│   ├── paloalto/
│   │   └── firewall.yaml
│   ├── microsoft/
│   │   └── defender.yaml
│   ├── elastic/
│   │   └── elasticsearch.yaml
│   └── splunk/
│       └── enterprise.yaml
│
├── ai-config/                 # AI model configurations
│   ├── models.yaml            # Model catalog with pricing
│   ├── task-mappings.yaml     # Task → model routing
│   └── family-policies.yaml   # Version locking rules
│
├── parsers/                   # Parser templates (coming soon)
│   └── .gitkeep
│
└── siem-schemas/             # SIEM field mappings (coming soon)
    ├── elastic/
    ├── splunk/
    └── sentinel/
```

## How Sync Works

### 1. Startup Sync
When a SIEMLess instance starts, it fetches the latest registry:

```python
registry = fetch("https://raw.githubusercontent.com/.../registry.json")
if registry.checksums != local_checksums:
    sync_all_sections()
```

### 2. Periodic Sync
A background worker syncs every 6 hours:
- Compares checksums to detect changes
- Only downloads updated sections
- Falls back to local cache if GitHub unreachable

### 3. Contribution (Optional)
Users can contribute discovered documentation:
1. Parser Workflow discovers new documentation URL
2. User clicks "Share with community"
3. SIEMLess creates PR to this repo
4. Maintainers review and merge
5. All users get the update on next sync

## Usage

### Fetching Registry Data

```python
import yaml
import requests

REGISTRY_URL = "https://raw.githubusercontent.com/crazyguy106/siemless-central-registry/main"

# Fetch vendor docs
response = requests.get(f"{REGISTRY_URL}/vendor-docs/crowdstrike/falcon.yaml")
vendor_docs = yaml.safe_load(response.text)

# Fetch AI task mappings
response = requests.get(f"{REGISTRY_URL}/ai-config/task-mappings.yaml")
task_mappings = yaml.safe_load(response.text)

# Get model for a task
task = "rule_enhancement"
model_config = task_mappings["task_mappings"].get(task)
print(f"Use {model_config['model']} from {model_config['provider']}")
```

### Vendor Documentation Format

```yaml
vendor: crowdstrike
products:
  - name: falcon_edr
    documentation_urls:
      - url: https://docs.crowdstrike.com/falcon-edr/latest/
        doc_type: api_reference
        confidence: 0.95
        last_verified: 2025-12-24
```

### Task Mapping Format

```yaml
task_mappings:
  rule_enhancement:
    model: gemini-2.5-flash
    provider: google
    reason: "100% quality, 8.7x cheaper than Claude"
    strategy: single
```

## Contributing

### Adding Vendor Documentation

1. Fork this repository
2. Add/update YAML file in `vendor-docs/{vendor}/{product}.yaml`
3. Update `registry.json` stats
4. Create pull request

### Documentation URL Schema

```yaml
- url: https://example.com/docs
  doc_type: field_reference | api_reference | user_guide | schema_reference
  confidence: 0.0-1.0
  last_verified: YYYY-MM-DD
  notes: Optional description
```

### Updating AI Configurations

AI configurations are maintained by the SIEMLess team. If you notice:
- Outdated pricing
- Deprecated models
- Better task mappings

Please open an issue with your suggestion.

## Offline / Air-Gapped Deployments

For air-gapped environments:

1. Clone this repository to your internal Git server
2. Configure `REGISTRY_URL` to point to your internal server
3. Manually sync periodically

```bash
REGISTRY_URL=https://internal-git.company.com/siemless-registry/main
```

## Stats

| Category | Count |
|----------|-------|
| Vendors | 5 |
| Products | 8 |
| AI Models | 9 |
| Task Mappings | 13 |
| Parsers | Coming soon |

## License

MIT License - Free to use, modify, and distribute.

## Links

- [SIEMLess Documentation](https://docs.besiemless.ai)
- [SIEMLess Demo](https://demo.besiemless.ai)
- [Report Issues](https://github.com/crazyguy106/siemless-central-registry/issues)