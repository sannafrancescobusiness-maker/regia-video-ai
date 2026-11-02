#!/usr/bin/env python3
"""Conta davvero il lavoro fatto con Claude Code in questa cartella: ore attive, giorni, messaggi, render.
uso: conta_lavoro.py [altre cartelle di lavoro...]  Le ore sono sessione attiva, pause oltre 15 minuti escluse."""
import datetime as dt, glob, json, os, re, sys
def slug(p): return re.sub(r"[^A-Za-z0-9-]", "-", os.path.abspath(p))
D = [os.getcwd()] + sys.argv[1:]; F = [f for d in D for f in glob.glob(os.path.expanduser(f"~/.claude/projects/{slug(d)}/*.jsonl"))]
vis = set(); ev = []; msg = 0; cmd = {}; err = set()
for f in F:
    for l in open(f, errors="ignore"):
        try: d = json.loads(l)
        except Exception: continue
        u = d.get("uuid")
        if u in vis and u: continue
        vis.add(u); ts = d.get("timestamp")
        if not ts or d.get("isSidechain"): continue
        ty = d.get("type"); c = (d.get("message") or {}).get("content")
        if ty in ("user", "assistant"): ev.append(dt.datetime.fromisoformat(ts.replace("Z", "+00:00")))
        if ty == "user" and not d.get("isMeta") and not d.get("isCompactSummary"):
            T = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text") if isinstance(c, list) else ""
            if T.strip() and not T.strip().startswith(("<", "This session is being continued", "[Request interrupted", "Caveat:")): msg += 1
        if isinstance(c, list):
            for x in c:
                if isinstance(x, dict) and x.get("type") == "tool_use" and x.get("name") == "Bash": cmd[x.get("id")] = x["input"].get("command", "")
                if isinstance(x, dict) and x.get("type") == "tool_result" and x.get("is_error"): err.add(x.get("tool_use_id"))
ev.sort(); ore = sum(s for s in ((ev[i + 1] - ev[i]).total_seconds() for i in range(len(ev) - 1)) if s < 900) / 3600
prove = falliti = 0
for i, c in cmd.items():
    for s in re.split(r"&&|;|\n|\|\|", c):
        s = s.strip()
        if s.startswith(("pgrep", "pkill", "grep", "echo", "#", "ps ", "cat ", "sed ")): continue
        if (re.search(r"\bhyperframes\s+render\b", s) and "--help" not in s) or re.search(r"python3?\s+\S*render\.py\s", s):
            prove += 1; falliti += i in err
print(f"sessioni {len(F)} · ore attive {ore:.1f} · giorni {len({e.astimezone().date() for e in ev})} · messaggi {msg} · render lanciati {prove} (falliti subito {falliti})")
