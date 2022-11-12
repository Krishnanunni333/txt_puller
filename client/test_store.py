from click.testing import CliRunner

from store import ls

runner = CliRunner()

def test_ls():
    response = runner.invoke(ls)
    assert response.exit_code == 0

def test_wc():
    pass

def test_rm():
    pass

def test_update():
    pass

def test_add():
    pass

