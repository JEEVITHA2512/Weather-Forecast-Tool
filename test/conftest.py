import pytest
from typer.testing import CliRunner

# This is a fixture that will be used in all tests, must be passed as an argument to the test function
@pytest.fixture(scope="session")
def runner():
    return CliRunner()