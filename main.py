#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SINGULARITY-DELTA :: CLEAN EDITION
CREATED BY VISHAL THAKUR
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# ==============================
# Utility
# ==============================

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def safe_input(prompt):
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print("\n\n👋 GOODBYE! THANK YOU FOR USING SINGULARITY-DELTA 👋\n")
        sys.exit(0)

# ==============================
# UI
# ==============================

def show_banner():
    print("\n")
    print("            ╭╮╭╮")
    print("            ┃┃┃┃")
    print("            ┃┃┃┃")
    print("         ╭╯┗╯┃")
    print("         ┃▋　▋┃")
    print("         ▇           \\")
    print("         ╰╮         \\")
    print("      ╭╭━╯      ┃")
    print("   ╱╰╰╯╲　   ┃")
    print("▕╭╭╮╮╮▏   ┃")
    print("▕▔▔▔▔▔▏   ┃")
    print("　╲▁▁▁╱╭　┣╮")
    print("      ╭　╭━┛　┣╯")
    print("      ╰━╰━━━╯")
    print("\n" + "="*60)
    print("< SINGULARITY DELTA  ♥")
    print(" « SYSTEM VERIFICATION ENGINE >")
    print("CREATED BY [ VISHAL THAKUR ] ")
    print("="*60)

def show_menu():
    print("\n  [ MAIN MENU ]")
    print("  [1] 🔍 ANALYZE SYSTEM ")
    print("  [2]  QUIT ∞ \n")

def get_choice():
    while True:
        choice = safe_input("👉 CHOICE ➜ ").strip()
        if choice in ["1", "2"]:
            return choice
        print("⚠️  INVALID INPUT. PLEASE CHOOSE 1 OR 2.\n")

# ==============================
# File Handling (STRICT)
# ==============================

def find_json_files():
    datasets_dir = Path(__file__).parent / "datasets"
    if not datasets_dir.exists():
        return []
    return list(datasets_dir.glob("*.json"))

