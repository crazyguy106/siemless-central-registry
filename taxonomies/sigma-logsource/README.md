# Sigma Logsource Taxonomy

**Version**: 2.0.0
**Last Updated**: December 31, 2025
**Based On**: [Sigma Specification 2.0 Appendix](https://sigmahq.io/sigma-specification/specification/sigma-appendix-taxonomy.html)

---

## Overview

This folder contains the official Sigma logsource taxonomy for normalizing vendor/product names in Sigma rules.

**Purpose**: Enable case-insensitive, alias-aware matching for Detection Wizard Step 3.

---

## Files

| File | Count | Description |
|------|-------|-------------|
| `products.yaml` | 41 products | Canonical vendor/product names with aliases |
| `categories.yaml` | 30 categories | Canonical log source categories |
| `services.yaml` | 0 (merged) | Services are part of products |

---

## Products (41 entries)

### By Type

**Cloud Providers** (14):
- aws, azure, gcp, m365, okta, onelogin, github, bitbucket, cisco_cloud, salesforce, slack, workday, box, dropbox

**Operating Systems** (12):
- windows, linux, macos, unix, android, ios, freebsd, openbsd, netbsd, solaris, aix, hpux

**Network Devices** (7):
- cisco, paloalto, fortinet, checkpoint, juniper, huawei, f5

**Applications** (8):
- apache, iis, nginx, django, spring, sql, modsecurity, tomcat

---

## Categories (30 entries)

**Process Events**:
- process_creation, process_termination, process_access, process_tampering

**Network Events**:
- network_connection, dns_query, firewall, proxy

**File Events**:
- file_event, file_change, file_delete, image_load

**Registry Events**:
- registry_event, registry_add, registry_set, registry_delete

**Authentication Events**:
- authentication, logon, logoff

**Generic Categories**:
- antivirus, database, webserver, application_log

---

## Format

### products.yaml
```yaml
version: "2.0.0"
last_updated: "2025-12-31"
source: "Sigma Specification 2.0 Appendix"

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

  - canonical: "paloalto"
    type: "network"
    aliases:
      - "Palo Alto"
      - "PaloAlto"
      - "PA"
      - "PAN-OS"
    description: "Palo Alto Networks firewall"
    sigma_spec_url: "https://sigmahq.io/docs/basics/log-sources.html#paloalto"
```

### categories.yaml
```yaml
version: "2.0.0"
last_updated: "2025-12-31"
source: "Sigma Specification 2.0 Appendix"

categories:
  - canonical: "process_creation"
    type: "category"
    aliases:
      - "process_create"
      - "proc_creation"
      - "ProcessCreation"
    description: "Process creation events"
```

---

## Usage

### Normalizing Product Names

**Problem**: User declares "PaloAlto" or "Palo Alto" log source

**Solution**: Lookup in `products.yaml` to find canonical form "paloalto"

**Python Example**:
```python
import yaml

with open('products.yaml') as f:
    taxonomy = yaml.safe_load(f)

user_input = "PaloAlto"

for product in taxonomy['products']:
    if user_input in product['aliases'] or user_input.lower() == product['canonical']:
        print(f"Canonical: {product['canonical']}")
        # Output: Canonical: paloalto
        break
```

### Fuzzy Matching

**Problem**: User types "win" instead of "windows"

**Solution**: Use PostgreSQL `similarity()` function (pg_trgm extension)

**SQL Example**:
```sql
-- Exact match via alias
SELECT canonical_product FROM sigma_logsource_taxonomy
WHERE 'Windows' = ANY(product_aliases);
-- Result: "windows"

-- Fuzzy match
SELECT canonical_product, similarity('win', canonical_product) as confidence
FROM sigma_logsource_taxonomy
WHERE similarity('win', canonical_product) > 0.6
ORDER BY confidence DESC LIMIT 1;
-- Result: "windows", confidence 0.75
```

---

## Contributing

### Adding a New Product

1. **Check Sigma Spec**: Verify product exists in [official Sigma taxonomy](https://sigmahq.io/sigma-specification/specification/sigma-appendix-taxonomy.html)
2. **Edit products.yaml**: Add entry with canonical name + aliases
3. **Test**: Ensure no duplicate canonical names
4. **PR**: Submit pull request with description

**Example**:
```yaml
- canonical: "fortinet"
  type: "network"
  aliases:
    - "Fortinet"
    - "FORTINET"
    - "FortiGate"
    - "Fortigate"
  description: "Fortinet FortiGate firewall"
  sigma_spec_url: "https://sigmahq.io/docs/basics/log-sources.html#fortinet"
```

### Adding Aliases to Existing Product

1. **Identify Need**: Unknown field logged during rule import
2. **Research**: Verify alias is valid (vendor documentation, common usage)
3. **Edit**: Add alias to `aliases` array
4. **Test**: Import rules using new alias
5. **PR**: Submit with explanation

---

## Maintenance

### Sync from Sigma Spec

**Frequency**: Quarterly (or when Sigma spec updates)

**Process**:
1. Check [Sigma Specification changelog](https://github.com/SigmaHQ/sigma-specification/releases)
2. Compare with current `products.yaml` and `categories.yaml`
3. Add missing products/categories
4. Update aliases if Sigma spec changed
5. Increment version (MINOR for additions, MAJOR for removals)

### Sync to Database

**Script**: `import_taxonomy_from_yaml.py`

**Command**:
```bash
python scripts/import_taxonomy_from_yaml.py \
  --type sigma \
  --input ../siemless-central-registry/taxonomies/sigma-logsource/
```

**What it does**:
- Reads YAML files
- Creates Migration 069 (if first time)
- Inserts/updates `sigma_logsource_taxonomy` table
- Logs sync timestamp

---

## Version History

**2.0.0** (Dec 31, 2025):
- Initial YAML export from PostgreSQL Migration 067
- 41 products, 30 categories
- Based on Sigma Specification 2.0

**Future**:
- 2.1.0: Add OT/ICS products (Siemens, Schneider, Rockwell)
- 2.2.0: Add cloud-native categories (Kubernetes, Docker)

---

## Attribution

Based on [Sigma Specification 2.0](https://sigmahq.io/sigma-specification/) by SigmaHQ.
Maintained by SIEMLess contributors.

---

## Related Files

- [Universal Schema](../universal-schema/README.md) - Field name normalization
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [Parent README](../README.md) - Overall taxonomy documentation