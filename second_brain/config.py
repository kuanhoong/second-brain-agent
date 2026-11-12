"""Settings, read from the environment (see .env.example)."""
import os

# Pin an exact model ID. gemini-3.8-flash is the current stable Flash model
# (GA 2 September 2026). Check https://ai.google.dev/gemini-api/docs/models before a talk.
MODEL = os.environ.get("SECOND_BRAIN_MODEL", "gemini-3.8-flash")

# Your id for the OKF actor convention: reviews are recorded as `human:<OWNER>`.
OWNER = os.environ.get("SECOND_BRAIN_OWNER", "kuanhoong")
