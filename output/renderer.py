"""
CLI Renderer
Beautiful terminal output formatting
NO LOGIC. ONLY DISPLAY.
"""
from typing import Dict, List
from core.result import AnalysisResult


class CLIRenderer:
    """
    Renders analysis results to the terminal.
    Pure presentation layer - no business logic.
    """
    
    # Color codes for terminal output
    COLORS = {
        "RESET": "\033[0m",
        "BOLD": "\033[1m",
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "GRAY": "\033[90m"
    }
    
    SEVERITY_COLORS = {
        "CRITICAL": "RED",
        "HIGH": "RED",
        "MEDIUM": "YELLOW",
        "LOW": "BLUE",
        "INFO": "GRAY"
    }
    
    @classmethod
    def render(cls, result: AnalysisResult, use_colors: bool = True) -> None:
        """
        Render complete analysis result to terminal.
        
        Args:
            result: AnalysisResult to render
            use_colors: Whether to use terminal colors
        """
        if not use_colors:
            cls.COLORS = {k: "" for k in cls.COLORS}
        
        cls._render_header()
        cls._render_summary(result)
        cls._render_findings(result)
        cls._render_footer(result)
    
    @classmethod
    def _render_header(cls) -> None:
        """Render analysis header"""
        bold = cls.COLORS["BOLD"]
        cyan = cls.COLORS["CYAN"]
        reset = cls.COLORS["RESET"]
        
        print(f"\n{bold}{cyan}╔════════════════════════════════════════════════════════════════╗{reset}")
        print(f"{bold}{cyan}║           SINGULARITY DELTA - ANALYSIS REPORT                  ║{reset}")
        print(f"{bold}{cyan}╚════════════════════════════════════════════════════════════════╝{reset}\n")
    
    @classmethod
    def _render_summary(cls, result: AnalysisResult) -> None:
        """Render summary section"""
        bold = cls.COLORS["BOLD"]
        reset = cls.COLORS["RESET"]
        
        # Verdict color
        verdict_color = cls.COLORS["GREEN"] if result.verdict == "PASSED" else cls.COLORS["RED"]
        
        # Risk color
        risk_colors = {
            "NONE": "GREEN",
            "LOW": "BLUE",
            "MEDIUM": "YELLOW",
            "HIGH": "RED",
            "CRITICAL": "RED"
        }
        risk_color = cls.COLORS[risk_colors.get(result.risk, "GRAY")]
        
        print(f"{bold}FINAL VERDICT{reset}")
        print("=" * 64)
        print(f"Target        : {result.target}")
        print(f"Verdict       : {verdict_color}{bold}{result.verdict}{reset}")
        print(f"Risk Level    : {risk_color}{bold}{result.risk}{reset}")
        print(f"Score         : {result.score:.1f}/100.0")
        print(f"Confidence    : {result.confidence:.2f}")
        print(f"Findings      : {len(result.findings)}")
        print(f"Engine Version: {result.engine_version}")
        print(f"Timestamp     : {result.timestamp}")
        print()
    
    @classmethod
    def _render_findings(cls, result: AnalysisResult) -> None:
        """Render findings section"""
        if not result.findings:
            green = cls.COLORS["GREEN"]
            bold = cls.COLORS["BOLD"]
            reset = cls.COLORS["RESET"]
            print(f"{green}{bold}✓ No issues found - system is compliant{reset}\n")
            return
        
        bold = cls.COLORS["BOLD"]
        reset = cls.COLORS["RESET"]
        
        print(f"{bold}FINDINGS{reset}")
        print("=" * 64)
        
        # Group by severity
        by_severity = {}
        for finding in result.findings:
            severity = finding.get("severity", "INFO")
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(finding)
        
        # Render in severity order
        severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
        
        for severity in severity_order:
            if severity not in by_severity:
                continue
            
            findings = by_severity[severity]
            color = cls.COLORS[cls.SEVERITY_COLORS.get(severity, "GRAY")]
            
            print(f"\n{color}{bold}[{severity}]{reset} - {len(findings)} issue(s)")
            print("-" * 64)
            
            for i, finding in enumerate(findings, 1):
                cls._render_finding(finding, i, color)
        
        print()
    
    @classmethod
    def _render_finding(cls, finding: Dict, index: int, color: str) -> None:
        """Render individual finding"""
        reset = cls.COLORS["RESET"]
        gray = cls.COLORS["GRAY"]
        
        rule_id = finding.get("id", "UNKNOWN")
        message = finding.get("message", "No message")
        category = finding.get("category", "GENERAL")
        
        print(f"{color}  {index}. [{rule_id}]{reset} {message}")
        print(f"     {gray}Category: {category}{reset}")
        
        # Show details if available
        details = finding.get("details")
        if details and isinstance(details, dict):
            for key, value in details.items():
                if isinstance(value, list) and len(value) <= 5:
                    print(f"     {gray}{key}: {', '.join(map(str, value))}{reset}")
                elif not isinstance(value, (list, dict)):
                    print(f"     {gray}{key}: {value}{reset}")
        
        print()
    
    @classmethod
    def _render_footer(cls, result: AnalysisResult) -> None:
        """Render analysis footer with metadata"""
        gray = cls.COLORS["GRAY"]
        reset = cls.COLORS["RESET"]
        
        metadata = result.metadata
        if metadata:
            print(f"{gray}Analysis Metadata:{reset}")
            print(f"{gray}  Rules Executed: {metadata.get('rules_executed', 0)}{reset}")
            print(f"{gray}  Critical: {metadata.get('critical', 0)} | " +
                  f"High: {metadata.get('high', 0)} | " +
                  f"Medium: {metadata.get('medium', 0)} | " +
                  f"Low: {metadata.get('low', 0)}{reset}")
            print()


class CompactRenderer:
    """Minimal one-line renderer for CI/CD"""
    
    @staticmethod
    def render(result: AnalysisResult) -> None:
        """Render compact one-line summary"""
        status = "✓ PASS" if result.verdict == "PASSED" else "✗ FAIL"
        print(f"{status} | {result.target} | Score: {result.score:.0f} | " +
              f"Risk: {result.risk} | Findings: {len(result.findings)}")
