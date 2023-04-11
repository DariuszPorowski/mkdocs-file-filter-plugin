"""TODO."""

import pathlib

import pytest
from mkdocs.exceptions import PluginError

from mkdocs_file_filter_plugin.external_config import ExternalConfig


class TestExternalConfig:
    """TODO."""

    @pytest.mark.parametrize(
        ("test_input", "expected"),
        [
            ("tests/test_external_config_valid.yml", {"only_doc_pages": True}),
        ],
    )
    def test_load_external_config_valid(self, test_input: str, expected: dict) -> None:
        """TODO."""
        config_file_path = pathlib.Path(test_input)
        outcome = ExternalConfig().load(config_file_path)
        assert outcome == expected

    @pytest.mark.parametrize(
        ("test_input", "expected"),
        [
            ("tests/test_external_config_invalid.yml", "Wrong key 'foo' in {'foo': 'bar'}"),
        ],
    )
    def test_load_external_config_invalid(self, test_input: str, expected: str) -> None:
        """TODO."""
        config_file_path = pathlib.Path(test_input)
        with pytest.raises(PluginError) as exception:
            ExternalConfig().load(config_file_path)
        assert exception.match(expected)
