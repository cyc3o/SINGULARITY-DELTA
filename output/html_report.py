"""
HTML Report Generator
Professional, offline HTML reports for Singularity-Delta
"""

import json
from pathlib import Path
from datetime import datetime
from core.result import AnalysisResult


class HTMLReport:
    """
    Generates professional HTML reports from AnalysisResult.
    """

    @staticmethod
    def generate(result: AnalysisResult, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        html = HTMLReport._build_html(result)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    # -----------------------------
    # INTERNAL HTML BUILDER
    # -----------------------------
    @staticmethod
    def _build_html(result: AnalysisResult) -> str:
        findings_html = ""
        if result.findings:
            findings_html = "".join(
                f"""
            <tr>
                <td>{f.get('id', 'N/A').upper()}</td>
                <td><span class="severity-{f.get('severity', 'INFO').lower()}">{f.get('severity', 'INFO').upper()}</span></td>
                <td>{f.get('message', '').upper()}</td>
            </tr>
                """
                for f in result.findings
            )
        else:
            findings_html = '<tr><td colspan="3" style="text-align:center;">✅ NO FINDINGS DETECTED - SYSTEM IS CLEAN</td></tr>'

        # Convert all text to uppercase
        target_upper = (result.target or 'UNKNOWN').upper()
        verdict_upper = (result.verdict or 'UNKNOWN').upper()
        risk_upper = (result.risk or 'UNKNOWN').upper()
        
        # Verdict emoji
        verdict_emoji = "✅" if verdict_upper == "PASSED" else "❌" if verdict_upper == "FAILED" else "⚠️"
        verdict_class = HTMLReport._verdict_class(result.verdict)

        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SINGULARITY-DELTA REPORT</title>
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Courier New', monospace;
    background: linear-gradient(135deg, #0d1117 0%, #1a1e2e 100%);
    color: #c9d1d9;
    padding: 30px;
    margin: 0;
    min-height: 100vh;
}}

.header {{
    text-align: center;
    margin-bottom: 40px;
    padding: 30px;
    background: #161b22;
    border: 2px solid #30363d;
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
}}

h1 {{
    color: #58a6ff;
    font-size: 36px;
    font-weight: bold;
    letter-spacing: 3px;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(88, 166, 255, 0.5);
}}

h2 {{
    color: #58a6ff;
    font-size: 24px;
    margin-bottom: 15px;
    letter-spacing: 2px;
    border-bottom: 2px solid #30363d;
    padding-bottom: 10px;
}}

