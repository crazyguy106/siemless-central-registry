# MITRE ATT&CK Taxonomy Reference

**Version**: v18 (October 2025)
**Last Updated**: January 9, 2026
**Source**: https://github.com/mitre-attack/attack-stix-data

## Official Counts

### Enterprise ATT&CK v18
- **Parent Techniques**: 216
- **Sub-techniques**: 475
- **Total Techniques**: 691
- **Tactics**: 14 (Reconnaissance, Resource Development, Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, Command and Control, Exfiltration, Impact)

### ICS ATT&CK v18
- **Techniques**: 83
- **Tactics**: 12 (Initial Access, Execution, Persistence, Privilege Escalation, Evasion, Discovery, Lateral Movement, Collection, Command and Control, Inhibit Response Function, Impair Process Control, Impact)

## SIEMLess Integration

### Data Source
MITRE ATT&CK data is stored locally in SIEMLess v3 due to file size (51MB combined):
- `attack-control-framework-mappings/data/attack/enterprise-attack-v18.json` (48MB)
- `attack-control-framework-mappings/data/attack/ics-attack-v18.json` (3.4MB)

### Usage in SIEMLess
1. **MITRELoader**: `src/modules/detection/application/services/mitre_loader.py`
   - Loads and caches MITRE framework data
   - Provides technique-to-tactic mappings
   - Calculates detection coverage

2. **InvestigationGuideClassifier**: `src/modules/detection/domain/services/investigation_guide_classifier.py`
   - Maps techniques to attack categories for prompt routing
   - Includes D3FEND detection methods
   - Pyramid of Pain evasion resistance levels

3. **Sigma Rules**: All Sigma rules reference MITRE ATT&CK techniques
   - `attack.t1059.001` → PowerShell execution
   - `attack.t1003` → Credential dumping
   - etc.

## Updating MITRE Data

To update to a newer MITRE ATT&CK version:

```bash
# Download latest Enterprise ATT&CK
curl -L "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/enterprise-attack/enterprise-attack.json" \
  -o attack-control-framework-mappings/data/attack/enterprise-attack-vXX.json

# Download latest ICS ATT&CK
curl -L "https://raw.githubusercontent.com/mitre-attack/attack-stix-data/master/ics-attack/ics-attack.json" \
  -o attack-control-framework-mappings/data/attack/ics-attack-vXX.json

# Update MITRELoader path
# Update InvestigationGuideClassifier technique mappings
```

## Reference Links

- [MITRE ATT&CK Enterprise](https://attack.mitre.org/matrices/enterprise/)
- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/)
- [MITRE STIX Data Repository](https://github.com/mitre-attack/attack-stix-data)
- [D3FEND Matrix](https://d3fend.mitre.org/)
