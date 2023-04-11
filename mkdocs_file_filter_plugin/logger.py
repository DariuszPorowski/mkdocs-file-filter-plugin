"""Generic utils."""

import logging

from mkdocs.utils import warning_filter

# ------------------------------------------
# Logging
# ------------------------------------------
log = logging.getLogger("mkdocs.plugins." + __name__)
log.addFilter(warning_filter)

PLUGIN_LABEL = "FILE-FILTER"


def _format_trace(*args: object) -> str:
    """Format the message to be printed."""
    first = args[0]
    rest = [str(el) for el in args[1:]]
    text = f"[{PLUGIN_LABEL}] {first}"
    return " ".join([text, *rest])


def info(*args: object) -> None:
    """General purpose print function, as trace, for the mkdocs-macros framework.

    It will appear unless --quiet option is activated.
    """
    msg = _format_trace(*args)
    log.info(msg)


def debug(*args: object) -> None:
    """General purpose print function, as debug, for the mkdocs-macros framework.

    It will appear if --verbose option is activated.
    """
    msg = _format_trace(*args)
    log.debug(msg)
