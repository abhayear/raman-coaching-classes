"""Copy admin panel and generate site-services.js for the published book/."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "book"
ADMIN_SRC = ROOT / "admin"
SERVICES = ROOT / "config" / "services.json"


def publish_admin_and_services() -> None:
    BOOK.mkdir(exist_ok=True)
    (BOOK / "assets").mkdir(exist_ok=True)

    if ADMIN_SRC.exists():
        dest = BOOK / "admin"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(ADMIN_SRC, dest)

    if SERVICES.exists():
        data = json.loads(SERVICES.read_text(encoding="utf-8"))
    else:
        data = {}

    js = "window.SITE_SERVICES = " + json.dumps(
        {
            "supabaseUrl": data.get("supabaseUrl", ""),
            "supabaseAnonKey": data.get("supabaseAnonKey", ""),
            "storageBucket": data.get("storageBucket", "centre-documents"),
            "coursePdfBucket": data.get("coursePdfBucket", "course-pdfs"),
            "razorpayKeyId": data.get("razorpayKeyId", ""),
        },
        indent=2,
    ) + ";\n"

    for path in (
        BOOK / "site-services.js",
        BOOK / "admin" / "site-services.js",
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(js, encoding="utf-8")

    loader = ADMIN_SRC / "documents-loader.js"
    if loader.exists():
        shutil.copy2(loader, BOOK / "assets" / "documents-loader.js")
        shutil.copy2(loader, BOOK / "admin" / "documents-loader.js")

    assets_src = ROOT / "assets"
    if assets_src.exists():
        for path in assets_src.glob("*.js"):
            shutil.copy2(path, BOOK / "assets" / path.name)