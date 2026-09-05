# `adk web` discovers `agent.root_agent` in this package.
# The agent import is guarded so that tools which only need OKF parsing
# (e.g. build_viz.py) work even before `pip install google-adk`.
try:
    from . import agent  # noqa: F401
except ImportError:
    pass
