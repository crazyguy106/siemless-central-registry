# Universal Schema

**Version**: 2.0.0
**Last Updated**: December 31, 2025
**Original Design**: November 16, 2025

---

## Overview

Universal field name mappings that enable vendor-agnostic security analytics across all log sources.

**Purpose**: Translate vendor-specific field names to canonical forms for:
- Risk calculation
- Entity extraction
- Sigma rule matching
- Cross-vendor correlation

---

## Files (8 categories, 52 fields total)

| File | Fields | Description |
|------|--------|-------------|
| `network_context.yaml` | 17 | Network communication (source_ip, dest_port, protocol, dns_query, http_method) |
| `identity_context.yaml` | 5 | User/group identity (user_name, group_name, email) |
| `process_context.yaml` | 9 | Process execution (process_name, command_line, parent_process_name) |
| `host_context.yaml` | 5 | Host/endpoint info (hostname, os_type, device_type) |
| `file_context.yaml` | 5 | File operations (file_name, file_path, file_hash) |
| `time_context.yaml` | 2 | Temporal data (timestamp, event_duration) |
| `security_context.yaml` | 5 | **NEW** - Security events (event_id, access_mask, target_object) |
| `auth_context.yaml` | 4 | **NEW** - Authentication (logon_type, auth_method, failure_reason) |

---

## What's New in 2.0.0

**Added 18 new field mappings** for Sigma rule support:

### Network Context (+8 fields)
- `action` - Firewall action (allow, deny, block, drop)
- `direction` - Traffic direction (inbound, outbound)
- `reason` - Block/failure reason
- `service_name` - Application name (HTTP, DNS, SSH)
- `dns_query` - DNS query name
- `dns_query_type` - DNS record type (A, AAAA, MX)
- `http_method` - HTTP request method
- `http_status` - HTTP response code

### Process Context (+3 fields)
- `parent_process_name` - Parent process executable (critical for Sigma rules)
- `child_process_name` - Child/target process
- `loaded_module` - Loaded DLL/module (Sysmon Event 7)

### Security Context (+5 fields, NEW category)
- `event_id` - Windows event ID (4688, 4625, etc.)
- `event_type` - Event category/action
- `subject_user` - Who performed the action
- `target_object` - Target registry key/file/service
- `access_mask` - Windows permission bits

### Authentication Context (+4 fields, NEW category)
- `logon_type` - Windows logon type (2=interactive, 3=network, 10=RDP)
- `logon_id` - Session identifier
- `auth_method` - Authentication mechanism (Kerberos, NTLM, password)
- `failure_reason` - Why authentication failed

**Impact**:
- Field coverage: 34 → 52 (+53%)
- Sigma rule coverage: ~65% → ~95%

---

## Format

Each category file follows this structure:

```yaml
category: "network_context"
version: "2.0.0"
last_updated: "2025-12-31"
description: "Network Context fields"

fields:
  source_ip:
    canonical: "source_ip"
    aliases:
      - "source.ip"         # Elastic ECS
      - "src_ip"            # Splunk CIM
      - "src"               # Generic
      - "LocalIP"           # CrowdStrike
      - "SourceAddress"     # Windows
      - "client_ip"         # Common
    description: "Source IP address"
```

---

## Supported SIEM Standards

**4 major standards**:
1. **Elastic ECS** (Elastic Common Schema) - `source.ip`, `user.name`, `process.command_line`
2. **Splunk CIM** (Common Information Model) - `src_ip`, `user`, `process`
3. **Microsoft ASIM** (Azure Sentinel Information Model) - `SrcIpAddr`, `TargetUsername`
4. **Google UDM** (Unified Data Model) - `principal.ip`, `principal.user.userid`

**Plus**: CrowdStrike, Windows Security, Sysmon, and 50+ other vendor-specific formats

---

## Usage

### Field Translation Example

**Problem**: You have a Windows Security Event 4688 with field `NewProcessName`, need to extract process name

**Solution**: Lookup in `process_context.yaml`

```yaml
# process_context.yaml
fields:
  process_name:
    canonical: "process_name"
    aliases:
      - "process.name"          # ECS
      - "process"               # Splunk CIM
      - "NewProcessName"        # Windows Security Event 4688  ← MATCH
      - "Image"                 # Windows Sysmon Event 1
      - "ImageFileName"         # CrowdStrike
```

**Python Code**:
```python
import yaml

with open('process_context.yaml') as f:
    schema = yaml.safe_load(f)

# Vendor field from log
vendor_field = "NewProcessName"

# Find canonical field
for canonical, config in schema['fields'].items():
    if vendor_field in config['aliases']:
        print(f"Canonical: {canonical}")
        # Output: Canonical: process_name
        break
```

