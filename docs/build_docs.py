#!/usr/bin/env python3
"""
Automated Document & PDF Build Pipeline for Avalanche Native Stablecoin Whitepaper
Primary Engine: Tectonic LaTeX Compiler (WHITEPAPER.tex -> WHITEPAPER.pdf)
Secondary Engine: Python Markdown & MathJax (WHITEPAPER.md -> WHITEPAPER.html)
"""
import os
import subprocess
import shutil

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
TEX_PATH = os.path.join(DOCS_DIR, "WHITEPAPER.tex")
PDF_PATH = os.path.join(DOCS_DIR, "WHITEPAPER.pdf")
MD_PATH = os.path.join(DOCS_DIR, "WHITEPAPER.md")
HTML_PATH = os.path.join(DOCS_DIR, "WHITEPAPER.html")

TECTONIC_BIN = "/home/hash/Miniforge3/bin/tectonic"
if not os.path.exists(TECTONIC_BIN):
    TECTONIC_BIN = shutil.which("tectonic") or "tectonic"

def compile_latex_to_pdf():
    print(f"[1/2] Compiling LaTeX Source: {TEX_PATH}")
    if not os.path.exists(TEX_PATH):
        print(f"Error: {TEX_PATH} not found.")
        return False

    cmd = [TECTONIC_BIN, TEX_PATH]
    res = subprocess.run(cmd, cwd=DOCS_DIR, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(PDF_PATH):
        size_kb = os.path.getsize(PDF_PATH) / 1024
        print(f"      -> Successfully compiled {PDF_PATH} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"      -> LaTeX build error: {res.stderr}")
        return False

def compile_markdown_to_html():
    print(f"[2/2] Updating HTML & MathJax View: {HTML_PATH}")
    try:
        import markdown
        with open(MD_PATH, "r", encoding="utf-8") as f:
            text = f.read()

        html_body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc"])
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Avalanche Native USD (anUSD) Whitepaper</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #24292e; }}
        h1, h2, h3, h4 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #dfe2e5; padding: 8px 12px; text-align: left; }}
        th {{ background-color: #f6f8fa; }}
        pre {{ background-color: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; }}
        code {{ font-family: SFMono-Regular, Consolas, monospace; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html_doc)
        print(f"      -> Updated {HTML_PATH}")
    except Exception as e:
        print(f"      -> Note: Could not build HTML: {e}")

if __name__ == "__main__":
    compile_latex_to_pdf()
    compile_markdown_to_html()
