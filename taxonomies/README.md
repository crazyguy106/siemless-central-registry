# SIEMLess Taxonomies

**Purpose**: Version-controlled normalization standards for cross-installation consistency

**Last Updated**: December 31, 2025

---

## Overview

This folder contains YAML-based taxonomies that enable:

1. **Sigma Logsource Normalization** - Canonical vendor/product names with aliases
2. **Universal Schema Field Mappings** - Vendor-agnostic field name translations
3. **Cross-Installation Sync** - Pull latest standards from GitHub
4. **Community Contributions** - Discover → contribute → merge workflow

---

## Folder Structure

```
taxonomies/
├── sigma-logsource/          # Sigma Specification 2.0 taxonomy
│   ├── products.yaml         # 71 canonical products (aws, windows, paloalto, etc.)
│   ├── categories.yaml       # 24 canonical categories (process_creation, etc.)
│   ├── services.yaml         # Canonical services (security, sysmon, etc.)
│   └── README.md
├── universal-schema/         # Universal field name mappings
│   ├── network_context.yaml  # Network fields (source_ip, dest_port, etc.)
│   ├── identity_context.yaml # Identity fields (user_name, group_name, etc.)
│   ├── process_context.yaml  # Process fields (process_name, command_line, etc.)
│   ├── host_context.yaml     # Host fields (hostname, os_type, etc.)
│   ├── file_context.yaml     # File fields (file_path, file_hash, etc.)
│   ├── time_context.yaml     # Time fields (timestamp, event_time, etc.)
│   ├── security_context.yaml # Security fields (event_id, access_mask, etc.) - NEW
│   ├── auth_context.yaml     # Auth fields (logon_type, auth_method, etc.) - NEW
│   └── README.md
├── CHANGELOG.md              # Version history
└── README.md                 # This file
```

---

## Sigma Logsource Taxonomy

**Based on**: [Sigma Specification 2.0 Appendix](https://sigmahq.io/sigma-specification/specification/sigma-appendix-taxonomy.html)

**Purpose**: Normalize vendor/product names for Sigma rule matching

**Format**:
```yaml
# products.yaml
products:
  - canonical: "windows"
    type: "os"
    aliases:
      - "Windows"
      - "WINDOWS"
      - "Microsoft Windows"
      - "Win"
    description: "Microsoft Windows operating system"
    sigma_spec_url: "https://sigmahq.io/docs/basics/log-sources.html#windows"
```

**Coverage**:
- 14 cloud providers (aws, azure, gcp, m365, okta, etc.)
- 12 operating systems (windows, linux, macos, etc.)
- 7 network devices (cisco, paloalto, fortinet, etc.)
- 8 applications (apache, iis, nginx, etc.)
- 6 generic categories (firewall, proxy, antivirus, etc.)
- 24 log source categories (process_creation, network_connection, dns_query, etc.)

---

## Universal Schema

**Based on**: SIEMLess multi-standard field mapping architecture

**Purpose**: Translate vendor-specific field names to canonical forms

**Format**:
```yaml
# network_context.yaml
category: "network_context"
description: "Network communication fields"
last_updated: "2025-12-31"
version: "2.0"

fields:
  source_ip:
    canonical: "source_ip"
    description: "Source IP address"
    aliases:
      - source.ip         # Elastic ECS
      - src_ip            # Splunk CIM
      - src              # Generic
      - SourceIP         # Windows
      - LocalIP          # CrowdStrike
      - client_ip        # Common
```

**Coverage**:
- 52 total fields (was 34 before Sigma extensions)
- 8 categories (was 6 before Sigma extensions)
- 200+ vendor aliases per category
- 4 SIEM standards: ECS, CIM, ASIM, UDM

---

## Versioning

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (field removal, canonical rename)
- **MINOR**: Non-breaking additions (new fields, new aliases)
- **PATCH**: Corrections (typo fixes, description updates)

**Current Versions**:
- Sigma Logsource Taxonomy: `2.0.0` (Sigma Spec 2.0 baseline)
- Universal Schema: `2.0.0` (Sigma extensions Dec 31, 2025)

**See**: [CHANGELOG.md](./CHANGELOG.md) for detailed version history

---

## Sync Workflow

### Installation → Registry (Discovery)

When SIEMLess instances discover unknown fields during rule imports:

1. **Detection**: Unknown field logged to `unknown_fields_for_review` table
2. **Admin Review**: Platform app → approve/reject field
3. **Local Update**: Migration adds field to local Universal Schema
4. **Contribution**: Export to YAML → GitHub PR to central registry
5. **Community Review**: Maintainers review → merge if valid
6. **Distribution**: All installations pull updated taxonomy

### Registry → Installation (Sync)

Periodic sync (startup + every 6 hours):

1. **Fetch**: GET `https://raw.githubusercontent.com/crazyguy106/siemless-central-registry/main/taxonomies/...`
2. **Compare**: Check if registry version > local version
3. **Apply**: Import YAML → update local database (migrations)
4. **Log**: Record sync timestamp + version

---

## Conversion Scripts

**Location**: `siemless_v3/scripts/`

### Export (DB → YAML)
```bash
# Export Sigma taxonomy
python scripts/export_taxonomy_to_yaml.py --type sigma --output ../siemless-central-registry/taxonomies/sigma-logsource/

# Export Universal Schema
python scripts/export_taxonomy_to_yaml.py --type universal --output ../siemless-central-registry/taxonomies/universal-schema/
```

### Import (YAML → DB)
```bash
# Import Sigma taxonomy
python scripts/import_taxonomy_from_yaml.py --type sigma --input ../siemless-central-registry/taxonomies/sigma-logsource/

# Import Universal Schema
python scripts/import_taxonomy_from_yaml.py --type universal --input ../siemless-central-registry/taxonomies/universal-schema/
```

---

## Contributing

### Discover New Field
1. Import Sigma rules → unknown field detected
2. Admin reviews field in Platform app
3. Approve field → added to local schema

### Contribute to Registry
1. Run export script: `python scripts/export_taxonomy_to_yaml.py`
2. Create branch: `git checkout -b add-field-{field_name}`
3. Commit YAML: `git add taxonomies/ && git commit -m "Add {field_name} to {category}"`
4. Push + PR: `git push origin add-field-{field_name}`
5. Maintainer review → merge

### Pull Latest
1. Automatic: Sync service runs every 6 hours
2. Manual: `python scripts/sync_taxonomy_from_registry.py`

---

## Attribution

- **Sigma Logsource Taxonomy**: Based on [Sigma Specification 2.0](https://sigmahq.io/sigma-specification/)
- **Universal Schema**: SIEMLess original design (Nov 16, 2025)
- **Sigma Extensions**: Added Dec 31, 2025 (18 new field mappings)

---

## Related Documentation

- [Sigma Normalization & Universal Schema Extensions](../../siemless_v3/Documentation/implementation/SIGMA_NORMALIZATION_AND_UNIVERSAL_SCHEMA_EXTENSIONS_DEC_31_2025.md)
- [Unknown Field Detection - Phase 3](../../siemless_v3/Documentation/implementation/UNKNOWN_FIELD_DETECTION_PHASE_3_COMPLETE_DEC_31_2025.md)
- [Universal Parser Implementation](../../siemless_v3/Documentation/implementation/UNIVERSAL_PARSER_IMPLEMENTATION_OVERVIEW_NOV_16_2025.md)

---

**Status**: Phase 4 In Progress (YAML export pending)