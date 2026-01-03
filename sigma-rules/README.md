# SIEMLess Sigma Rules Repository

**Purpose**: Central repository for Sigma rules, including original SigmaHQ rules and Sigma+ enhanced rules

**Last Updated**: January 3, 2026

---

## Directory Structure

```
sigma-rules/
├── README.md                    # This file
├── index.yaml                   # Index of all rules
├── original/                    # Original SigmaHQ rules (3,000+)
│   ├── windows/                 # Windows detection rules
│   │   ├── process_creation/
│   │   ├── security/
│   │   ├── powershell/
│   │   └── ...
│   ├── linux/                   # Linux detection rules
│   ├── cloud/                   # Cloud provider rules
│   ├── network/                 # Network traffic rules
│   └── ...
│
└── sigma-plus/                  # Sigma+ Enhanced rules
    ├── windows/
    ├── linux/
    ├── cloud/
    └── ...
```

## What is Sigma+?

Sigma+ is an extension to standard Sigma rules that adds:

| Extension | Purpose |
|-----------|---------|
| AGGREGATION | Count-based detection (e.g., "5+ failed logins in 1 minute") |
| SEQUENCE | Ordered event chains (e.g., "login → privesc → lateral movement") |
| TIME_WINDOW | Temporal constraints between events |
| CORRELATION | Cross-log correlation (e.g., network + endpoint) |
| TRANSFORMATION | Field value transformations (base64 decode, regex extract) |

### Sigma+ Example

```yaml
title: Privileged Account Brute Force Attack Detection
# ... standard Sigma fields ...

# Sigma+ Extensions
x-siemless-plus:
  aggregation:
    count: selection
    groupby:
      - TargetUserName
      - SourceIP
    condition: "> 5"
    timespan: 5m
  sequence:
    - failed_login
    - successful_login
    ordered: true
    maxspan: 15m
```

## Statistics

| Category | Original | Sigma+ | Total |
|----------|----------|--------|-------|
| Windows | - | - | - |
| Linux | - | - | - |
| Cloud | - | - | - |
| Network | - | - | - |
| **Total** | - | - | - |

*Statistics auto-updated via sync script*

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

## Enhancement Pipeline

Rules in `sigma-plus/` have been enhanced through the SIEMLess Sigma+ Enhancement Pipeline:

1. **NORMALIZE** - Map vendor fields to Sigma taxonomy
2. **LOGIC_COMPLETION** - Fix incomplete detection logic
3. **METADATA_ENRICHMENT** - Add MITRE ATT&CK, descriptions, false positives
4. **SIGMA_PLUS_EXTENSION** - Add aggregation, sequence, correlation
5. **VALIDATION** - Verify enhanced rule quality

Typical enhancement metrics:
- **Quality improvement**: +25-40 points
- **Cost**: ~$0.06 per rule
- **Duration**: ~14 seconds per rule

## Source

- **Original**: [SigmaHQ/sigma](https://github.com/SigmaHQ/sigma)
- **Enhanced**: SIEMLess AI Enhancement Pipeline

## License

- Original Sigma rules: [SigmaHQ License](https://github.com/SigmaHQ/sigma/blob/master/LICENSE)
- Sigma+ extensions: Proprietary - SIEMLess Technologies