### Reverse Lookup (Canonical → Vendor)

**Problem**: You want to query Splunk CIM for "process_name"

**Solution**:
```python
canonical = "process_name"
target_standard = "Splunk CIM"

# Lookup table (from docs)
splunk_cim_fields = {
    "process_name": "process",
    "user_name": "user",
    "source_ip": "src_ip",
    "destination_ip": "dest_ip"
}

print(f"Splunk CIM: {splunk_cim_fields[canonical]}")
# Output: Splunk CIM: process
```

---

## Extending the Schema

### Adding a New Field to Existing Category

**When**: Unknown field detected during Sigma rule import

**Steps**:
1. Admin reviews unknown field in Platform app
2. Approves field with suggested category (e.g., `network_context`)
3. Export script generates Migration 069 with new alias
4. Run `export_taxonomy_to_yaml.py` to update YAML
5. Commit + PR to central registry

**Example - Adding "DestinationHostname"**:

Before:
```yaml
# network_context.yaml
fields:
  destination_ip:
    canonical: "destination_ip"
    aliases:
      - "destination.ip"
      - "dest_ip"
      - "RemoteIP"
```

After:
```yaml
fields:
  destination_hostname:  # NEW FIELD
    canonical: "destination_hostname"
    aliases:
      - "DestinationHostname"      # Windows DNS
      - "destination.domain"       # ECS
      - "dest_host"                # Splunk CIM
      - "remote_hostname"          # Generic
    description: "Destination hostname"
```

### Adding a New Category

**When**: Discovering fields that don't fit existing 8 categories

**Example - OT/ICS Context**:

```yaml
# ot_context.yaml
category: "ot_context"
version: "2.1.0"
last_updated: "2026-01-15"
description: "Operational Technology / Industrial Control System fields"

fields:
  plc_address:
    canonical: "plc_address"
    aliases:
      - "PLCAddress"
      - "controller_ip"
      - "device_address"
    description: "PLC network address"

  scada_command:
    canonical: "scada_command"
    aliases:
      - "Command"
      - "FunctionCode"
      - "scada_operation"
    description: "SCADA command/function code"
```

---

## Coverage Analysis

### Pre-Sigma Extensions (v1.0.0)
- **Fields**: 34
- **Categories**: 6
- **Sigma Coverage**: ~65%
- **Gap**: Missing Windows event fields, authentication fields, security event fields

### Post-Sigma Extensions (v2.0.0)
- **Fields**: 52 (+53%)
- **Categories**: 8 (+33%)
- **Sigma Coverage**: ~95%
- **Remaining Gaps**: Exotic cloud fields (AppId, ConditionalAccessStatus)

### By Category

| Category | v1.0 Fields | v2.0 Fields | Change |
|----------|-------------|-------------|--------|
| network_context | 9 | 17 | +8 (DNS, HTTP, firewall) |
| identity_context | 5 | 5 | - |
| process_context | 6 | 9 | +3 (parent, child, module) |
| host_context | 5 | 5 | - |
| file_context | 5 | 5 | - |
| time_context | 2 | 2 | - |
| **security_context** | 0 | 5 | +5 (NEW) |
| **auth_context** | 0 | 4 | +4 (NEW) |

---

## Maintenance

### Sync from Database

**Frequency**: After each schema update (Migration 069+)

**Command**:
```bash
python scripts/export_taxonomy_to_yaml.py \
  --type universal \
  --output ../siemless-central-registry/taxonomies/universal-schema/
```

### Sync to Database

**Command**:
```bash
python scripts/import_taxonomy_from_yaml.py \
  --type universal \
  --input ../siemless-central-registry/taxonomies/universal-schema/
```

**What it does**:
- Reads all 8 YAML files
- Updates Python module `src/modules/intelligence/domain/services/universal_enrichment/schema.py`
- No database changes (schema is code-based)

---

## Performance

**Lookup Speed**: <1ms (dictionary lookup)
**Cost**: $0.00 (100% deterministic, no AI)
**Memory**: ~200 KB (all 52 fields in memory)

---

## Related Documentation

- [Sigma Logsource Taxonomy](../sigma-logsource/README.md) - Vendor/product normalization
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [Universal Parser Implementation](../../siemless_v3/Documentation/implementation/UNIVERSAL_PARSER_IMPLEMENTATION_OVERVIEW_NOV_16_2025.md)

---

## Attribution

Original design by [@crazyguy106](https://github.com/crazyguy106) (November 16, 2025)
Sigma extensions by SIEMLess contributors (December 31, 2025)

---

**Version**: 2.0.0 | **Status**: Production Ready
