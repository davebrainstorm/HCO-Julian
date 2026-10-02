"""Build the Groundwork review site into review/hco/. Run: python3 site.py"""
import os, re
import site_base as B
import pages_a, pages_b, pages_c, pages_d, pages_e, pages_f
def build():
    css_n = len(set(re.findall(r"(--hco-[a-z0-9-]+)\s*:", open(B.OUT + "assets/tokens/tokens.css").read())))
    pages_d.COMPONENTS.clear(); comp_html = pages_d.components(); n_comp = len(pages_d.COMPONENTS)
    counts = dict(tokens=css_n, icons=len(B.ICONS), components=n_comp)
    out = {"index.html": pages_a.overview(counts), "principles.html": pages_a.principles(), "brand.html": pages_a.brand(), "colour.html": pages_b.colour(),
           "typography.html": pages_b.typography(), "layout.html": pages_b.layout(), "motion.html": pages_b.motion(), "icons.html": pages_b.icons(),
           "data.html": pages_c.data(), "capture.html": pages_c.capture(), "components.html": comp_html, "content.html": pages_f.content(), "tokens.html": pages_f.tokens(),
           "portal.html": pages_e.portal(), "report.html": pages_e.report(), "app.html": pages_e.app(), "website.html": pages_e.website(), "email.html": pages_e.email()}
    return out
build(); B.register_index()
pages = build()
for f, h in pages.items(): open(B.OUT + f, "w").write(h)
print(len(pages), "pages;", sum(len(h) for h in pages.values()) // 1024, "kB HTML;", len(B.INDEX), "search entries")
