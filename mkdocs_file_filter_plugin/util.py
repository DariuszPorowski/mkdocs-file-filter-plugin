import logging

from mkdocs.utils import warning_filter

# ------------------------------------------
# Logging
# ------------------------------------------
log = logging.getLogger("mkdocs.plugins." + __name__)
log.addFilter(warning_filter)


PLUGIN_LABEL = "FILE-FILTER"


def _format_trace(*args):
    first = args[0]
    rest = [str(el) for el in args[1:]]
    text = "[%s] %s" % (PLUGIN_LABEL, first)
    return " ".join([text] + rest)


def info(*args):
    """
    General purpose print function, as trace,
    for the mkdocs-macros framework;
    it will appear unless --quiet option is activated
    """
    msg = _format_trace(*args)
    log.info(msg)


def debug(*args):
    """
    General purpose print function, as debug,
    for the mkdocs-macros framework;
    it will appear if --verbose option is activated
    """
    msg = _format_trace(*args)
    log.debug(msg)
