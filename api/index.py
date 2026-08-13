import sys
from pathlib import Path

# Add project root directory to path for clean imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

# Middleware to resolve Vercel rewritten paths back to original incoming request URLs.
# Vercel rewrites all requests to /api/index via vercel.json.  The original path
# must be recovered so FastAPI can route to the correct handler.
@app.middleware("http")
async def vercel_rewrite_path_fix(request, call_next):
    path = request.scope.get("path", "")

    # Strategy 1: Check Vercel-specific headers for original URI
    raw_uri = (
        request.headers.get("x-forwarded-uri")
        or request.headers.get("x-invoke-path")
    )

    if raw_uri:
        clean_path = raw_uri.split("?")[0]
        # If the header itself contains the rewrite prefix, strip it
        if clean_path.startswith("/api/index"):
            clean_path = clean_path[10:] or "/"
            if not clean_path.startswith("/"):
                clean_path = "/" + clean_path
    elif path.startswith("/api/index"):
        # Strategy 2: Strip the Vercel rewrite prefix from the ASGI scope path.
        # On Vercel, every request arrives as /api/index or /api/index/<real_path>.
        clean_path = path[10:] or "/"  # len("/api/index") == 10
        if not clean_path.startswith("/"):
            clean_path = "/" + clean_path
    else:
        clean_path = None  # No fixup needed (local dev / non-Vercel)

    if clean_path is not None:
        request.scope["path"] = clean_path

    return await call_next(request)
