import sys
from pathlib import Path

# Add project root directory to path for clean imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

# Middleware to resolve Vercel rewritten paths back to original incoming request URLs
@app.middleware("http")
async def vercel_rewrite_path_fix(request, call_next):
    # Vercel Edge sets x-matched-path or x-forwarded-uri for rewritten requests
    matched_path = request.headers.get("x-matched-path") or request.headers.get("x-forwarded-uri")
    if matched_path:
        # Normalize and restore original path in ASGI scope
        request.scope["path"] = matched_path.split("?")[0]
    return await call_next(request)
