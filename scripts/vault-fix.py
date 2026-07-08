#!/usr/bin/env python3
"""Fix known Graphify Obsidian export issues:
  F1-1: Merge singleton communities into _UNCLUSTERED_Nodes.md
  F1-3: Fix filename collisions (prefix node filenames with source path)
  F2-4: Merge duplicate _COMMUNITY_Saham* files
"""
import json, os, re, sys
from collections import defaultdict

VAULT = None
for p in ["/mnt/c/Users/Akhmfz/obsidian-vault",
          os.path.expanduser("~") + "/obsidian-vault"]:
    if os.path.isdir(p):
        VAULT = p
        break

if not VAULT:
    print("❌ Vault not found")
    sys.exit(1)

def fix_singletons(prefix):
    """F1-1: Merge singleton community files into one _UNCLUSTERED_Nodes.md"""
    vault_dir = os.path.join(VAULT, prefix)
    singletons = []
    kept = set()
    for f in os.listdir(vault_dir):
        if not f.startswith("_COMMUNITY_") or not f.endswith(".md"):
            continue
        fpath = os.path.join(vault_dir, f)
        with open(fpath) as fh:
            content = fh.read()
        if re.search(r'^members:\s*1\s*$', content, re.MULTILINE):
            singletons.append((f, content))
    if not singletons:
        print(f"  No singletons in {prefix}/")
        return
    singletons.sort()
    out_path = os.path.join(vault_dir, "_UNCLUSTERED_Nodes.md")
    lines = [
        "---",
        "type: unclustered",
        "tags: [graphify/unclustered]",
        "---",
        "",
        f"# Unclustered Nodes ({len(singletons)} nodes)",
        "",
        "Node-node berikut tidak berhasil dikelompokkan oleh algoritma community",
        "detection dan muncul sebagai komunitas singleton (anggota 1).",
        "",
    ]
    for fname, content in singletons:
        lines.append(f"### {fname.replace('.md','')}")
        lines.append("")
        for line in content.split("\n"):
            if line.startswith("---") or "type: community" in line:
                continue
            lines.append(line)
        lines.append("")
    with open(out_path, "w") as fh:
        fh.write("\n".join(lines))
    for fname, _ in singletons:
        os.remove(os.path.join(vault_dir, fname))
    print(f"  Merged {len(singletons)} singletons → _UNCLUSTERED_Nodes.md")

def fix_collisions(prefix):
    """F1-3: Fix filename collisions by reading graph.json source paths"""
    vault_dir = os.path.join(VAULT, prefix)
    graph_path = f"/home/Akhmfz/{prefix}/graphify-out/graph.json"
    if not os.path.isfile(graph_path):
        print(f"  graph.json not found for {prefix}")
        return
    with open(graph_path) as fh:
        graph = json.load(fh)
    label_map = {}
    label_count = defaultdict(int)
    for node in graph.get("nodes", []):
        lbl = node.get("label", "")
        src = node.get("source_file", "")
        nid = node.get("id", "")
        label_count[lbl] += 1
        if label_count[lbl] > 1:
            if src:
                safe = re.sub(r'[\\/*?:"<>|#^\[\]]', "_", src)
                label_map.setdefault(lbl, []).append((nid, safe))
    renamed = 0
    for lbl, entries in label_map.items():
        for nid, safe_prefix in entries:
            for suffix_num in range(1, 10):
                old_name = f"{lbl}_{suffix_num}.md"
                old_path = os.path.join(vault_dir, old_name)
                if os.path.isfile(old_path):
                    new_name = f"{safe_prefix}_{lbl}_{suffix_num}.md" if safe_prefix else old_name
                    new_path = os.path.join(vault_dir, new_name)
                    if old_path != new_path and not os.path.isfile(new_path):
                        os.rename(old_path, new_path)
                        renamed += 1
    if renamed:
        print(f"  Fixed {renamed} collision(s) in {prefix}/")

def fix_duplicate_communities(prefix):
    """F2-4: Merge duplicate _COMMUNITY_Saham* files"""
    vault_dir = os.path.join(VAULT, prefix)
    pattern = re.compile(r'^(_COMMUNITY_Saham[^_]+)(?:_(\d+))?\.md$')
    groups = defaultdict(list)
    for f in os.listdir(vault_dir):
        m = pattern.match(f)
        if m:
            groups[m.group(1)].append((int(m.group(2) or 0), f))
    for base, files in groups.items():
        if len(files) <= 1:
            continue
        files.sort()
        merged = []
        for _, fname in files:
            fpath = os.path.join(vault_dir, fname)
            with open(fpath) as fh:
                merged.append(fh.read())
            os.remove(fpath)
        out = os.path.join(vault_dir, f"{base}.md")
        with open(out, "w") as fh:
            fh.write("\n\n".join(merged))
        print(f"  Merged {len(files)} duplicates → {base}.md")

for proj in ["papan-instrumen", "papan-gerak"]:
    print(f"\n🔧 {proj}/")
    fix_singletons(proj)
    fix_collisions(proj)
    fix_duplicate_communities(proj)

print("\n✅ Vault fix complete")
