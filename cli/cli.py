"""
Command-Line Interface
User interaction layer for Singularity Delta
"""

import argparse
import sys

from core.engine import Engine
from rules import DEFAULT_RULES
from services.loader import DataLoader
from services.validator import Validator
from output.renderer import CLIRenderer, CompactRenderer
from output.json_exporter import JSONExporter
from config import Config


class CLI:
    """
    Command-line interface for Singularity Delta.
    Strictly argparse-based (no interactive loops).
    """

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="singularity-delta",
            description=f"{Config.ENGINE_NAME} – Deterministic Policy Verification Engine",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  singularity-delta analyze system.json
  singularity-delta analyze system.json --format json --output report.json
  singularity-delta analyze system.json --compact
  singularity-delta validate system.json
  singularity-delta version
            """
        )

        subparsers = parser.add_subparsers(dest="command", required=True)

        # analyze
        analyze = subparsers.add_parser("analyze", help="Analyze system JSON")
        analyze.add_argument("file", help="Path to JSON system file")
        analyze.add_argument("--format", choices=["cli", "json", "compact"], default="cli")
        analyze.add_argument("--output", help="Output file (for JSON format)")
        analyze.add_argument("--no-color", action="store_true")
        analyze.add_argument("--strict", action="store_true")

        # validate
        validate = subparsers.add_parser("validate", help="Validate JSON structure only")
        validate.add_argument("file", help="Path to JSON system file")

        # version
        subparsers.add_parser("version", help="Show engine version")

        return parser

    def run(self, argv=None):
        args = self.parser.parse_args(argv)

        if args.command == "analyze":
            return self._analyze(args)

        if args.command == "validate":
            return self._validate(args)

        if args.command == "version":
            return self._version()

        return 0

    # -------------------- COMMAND HANDLERS --------------------

    def _analyze(self, args) -> int:
        try:
            data = DataLoader.load_from_file(args.file)
            target = DataLoader.get_target_name(data)

            valid, msg = Validator.quick_validate(data)
            if not valid:
                print(f"❌ Validation failed: {msg}")
                return 1

            engine = Engine(DEFAULT_RULES)
            if args.strict:
                engine.context.enable_strict_mode()

            result = engine.run(data, target)

            if args.format == "cli":
                CLIRenderer.render(result, use_colors=not args.no_color)

            elif args.format == "compact":
                CompactRenderer.render(result)

            elif args.format == "json":
                if args.output:
                    JSONExporter.export(result, args.output)
                    print(f"✓ Exported to {args.output}")
                else:
                    print(JSONExporter.export_to_string(result))

            return 1 if result.verdict == "FAILED" else 0

        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return 1

        except Exception as e:
            print(f"❌ Error: {e}")
            if Config.LOG_LEVEL == "DEBUG":
                import traceback
                traceback.print_exc()
            return 1

    def _validate(self, args) -> int:
        try:
            data = DataLoader.load_from_file(args.file)
            valid, msg = Validator.quick_validate(data)

            if not valid:
                print(f"❌ {msg}")
                return 1

            print(f"✓ {msg}")

            metrics = Validator.estimate_complexity(data)
            print("\nComplexity Metrics:")
            for k, v in metrics.items():
                print(f"  {k.replace('_', ' ').title():15}: {v}")

            return 0

        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    def _version(self) -> int:
        print(f"{Config.ENGINE_NAME} v{Config.ENGINE_VERSION}")
        print("Deterministic Policy Verification Engine\n")
        print(f"Rules Loaded: {len(DEFAULT_RULES)}")

        categories = {}
        for rule in DEFAULT_RULES:
            categories[rule.category] = categories.get(rule.category, 0) + 1

        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}")

        return 0


def main():
    cli = CLI()
    exit_code = cli.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()