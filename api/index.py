import sys
from pathlib import Path

# Add project root directory to path for clean imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

# Middleware to resolve Vercel rewritten paths back to original incoming request URLs.
# Vercel rewrites requests to /api/index via vercel.json. The original path
# must be recovered so FastAPI can route to the correct handler.
@app.middleware("http")
async def vercel_rewrite_path_fix(request, call_next):
    path = request.scope.get("path", "")

    # Strategy 1: Check Vercel-specific headers for original URI.
    # Note: Do NOT use x-invoke-path as fallback, because x-invoke-path on Vercel is
    # internal and always evaluates to '/api/index', causing all requests to rewrite to '/'.
    raw_uri = (
        request.headers.get("x-forwarded-uri")
        or request.headers.get("x-matched-path")
        or request.headers.get("x-real-url")
    )

    clean_path = None
    if raw_uri:
        candidate = raw_uri.split("?")[0]
        # Ignore candidate if it points to /api/index or /api/index.py itself
        if candidate and candidate != "/api/index" and candidate != "/api/index.py" and not candidate.startswith("/api/index/") and not candidate.startswith("/api/index.py/"):
            clean_path = candidate

    if clean_path is None and path.startswith("/api/index"):
        # Strategy 2: Strip the Vercel rewrite prefix from the ASGI scope path if present
        clean_path = path[10:] or "/"  # len("/api/index") == 10
        if not clean_path.startswith("/"):
            clean_path = "/" + clean_path

    if clean_path is not None:
        request.scope["path"] = clean_path

    return await call_next(request)

