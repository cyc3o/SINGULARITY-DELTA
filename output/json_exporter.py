"""
JSON Exporter
Enterprise-grade export layer for Singularity-Delta
"""

import json
import uuid
import hashlib
from pathlib import Path
from typing import Optional, Any
from datetime import datetime

from core.result import AnalysisResult


class JSONExporter:
    """
    Exports analysis results to JSON files.
    Designed for audit, CI/CD, and enterprise compliance.
    """

    ENGINE_NAME = "Singularity-Delta"
    ENGINE_VERSION = "1.0.0"

    # -----------------------------
    # INTERNAL SAFE SERIALIZER
    # -----------------------------
    @staticmethod
    def _safe(obj: Any) -> Any:
        """
        Convert any object into JSON-safe form.
        """
        if obj is None:
            return None
        if isinstance(obj, (str, int, float, bool)):
            return obj
        if isinstance(obj, dict):
            return {str(k): JSONExporter._safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [JSONExporter._safe(v) for v in obj]
        if isinstance(obj, tuple):
            return [JSONExporter._safe(v) for v in obj]
        if isinstance(obj, datetime):
            return obj.isoformat()
        if hasattr(obj, "isoformat"):
            try:
                return obj.isoformat()
            except Exception:
                pass
        return str(obj)

    # -----------------------------
    # INPUT METADATA (HASHING)
    # -----------------------------
    @staticmethod
    def _input_metadata(result: AnalysisResult) -> Optional[dict]:
        """
        Generate input file metadata if source_path exists.
        """
        source = getattr(result, "source_path", None)
        if not source:
            return None

        try:
            p = Path(source)
            if not p.exists():
                return None

            sha256 = hashlib.sha256(p.read_bytes()).hexdigest()

            return {
                "path": str(p.resolve()),
                "filename": p.name,
                "size_bytes": p.stat().st_size,
                "sha256": sha256,
            }
        except Exception:
            return None

    # -----------------------------
    # CORE EXPORT
    # -----------------------------
    @staticmethod
    def export(
        result: AnalysisResult,
        filepath: str,
        pretty: bool = True
    ) -> None:
        """
        Export full analysis result to JSON file.
        """

        raw = result.to_dict()

        payload = {
            "engine": {
                "name": JSONExporter.ENGINE_NAME,
                "version": JSONExporter.ENGINE_VERSION,
                "run_id": str(uuid.uuid4()),
                "timestamp": JSONExporter._safe(result.timestamp),
            },
            "input": JSONExporter._input_metadata(result),
            "result": JSONExporter._safe(raw),
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            if pretty:
                json.dump(payload, f, indent=2, ensure_ascii=False)
            else:
                json.dump(payload, f, ensure_ascii=False)

    # -----------------------------
    # STRING EXPORT
    # -----------------------------
    @staticmethod
    def export_to_string(
        result: AnalysisResult,
        pretty: bool = True
    ) -> str:
        """
        Export result to JSON string.
        """

        raw = result.to_dict()

        payload = {
            "engine": {
                "name": JSONExporter.ENGINE_NAME,
                "version": JSONExporter.ENGINE_VERSION,
                "run_id": str(uuid.uuid4()),
                "timestamp": JSONExporter._safe(result.timestamp),
            },
            "input": JSONExporter._input_metadata(result),
            "result": JSONExporter._safe(raw),
        }

        if pretty:
            return json.dumps(payload, indent=2, ensure_ascii=False)
        return json.dumps(payload, ensure_ascii=False)

    # -----------------------------
    # SUMMARY EXPORT (MANAGEMENT)
    # -----------------------------
    @staticmethod
    def export_summary(
        result: AnalysisResult,
        filepath: str
    ) -> None:
        """
        Export condensed summary for executives / dashboards.
        """

        summary = {
            "engine": {
                "name": JSONExporter.ENGINE_NAME,
                "version": JSONExporter.ENGINE_VERSION,
                "timestamp": JSONExporter._safe(result.timestamp),
            },
            "target": result.target,
            "verdict": result.verdict,
            "risk": result.risk,
            "score": result.score,
            "total_findings": len(result.findings),
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                JSONExporter._safe(summary),
                f,
                indent=2,
                ensure_ascii=False
            )

    # -----------------------------
    # FINDINGS-ONLY EXPORT (CI/CD)
    # -----------------------------
    @staticmethod
    def export_findings_only(
        result: AnalysisResult,
        filepath: str
    ) -> None:
        """
        Export findings only for CI/CD pipelines.
        """

        data = {
            "engine": {
                "name": JSONExporter.ENGINE_NAME,
                "version": JSONExporter.ENGINE_VERSION,
            },
            "target": result.target,
            "verdict": result.verdict,
            "risk": result.risk,
            "findings": JSONExporter._safe(result.findings),
        }

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)