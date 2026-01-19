# SIEMLess Central Registry

Community-maintained log signatures for automatic vendor detection and field mapping.

## Statistics

- **Signature Files**: 79
- **Vendors**: 50+
- **Field Mappings**: 1,500+
- **Last Updated**: 2026-01-19

---

## What This Contains

Each signature file includes **both**:

1. **Signatures** - Regex patterns to identify log types
2. **Field Mappings** - Vendor fields → ECS/CIM/ASIM normalization

```yaml
signatures:
  - vendor: postgresql
    product: database
    primary_pattern: "LOG:|ERROR:|WARNING:"  # Pattern to match
    fields:
      - name: postgresql.log.client_addr     # Vendor field
        ecs: source.ip                        # Elastic Common Schema
        cim: src_ip                           # Splunk CIM
        asim: SrcIpAddr                       # Microsoft Sentinel ASIM
```

---

## Structure

```
signatures/
├── index.yaml                    # Master index
├── aws/                          # Cloud providers
│   ├── cloudtrail.yaml
│   ├── guardduty.yaml
│   ├── vpc-flow.yaml
│   └── ...
├── cisco/                        # Network vendors
│   ├── asa.yaml
│   ├── ftd.yaml
│   └── ios.yaml
├── microsoft/                    # Microsoft stack
│   ├── windows.yaml
│   ├── defender-for-endpoint.yaml
│   └── ...
├── ot/                           # OT/ICS protocols
│   ├── modbus.yaml
│   ├── dnp3.yaml
│   └── ...
└── ...
```

---

## Vendor Coverage

| Category | Vendors |
|----------|---------|
| **Firewalls** | Cisco ASA/FTD, Fortinet FortiGate, Palo Alto PAN-OS, Check Point, pfSense, SonicWall, Sophos, WatchGuard |
| **Cloud** | AWS (5), Azure (4), GCP (2) |
| **Identity** | Okta, Auth0, Azure AD/Entra ID, CyberArk PAS |
| **Endpoint** | CrowdStrike, Microsoft Defender, SentinelOne, Carbon Black, Sysmon |
| **Network** | Cisco IOS/Meraki, Juniper (6), Zeek, Suricata |
| **Web/Proxy** | Nginx, Apache, IIS, Traefik, HAProxy, Squid, Cloudflare, ModSecurity |
| **Database** | PostgreSQL, MongoDB |
| **SaaS** | Google Workspace, Office 365, Salesforce, Zoom |
| **Containers** | Kubernetes, Docker |
| **OT/ICS** | Modbus, DNP3, BACnet, OPC-UA, S7comm, IEC-104, Profinet, Ethernet/IP, MMS |
| **Threat Intel** | MISP |

---

## Usage

### Sync to SIEMLess Instance

```bash
# Via API
curl -X POST "https://your-instance/api/v1/ingestion/log-signatures/sync/github" \
  -H "Authorization: Bearer <token>"

# Via UI
Platform > Resource Hub > Log Signatures > "Sync from GitHub"
```

### Manual Import

```bash
# Import specific vendor
curl -X POST "https://your-instance/api/v1/ingestion/log-signatures/import" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @signatures/cisco/asa.yaml
```

---

## Contributing

### Adding New Vendor Signatures

1. **Find Documentation** - Elastic Filebeat docs, vendor docs, or SigmaHQ
2. **Create YAML File** - `signatures/{vendor}/{product}.yaml`
3. **Include Both**:
   - Signatures with regex patterns
   - Field mappings with ECS/CIM/ASIM
4. **Validate YAML** - Patterns with colons must be quoted!
5. **Submit PR**

### YAML Template

```yaml
# {Vendor} {Product} - Log Signatures
# Source: {Documentation URL}

signatures:
  - vendor: {vendor}
    product: {product}
    log_type: {type}
    signature_name: {Name}
    primary_pattern: "{regex}"     # QUOTE if contains colons!
    confidence: 0.95
    priority: 5
    fields:
      - name: {vendor}.{field}
        type: keyword
        ecs: {ecs_field}
        cim: {cim_field}
        asim: {asim_field}
        description: {description}

metadata:
  vendor: {Vendor}
  product: {Product}
  documentation_url: {URL}
  created_date: "{YYYY-MM-DD}"
```

### Validation

```bash
# Validate all YAML files
python -c "
import yaml, os
for root, dirs, files in os.walk('signatures'):
    for f in files:
        if f.endswith('.yaml'):
            path = os.path.join(root, f)
            try:
                yaml.safe_load(open(path).read())
                print(f'OK: {path}')
            except yaml.YAMLError as e:
                print(f'ERROR: {path}: {e}')
"
```

---

## Sigma Rules

Detection rules for threat identification in parsed logs.

- **Location**: `sigma-rules/`
- **Total Rules**: 3,067+
- **Documentation**: [sigma-rules/README.md](sigma-rules/README.md)

---

## Related Projects

- **SIEMLess v3** - Main platform (proprietary)
- **SigmaHQ** - Community detection rules
- **Elastic Filebeat** - Log shipping with field definitions

---

## License

Proprietary - SIEMLess Technologies
