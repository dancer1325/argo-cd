#!/usr/bin/env python3
"""Generate individual .md files from argo-cd-advisories.json."""
import json, os, sys

input_file = os.path.join(os.path.dirname(__file__), '..', '..', 'argo-cd-advisories.json')
outdir = os.path.join(os.path.dirname(__file__), 'mirror')
os.makedirs(outdir, exist_ok=True)

with open(input_file) as f:
    advisories = json.load(f)

for a in advisories:
    slug = a.get('ghsa_id', 'unknown')
    severity = a.get('severity', 'unknown')
    summary = a.get('summary', 'No summary')
    description = a.get('description', 'No description')
    published = a.get('published_at', 'N/A')
    cve = a.get('cve_id', 'N/A')
    url = a.get('html_url', '')

    vulns = a.get('vulnerabilities', [])
    vuln_lines = ''
    for v in vulns:
        pkg = v.get('package', {}).get('name', 'N/A')
        vrange = v.get('vulnerable_version_range', 'N/A')
        patched = v.get('patched_versions', 'N/A')
        vuln_lines += f'| {pkg} | {vrange} | {patched} |\n'

    md = f'''# {summary}

- **GHSA:** [{slug}]({url})
- **CVE:** {cve}
- **Severity:** {severity}
- **Published:** {published}

## Description

{description}

## Affected Versions

| Package | Vulnerable Range | Patched |
|---------|-----------------|---------|
{vuln_lines}'''

    with open(os.path.join(outdir, f'{slug}.md'), 'w') as f:
        f.write(md)

print(f'Generated {len(advisories)} files in {outdir}/')
