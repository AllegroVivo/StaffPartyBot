from __future__ import annotations

from typing         import Any
################################################################################

__all__ = ("NS", )

################################################################################
class _NotSet:

    def __eq__(self, other: Any) -> bool:

        return False

    def __bool__(self) -> bool:

        return False

    def __str__(self) -> str:

        return "`Not Set`"

NS = _NotSet()

################################################################################