.card {{
    background: #161b22;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 25px;
    border: 2px solid #30363d;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}}

.summary-table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}

.summary-table th,
.summary-table td {{
    border: 1px solid #30363d;
    padding: 12px;
    text-align: left;
    font-size: 14px;
}}

.summary-table th {{
    background: #21262d;
    font-weight: bold;
    color: #58a6ff;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 15px;
}}

th, td {{
    border: 1px solid #30363d;
    padding: 12px;
    text-align: left;
}}

th {{
    background: #21262d;
    font-weight: bold;
    color: #58a6ff;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.score {{
    font-size: 64px;
    font-weight: bold;
    text-align: center;
    margin: 30px 0;
    text-shadow: 0 0 20px rgba(88, 166, 255, 0.6);
    letter-spacing: 4px;
}}

.verdict {{
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin: 25px 0;
    padding: 20px;
    border-radius: 8px;
    letter-spacing: 3px;
    text-shadow: 0 0 15px currentColor;
}}

.pass {{ 
    color: #3fb950; 
    background: rgba(63, 185, 80, 0.1);
    border: 2px solid #3fb950;
}}

.fail {{ 
    color: #f85149; 
    background: rgba(248, 81, 73, 0.1);
    border: 2px solid #f85149;
}}

.warn {{ 
    color: #d29922; 
    background: rgba(210, 153, 34, 0.1);
    border: 2px solid #d29922;
}}

.severity-critical {{ 
    color: #f85149; 
    font-weight: bold; 
    text-shadow: 0 0 5px #f85149;
}}

.severity-high {{ 
    color: #f97583; 
    font-weight: bold;
}}

.severity-medium {{ 
    color: #d29922; 
}}

.severity-low {{ 
    color: #79c0ff; 
}}

.severity-info {{ 
    color: #8b949e; 
}}

.metadata {{
    background: #0d1117;
    padding: 15px;
    border-radius: 6px;
    margin-top: 15px;
    font-size: 13px;
    font-family: 'Courier New', monospace;
    border-left: 4px solid #58a6ff;
}}

.badge {{
    display: inline-block;
    padding: 5px 12px;
    border-radius: 4px;
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 1px;
    margin: 5px;
}}

.badge-critical {{ background: #f85149; color: #fff; }}
.badge-high {{ background: #f97583; color: #fff; }}
.badge-medium {{ background: #d29922; color: #000; }}
.badge-low {{ background: #79c0ff; color: #000; }}
.badge-info {{ background: #8b949e; color: #fff; }}

.engine-info {{
    text-align: center;
    margin-top: 30px;
    padding: 20px;
    background: #0d1117;
    border-radius: 8px;
    border: 1px solid #30363d;
}}

pre {{
    background: #0d1117;
    padding: 15px;
    border-radius: 6px;
    overflow-x: auto;
    border-left: 4px solid #58a6ff;
    font-size: 12px;
}}
</style>
</head>
<body>

<div class="header">
    <h1>🔬 SINGULARITY-DELTA</h1>
    <p style="font-size: 18px; color: #8b949e; letter-spacing: 2px;">DETERMINISTIC POLICY VERIFICATION ENGINE</p>
</div>

<div class="card">
<h2>📊 SUMMARY</h2>
<table class="summary-table">
<tr><th>PROPERTY</th><th>VALUE</th></tr>
<tr><td>🎯 TARGET</td><td><strong>{target_upper}</strong></td></tr>
<tr><td>⏰ TIMESTAMP</td><td>{result.timestamp}</td></tr>
<tr><td>⚙️ ENGINE VERSION</td><td>{result.engine_version}</td></tr>
<tr><td>🔍 TOTAL FINDINGS</td><td><strong>{len(result.findings)}</strong></td></tr>
</table>

<div class="score">📈 SCORE: {result.score:.1f}/100</div>

<div class="verdict {verdict_class}">
{verdict_emoji} VERDICT: {verdict_upper}
</div>

<div class="metadata">
<strong>⚠️ RISK LEVEL:</strong> {risk_upper}<br>
<strong>📊 CONFIDENCE:</strong> {result.confidence:.2%}
</div>
</div>

<div class="card">
<h2>🔍 FINDINGS ({len(result.findings)})</h2>
<table>
<tr>
    <th>🆔 ID</th>
    <th>⚠️ SEVERITY</th>
    <th>📝 DESCRIPTION</th>
</tr>
{findings_html}
</table>
</div>

<div class="card">
<h2>📋 METADATA</h2>
<pre>{json.dumps(result.metadata, indent=2, default=str).upper()}</pre>
</div>

<div class="engine-info">
    <p style="color: #58a6ff; font-weight: bold; font-size: 14px; letter-spacing: 1px;">
        ⚡ POWERED BY SINGULARITY-DELTA ENGINE v{result.engine_version}
    </p>
    <p style="color: #8b949e; font-size: 12px; margin-top: 10px;">
        DETERMINISTIC POLICY VERIFICATION • RULES-BASED ANALYSIS • PROFESSIONAL GRADE
    </p>
</div>

</body>
</html>
"""

    @staticmethod
    def _verdict_class(verdict: str) -> str:
        verdict = verdict.lower()
        if "pass" in verdict:
            return "pass"
        if "fail" in verdict:
            return "fail"
        return "warn"
