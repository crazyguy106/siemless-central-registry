# SIEMLess Log Signatures - GitHub Resource Hub

Auto-generated from local signature extraction.

## Statistics

- **Total Signatures**: 6,263
- **Total Files**: 5
- **Vendors**: 4
- **Generated**: 2025-12-31 00:20

## Structure

```
signatures/
├── index.yaml          # Index of all signatures
├── check-point/
│   └── security-gateway.yaml
├── cisco/
│   ├── asa.yaml
│   └── asa.yaml
├── fortinet/
│   └── fortigate.yaml
├── microsoft/
│   └── windows.yaml
```

## Files

| Vendor | Product | Signatures | Categories |
|--------|---------|------------|------------|
| Check Point | Security Gateway | 15 | firewall, threat_prevention, url_filtering... |
| Cisco | ASA | 2,341 | Authentication, Other, Failover... |
| Cisco | ASA | 2,341 | Authentication, Other, Failover... |
| Fortinet | FortiGate | 1,155 | activexfilter, analytics, anomaly... |
| Microsoft | Windows | 411 | Account Logon, Account Management, DS Access... |

## Usage

### Sync to SIEMLess Instance

```bash
# Via Resource Hub UI
1. Navigate to Platform > Resource Hub > Log Signatures
2. Click "Sync from GitHub"

# Via API
curl -X POST "https://your-instance/api/v1/ingestion/log-signatures/sync/github" \
  -H "Authorization: Bearer <token>"
```

### Manual Import

```bash
# Import specific vendor
curl -X POST "https://your-instance/api/v1/ingestion/log-signatures/import" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @signatures/cisco/asa.yaml
```

## Source

Generated from vendor documentation using SIEMLess signature extraction tools.
Local working copies: `config/log-signatures/*.json` (gitignored)

## License

Proprietary - SIEMLess Technologies
