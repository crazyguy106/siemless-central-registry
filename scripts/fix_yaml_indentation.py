#!/usr/bin/env python3
"""
Fix YAML indentation issues in Sigma rules.

These rules were converted from KQL/other formats and have block scalar
content that is not properly indented.

Example problem:
    detection:
      _kql_query: |
        let x = 1;
    let y = 2;  # <-- Should be indented under _kql_query

This script adds proper indentation to fix YAML parsing.

Usage:
    python fix_yaml_indentation.py [--dry-run] [--verbose]
"""

import re
import sys
from pathlib import Path
import yaml

def fix_yaml_indentation(content: str) -> str:
    """Fix YAML files where block scalar content is not indented."""
    lines = content.split('\n')
    fixed_lines = []
    in_block_scalar = False
    block_indent = 0

    for i, line in enumerate(lines):
        # Check if this line starts a block scalar (ends with | or >)
        if re.match(r'^(\s*)[\w_-]+:\s*[|>]\s*$', line):
            in_block_scalar = True
            match = re.match(r'^(\s*)', line)
            block_indent = len(match.group(1)) + 2
            fixed_lines.append(line)
            continue

        if in_block_scalar and line.strip():
            if not line.startswith(' ') and not line.startswith('\t'):
                if re.match(r'^[a-zA-Z_][\w_-]*:', line):
                    in_block_scalar = False
                    fixed_lines.append(line)
                else:
                    fixed_lines.append(' ' * block_indent + line)
                continue
            else:
                if re.match(r'^(\s+)[a-zA-Z_][\w_-]*:', line):
                    current_indent = len(re.match(r'^(\s*)', line).group(1))
                    if current_indent <= block_indent - 2:
                        in_block_scalar = False

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv

    # Find sigma rules directory (relative to this script)
    script_dir = Path(__file__).parent
    sigma_path = script_dir.parent / "sigma-rules"

    if not sigma_path.exists():
        print(f"Error: Sigma rules directory not found at {sigma_path}")
        sys.exit(1)

    print(f"Scanning: {sigma_path}")
    print(f"Dry run: {dry_run}")
    print()

    files = list(sigma_path.rglob('*.yml')) + list(sigma_path.rglob('*.yaml'))
    files = [f for f in files if 'index.yaml' not in f.name]

    fixed_count = 0
    already_valid = 0
    still_broken = []

    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            yaml.safe_load(content)
            already_valid += 1
        except yaml.YAMLError:
            # Try to fix
            try:
                fixed_content = fix_yaml_indentation(content)
                yaml.safe_load(fixed_content)

                if not dry_run:
                    f.write_text(fixed_content, encoding='utf-8')

                fixed_count += 1
                if verbose:
                    print(f"  Fixed: {f.name}")
            except Exception as e:
                still_broken.append((f, str(e)[:80]))

    print(f"\nResults:")
    print(f"  Already valid: {already_valid}")
    print(f"  Fixed: {fixed_count}")
    print(f"  Still broken: {len(still_broken)}")
    print(f"  Total valid after fix: {already_valid + fixed_count} / {len(files)}")

    if still_broken and verbose:
        print("\nFiles that could not be fixed:")
        for f, err in still_broken[:10]:
            print(f"  {f.name}: {err}")

    if dry_run:
        print("\n[DRY RUN] No files were modified.")
    else:
        print(f"\n{fixed_count} files have been fixed.")


if __name__ == "__main__":
    main()
