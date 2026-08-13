import sys
from pathlib import Path

# Add project root directory to path for clean imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

# Middleware to resolve Vercel rewritten paths back to original incoming request URLs
@app.middleware("http")
async def vercel_rewrite_path_fix(request, call_next):
    # x-forwarded-uri contains the exact original URI requested by the client
    raw_uri = request.headers.get("x-forwarded-uri") or request.headers.get("x-matched-path")
    if raw_uri:
        clean_path = raw_uri.split("?")[0]
        if clean_path.startswith("/api/index") and len(clean_path) > 10:
            clean_path = clean_path[10:]
            if not clean_path.startswith("/"):
                clean_path = "/" + clean_path
        elif clean_path == "/api/index":
            clean_path = "/"
        request.scope["path"] = clean_path
    return await call_next(request)
