# SIEMLess Sigma Rules Repository

**Purpose**: Central repository for Sigma detection rules from multiple sources

**Last Updated**: January 20, 2026

---

## Directory Structure

```
sigma-rules/
├── README.md                    # This file
├── index.yaml                   # Index of all rules
├── sigmahq/                     # Original SigmaHQ rules (3,000+)
│   ├── windows/                 # Windows detection rules
│   ├── linux/                   # Linux detection rules
│   ├── cloud/                   # Cloud provider rules
│   ├── network/                 # Network traffic rules
│   ├── application/             # Application-specific rules
│   └── ...
│
├── community/                   # Community-contributed rules (4,600+)
│   ├── splunk/                  # From Splunk Security Content
│   ├── wazuh/                   # From Wazuh
│   ├── chronicle/               # From Google Chronicle
│   ├── azure-sentinel/          # From Microsoft Sentinel
│   ├── bert-jan-hunting/        # From Bert-JanP hunting queries
│   └── mdecrevoisier/           # From mdecrevoisier
│
├── converted/                   # Vendor rules converted to Sigma (1,100+)
│   └── elastic/                 # Elastic detection rules converted
│
├── manual/                      # Manually created custom rules
│
└── sigma-plus/                  # Reserved for future Sigma+ enhanced rules
```

## Folder Descriptions

| Folder | Source | Description |
|--------|--------|-------------|
| `sigmahq/` | [SigmaHQ/sigma](https://github.com/SigmaHQ/sigma) | Official SigmaHQ rules - auto-synced weekly |
| `community/` | Multiple sources | Enhanced rules from security vendors and researchers |
| `converted/` | Elastic, etc. | Vendor detection rules converted to Sigma format |
| `manual/` | Custom | Hand-crafted rules for specific use cases |
| `sigma-plus/` | Future | Reserved for AI-enhanced rules |

## Automatic Sync

SigmaHQ rules are automatically synced every Sunday at 2 AM UTC via GitHub Actions.

**Flow:**
```
SigmaHQ/sigma (GitHub)
    ↓ Weekly cron
siemless-central-registry/sigma-rules/sigmahq/
    ↓ Auto-commit
SIEMLess database (via sync_from_local_registry.py)
```

## Statistics

See `index.yaml` for current rule counts by source and category.

## Sync to SIEMLess Instance

### Via Resource Hub UI
1. Navigate to **Platform > Resource Hub > Sigma Rules**
2. Click **"Sync from GitHub"**
3. Select categories to sync

### Via API
```bash
# Sync all rules
curl -X POST "https://your-instance/api/v1/detection/sigma-rules/sync/github" \
  -H "Authorization: Bearer <token>"

# Sync specific category
curl -X POST "https://your-instance/api/v1/detection/sigma-rules/sync/github" \
  -H "Authorization: Bearer <token>" \
  -d '{"categories": ["windows", "linux"]}'
```

### Via CLI (On-Prem)
```bash
python scripts/sync_from_local_registry.py \
  --path /opt/siemless/data/siemless-central-registry \
  --sigma
```

## License

- SigmaHQ rules: [Detection Rule License (DRL) 1.1](https://github.com/SigmaHQ/sigma/blob/master/LICENSE)
- Community rules: Various (see individual rule files)
- Converted rules: Original vendor licenses apply