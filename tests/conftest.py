import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Habilita testes reais exclusivamente no banco foodagent_test.",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    ignorar = pytest.mark.skip(
        reason="Use --integration para testar o PostgreSQL real."
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(ignorar)
