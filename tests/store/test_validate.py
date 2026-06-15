"""Test schema validation."""

import pytest
from voluptuous import Invalid

from supervisor.store.validate import DEFAULT_REPOSITORIES, repositories


def test_factory_assistant_addons_is_default_repository():
    """Test Factory Assistant add-ons are available as a default store."""
    assert "https://github.com/esaueng/factory-assistant-addons" in DEFAULT_REPOSITORIES


@pytest.mark.parametrize(
    ("repo_list", "valid"),
    [
        (["core", "local"], True),
        (["https://github.com/hassio-addons/repository"], True),
        (["not_a_url"], False),
        (["https://fail.com/duplicate", "https://fail.com/duplicate"], False),
    ],
)
async def test_repository_validate(repo_list: list[str], valid: bool):
    """Test repository list validate."""
    if valid:
        assert repositories(repo_list) == repo_list
    else:
        with pytest.raises(Invalid):
            repositories(repo_list)
