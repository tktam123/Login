import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# ── Auth config ────────────────────────────────────────────────────────────────
SECURITY_KEY = "ioweurlaksjdfoiquwerlkasjdf"   # move to env var in production
ALGORITHM    = "HS256"
TOKEN_TTL    = 30  # minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")