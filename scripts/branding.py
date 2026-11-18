"""Load site branding; supports deploy base path via SITE_BASE_PATH env."""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "branding.json"


def load_branding() -> dict:
    defaults = {
        "siteName": "Raman Coaching Classes",
        "shortName": "Raman Coaching",
        "tagline": "MSc Chemistry coaching",
        "webBasePath": "/",
        "deployWebBasePath": "/raman-coaching-classes/",
    }
    if CONFIG.exists():
        data = json.loads(CONFIG.read_text(encoding="utf-8"))
        defaults.update(data)

    base = os.environ.get("SITE_BASE_PATH", "").strip()
    if not base:
        base = defaults.get("webBasePath") or "/"
    if base != "/" and not base.endswith("/"):
        base += "/"
    defaults["base"] = base
    return defaults