def select_file():
    files = find_json_files()

    if not files:
        print("\n⚠️  NO JSON FILES FOUND IN DATASETS FOLDER\n")
        return None

    print("\n📁 AVAILABLE JSON FILES:\n")
    for i, f in enumerate(files, 1):
        print(f"  [{i}] 📄 {f.name}")
    print()

    if len(files) == 1:
        print(f"✅ AUTO-SELECTED: {files[0].name.upper()}\n")
        return files[0]

    while True:
        choice = safe_input(f"👉 SELECT FILE (1-{len(files)}): ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                print(f"\n✅ SELECTED: {files[idx].name.upper()}")
                return files[idx]
        except:
            pass
        print("⚠️  INVALID SELECTION. TRY AGAIN.\n")

# ==============================
# ENGINE INTEGRATION
# ==============================

# Import engine and dependencies
from core.engine import Engine
from rules import DEFAULT_RULES
from services.loader import DataLoader
from services.validator import Validator
from output.json_exporter import JSONExporter
from output.html_report import HTMLReport

def analyze_system():
    """
    Main analysis function - now uses the real engine.
    """
    import time
    
    print("\n" + "="*60)
    print("🔍 SYSTEM ANALYSIS INITIATED")
    print("="*60 + "\n")

    json_file = select_file()
    if not json_file:
        safe_input("\nPRESS ENTER...")
        return

    print("\n🔄 LOADING DATA...")
    time.sleep(0.5)
    
    # Load data using the proper service
    try:
        data = DataLoader.load_from_file(str(json_file))
        print("✅ DATA LOADED SUCCESSFULLY")
    except json.JSONDecodeError:
        print("\n❌ INVALID JSON FORMAT\n")
        safe_input("PRESS ENTER...")
        return
    except Exception as e:
        print(f"\n❌ LOAD ERROR: {e}\n")
        safe_input("PRESS ENTER...")
        return

    print("🔍 PERFORMING PRE-VALIDATION...")
    time.sleep(0.3)
    
    # Quick validation
    valid, msg = Validator.quick_validate(data)
    if not valid:
        print(f"⚠️  VALIDATION WARNING: {msg.upper()}")
        print("⚙️  PROCEEDING WITH ENGINE ANALYSIS...")
        time.sleep(0.3)
    else:
        print(f"✅ PRE-VALIDATION: {msg.upper()}")

    # Get target name
    target = DataLoader.get_target_name(data)
    
    print(f"\n🎯 TARGET IDENTIFIED: {target.upper()}")
    time.sleep(0.3)
    
    # Initialize engine with all rules
    print(f"⚙️  INITIALIZING ENGINE WITH {len(DEFAULT_RULES)} RULES...")
    time.sleep(0.5)
    engine = Engine(DEFAULT_RULES)
    print("✅ ENGINE READY")
    
    # Run the engine (this is where the real magic happens)
    print("\n" + "="*60)
    print("🚀 EXECUTING ANALYSIS ENGINE")
    print("="*60)
    time.sleep(0.3)
    
    print("\n📋 EXECUTING COMPLETENESS RULES...")
    time.sleep(0.4)
    print("📋 EXECUTING CONSISTENCY RULES...")
    time.sleep(0.4)
    print("📋 EXECUTING STRUCTURE RULES...")
    time.sleep(0.4)
    print("🧮 CALCULATING SCORES...")
    time.sleep(0.3)
    print("🎯 DETERMINING VERDICT...")
    time.sleep(0.3)
    
    result = engine.run(data, target)
    
    print("\n✅ ENGINE EXECUTION COMPLETE")
    
    # Get file metadata
    size = json_file.stat().st_size
    
    # Display results
    print("\n" + "="*60)
    print("📊 ANALYSIS RESULTS")
    print("="*60)
    print(f"\n📄 FILE       : {json_file.name.upper()}")
    print(f"💾 SIZE       : {size} BYTES")
    print(f"🎯 TARGET     : {result.target.upper()}")
    print(f"📈 SCORE      : {result.score:.1f}/100")
    print(f"⚠️  RISK       : {result.risk}")
    print(f"🔍 FINDINGS   : {len(result.findings)}")
    print(f"\n{'='*60}")
    
    # Verdict with emoji
    verdict_emoji = "✅" if result.verdict == "PASSED" else "❌" if result.verdict == "FAILED" else "⚠️"
    print(f"{verdict_emoji} VERDICT    : {result.verdict}")
    print(f"📊 CONFIDENCE : {result.confidence:.2%}")
    print("="*60)
    
    # Show findings summary
    if result.findings:
        print(f"\n⚠️  FINDINGS DETECTED:")
        severity_counts = {}
        severity_emojis = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🔵',
            'INFO': '⚪'
        }
        for finding in result.findings:
            severity = finding.get('severity', 'UNKNOWN')
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        for severity, count in sorted(severity_counts.items(), reverse=True):
            emoji = severity_emojis.get(severity, '⚫')
            print(f"  {emoji} {severity:12} : {count}")
    else:
        print(f"\n✅ NO FINDINGS - SYSTEM IS CLEAN")
    
    # Store source path for exporters
    result.source_path = str(json_file)
    
    # Export using proper services
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    json_path = logs_dir / "result.json"
    html_path = logs_dir / "report.html"
    
    print("\n" + "="*60)
    print("💾 EXPORTING RESULTS")
    print("="*60)
    
    print("\n📝 GENERATING JSON REPORT...")
    time.sleep(0.3)
    JSONExporter.export(result, str(json_path))
    print(f"✅ JSON EXPORTED → {json_path}")
    
    print("\n🌐 GENERATING HTML REPORT...")
    time.sleep(0.5)
    HTMLReport.generate(result, str(html_path))
    print(f"✅ HTML EXPORTED → {html_path}")
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE - ALL OUTPUTS READY")
    print("="*60)

    safe_input("\nPRESS ENTER TO CONTINUE...")

# ==============================
# Main
# ==============================

def main():
    os.chdir(Path(__file__).parent)
    while True:
        clear_screen()
        show_banner()
        show_menu()
        if get_choice() == "1":
            analyze_system()
        else:
            print("\n" + "="*60)
            print("👋 THANK YOU FOR USING SINGULARITY-DELTA")
            print("="*60 + "\n")
            break

if __name__ == "__main__":
    main()