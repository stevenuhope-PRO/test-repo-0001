#!/usr/bin/env python3
"""Convert a prototype (vN/index.html) into an importable Elementor page template.

Each top-level <header>/<section>/<footer> becomes one full-width Elementor
container holding an HTML widget, so the import is pixel-identical to the
prototype. The page CSS and font links ride along in the first container.

Usage: python3 tools/build_elementor.py v2 v3
"""
import json, re, sys, uuid, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZERO = {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}


def eid():
    return uuid.uuid4().hex[:7]


def container(html, label):
    return {
        "id": eid(), "elType": "container", "isInner": False,
        "settings": {"content_width": "full", "padding": ZERO, "margin": ZERO,
                     "flex_gap": {"unit": "px", "size": 0, "column": "0", "row": "0"},
                     "_title": label},
        "elements": [{"id": eid(), "elType": "widget", "widgetType": "html",
                      "settings": {"html": html}, "elements": []}],
    }


def build(version):
    src = (ROOT / version / "index.html").read_text()
    fonts = "\n".join(re.findall(r'<link[^>]+fonts\.g[^>]+>', src))
    style = re.search(r"<style>.*?</style>", src, re.S).group(0)
    body = re.search(r"<body>(.*)</body>", src, re.S).group(1)
    blocks = [m.group(0) for m in re.finditer(r"<(header|section|footer)\b.*?</\1>", body, re.S)]
    scripts = "\n".join(re.findall(r"<script>.*?</script>", body, re.S))
    content = []
    for i, block in enumerate(blocks):
        label = (re.search(r'id="([\w-]+)"', block.split(">", 1)[0]) or [None, None])[1]
        label = label or re.match(r"<(\w+)", block).group(1)
        html = block
        if i == 0:
            html = fonts + "\n" + style + "\n" + block
        if i == len(blocks) - 1 and scripts:
            html += "\n" + scripts
        content.append(container(html, label.capitalize()))
    template = {"content": content, "page_settings": {"template": "elementor_canvas"},
                "version": "0.4", "title": f"Finchby {version.upper()} Home", "type": "page"}
    out = ROOT / "elementor" / f"finchby-{version}-home.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(template, indent=1))
    print(f"{out.relative_to(ROOT)}: {len(content)} containers")


if __name__ == "__main__":
    for v in sys.argv[1:] or ["v2", "v3"]:
        build(v)
