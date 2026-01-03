# Taxonomy Changelog

All notable changes to SIEMLess taxonomies will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2025-12-31

### Added - Universal Schema Extensions for Sigma Rule Support

**Network Context** (8 new fields):
- `action` - Firewall/network action (allow, deny, block, drop)
- `direction` - Traffic direction (inbound, outbound, internal, external)
- `reason` - Reason for action (block reason, failure reason)
- `service_name` - Service/application name (HTTP, DNS, SSH)
- `dns_query` - DNS query name
- `dns_query_type` - DNS query type (A, AAAA, MX, TXT)
- `http_method` - HTTP request method (GET, POST, PUT, DELETE)
- `http_status` - HTTP response status code (200, 404, 500)

**Process Context** (3 new fields):
- `parent_process_name` - Parent process name/image (critical for Sigma rules)
- `child_process_name` - Child/target process name (for process injection)
- `loaded_module` - Loaded module/DLL (Windows Sysmon Event 7)

**Security Context** (5 new fields, NEW category):
- `event_id` - Event ID (Windows Security/Sysmon event IDs)
- `event_type` - Event type/category
- `subject_user` - Subject/initiating user (who performed the action)
- `target_object` - Target object (registry key, file, service)
- `access_mask` - Access mask (Windows permission bits)

**Authentication Context** (4 new fields, NEW category):
- `logon_type` - Logon type (2=interactive, 3=network, 10=RDP)
- `logon_id` - Logon ID/session identifier
- `auth_method` - Authentication method (Kerberos, NTLM, password, certificate)
- `failure_reason` - Failure reason (wrong password, account locked)

**Impact**:
- Field coverage: 34 fields → 52 fields (+53%)
- Category count: 6 categories → 8 categories
- Sigma rule coverage: ~65% → ~95%

### Changed - Sigma Logsource Taxonomy

**Products** (41 entries):
- Organized by type: cloud (14), os (12), network (7), application (8)
- Added comprehensive aliases for case-insensitive matching
- Linked to Sigma Specification 2.0 documentation

**Categories** (30 entries):
- Expanded from 24 to 30 categories
- Added Windows-specific categories (registry_event, file_delete, process_tampering)
- Added network categories (firewall, proxy, dns_query)

### Infrastructure

**Database Migrations**:
- Migration 067: `sigma_logsource_taxonomy` table with 71 entries
- Migration 068: `unknown_fields_for_review` table for organic schema growth

**Services**:
- `FieldDetectionService`: Automatic unknown field detection during rule imports
- `SigmaImportService`: Integrated field detection into 3 import methods

**Export/Import Scripts**:
- `export_taxonomy_to_yaml.py`: DB → YAML conversion
- `import_taxonomy_from_yaml.py`: YAML → DB conversion (pending)

**Documentation**:
- [SIGMA_NORMALIZATION_AND_UNIVERSAL_SCHEMA_EXTENSIONS_DEC_31_2025.md](../../siemless_v3/Documentation/implementation/SIGMA_NORMALIZATION_AND_UNIVERSAL_SCHEMA_EXTENSIONS_DEC_31_2025.md)
- [UNKNOWN_FIELD_DETECTION_PHASE_3_COMPLETE_DEC_31_2025.md](../../siemless_v3/Documentation/implementation/UNKNOWN_FIELD_DETECTION_PHASE_3_COMPLETE_DEC_31_2025.md)

---

## [1.0.0] - 2025-11-16

### Added - Initial Universal Schema Release

**Network Context** (9 fields):
- `source_ip`, `destination_ip`, `source_port`, `destination_port`
- `protocol`, `bytes_sent`, `bytes_received`

**Identity Context** (5 fields):
- `user_name`, `user_id`, `group_name`, `email`, `user_type`

**Process Context** (6 fields):
- `process_name`, `process_id`, `process_path`, `command_line`, `parent_process_id`

**Host Context** (5 fields):
- `hostname`, `os_type`, `os_version`, `device_type`, `mac_address`

**File Context** (5 fields):
- `file_name`, `file_path`, `file_hash`, `file_size`, `file_extension`

**Time Context** (2 fields):
- `timestamp`, `event_duration`

**Impact**:
- Total fields: 34
- Categories: 6
- Vendor alias count: ~200
- SIEM standards supported: 4 (ECS, CIM, ASIM, UDM)

---

## Version Numbering

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (field removal, canonical rename requiring code changes)
- **MINOR**: Non-breaking additions (new fields, new aliases, new categories)
- **PATCH**: Corrections (typo fixes, description updates, documentation improvements)

---

## Attribution

- **Sigma Logsource Taxonomy**: Based on [Sigma Specification 2.0](https://sigmahq.io/sigma-specification/) (Released Aug 2, 2025)
- **Universal Schema**: Original SIEMLess design by [@crazyguy106](https://github.com/crazyguy106)
- **Contributors**: Community contributions via GitHub PRs

---

## Upcoming Changes

### [2.1.0] - Planned (Q1 2026)

**Potential Additions**:
- OT/ICS field mappings (PLC, HMI, SCADA)
- Cloud-native fields (Kubernetes, Docker, serverless)
- Additional authentication fields (MFA, biometric)

**Community Contributions**:
- Discover unknown fields → approve → add to registry
- Two-way sync: Installation → Registry via GitHub PRs

---

## Migration Compatibility

| Version | SIEMLess Compatibility | Migration Required |
|---------|------------------------|-------------------|
| 2.0.0   | v3.0.0+ (Dec 31, 2025) | Migration 067-068 |
| 1.0.0   | v3.0.0 (Nov 16, 2025)  | Base schema |

---

## Related Links

- [Sigma Specification 2.0](https://sigmahq.io/sigma-specification/)
- [Sigma Taxonomy Appendix](https://sigmahq.io/sigma-specification/specification/sigma-appendix-taxonomy.html)
- [SIEMLess Central Registry](https://github.com/crazyguy106/siemless-central-registry)
- [SIEMLess v3 Documentation](../../siemless_v3/Documentation/)