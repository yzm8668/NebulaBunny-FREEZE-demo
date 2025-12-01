"""
NebulaBunny nb-freeze CLI (protocol layer only).

This package only contains:
- FREEZE-A / FREEZE-B protocol helpers
- Minimal CLI for generating and validating packages

It does NOT contain any drift/execution/stress/replay engine logic.
"""

__all__ = ["generate_a", "validate_a", "validate_b"]
__version__ = "0.1.0"
