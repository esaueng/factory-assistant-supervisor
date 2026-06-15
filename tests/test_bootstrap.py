"""Test bootstrap helpers."""

from pathlib import Path

from supervisor.bootstrap import seed_factory_defaults


def _make_source(tmp_path: Path) -> Path:
    """Create a minimal Factory Assistant defaults source tree."""
    source = tmp_path / "defaults"
    (source / "dashboards").mkdir(parents=True)
    (source / "configuration.yaml").write_text("default: config\n", encoding="utf-8")
    (source / "dashboards" / "factory-overview.yaml").write_text(
        "title: Plant overview\n", encoding="utf-8"
    )
    return source


def test_seed_into_empty_config(tmp_path: Path) -> None:
    """Defaults are copied into an unconfigured config dir."""
    source = _make_source(tmp_path)
    target = tmp_path / "config"
    target.mkdir()

    assert seed_factory_defaults(target, source=source) == 2

    config = target / "configuration.yaml"
    assert config.read_text(encoding="utf-8") == "default: config\n"
    assert (target / "dashboards" / "factory-overview.yaml").exists()


def test_seed_skips_when_already_configured(tmp_path: Path) -> None:
    """Seeding is a no-op when configuration.yaml already exists."""
    source = _make_source(tmp_path)
    target = tmp_path / "config"
    target.mkdir()
    config = target / "configuration.yaml"
    config.write_text("user: config\n", encoding="utf-8")

    assert seed_factory_defaults(target, source=source) == 0

    # Existing user config is untouched and nothing else is seeded.
    assert config.read_text(encoding="utf-8") == "user: config\n"
    assert not (target / "dashboards" / "factory-overview.yaml").exists()


def test_seed_never_overwrites_existing_file(tmp_path: Path) -> None:
    """An existing file is preserved even when configuration.yaml is absent."""
    source = _make_source(tmp_path)
    target = tmp_path / "config"
    (target / "dashboards").mkdir(parents=True)
    dashboard = target / "dashboards" / "factory-overview.yaml"
    dashboard.write_text("user: dashboard\n", encoding="utf-8")

    # configuration.yaml is seeded, but the pre-existing dashboard is kept.
    assert seed_factory_defaults(target, source=source) == 1
    assert (target / "configuration.yaml").exists()
    assert dashboard.read_text(encoding="utf-8") == "user: dashboard\n"


def test_seed_noop_when_source_missing(tmp_path: Path) -> None:
    """No defaults source -> no-op (e.g. development environment)."""
    target = tmp_path / "config"
    target.mkdir()

    assert seed_factory_defaults(target, source=tmp_path / "does-not-exist") == 0
    assert not (target / "configuration.yaml").exists()


def test_seed_is_idempotent(tmp_path: Path) -> None:
    """A second run after a successful seed copies nothing more."""
    source = _make_source(tmp_path)
    target = tmp_path / "config"
    target.mkdir()

    assert seed_factory_defaults(target, source=source) == 2
    assert seed_factory_defaults(target, source=source) == 0
