from pathlib import Path

import pytest
from wikmd.wiki import app, cfg, setup_wiki_template


@pytest.fixture()
def client():
    return app.test_client


@pytest.fixture(autouse=True, scope="session")
def wiki_path(tmpdir_factory):
    """Set up the temporary wiki path.

    autouse=True is needed as this behaves as a setup for the tests.
    """
    wiki_path = Path(tmpdir_factory.mktemp("wiki"))
    cfg.wiki_directory = wiki_path.as_posix()
    setup_wiki_template()
    return wiki_path
