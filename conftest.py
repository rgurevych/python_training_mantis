import ftputil
import pytest
import json
import os.path
from fixture.application import Application


fixture = None
target = None

def loadconfig(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as c_file:
            target = json.load(c_file)
    return target


@pytest.fixture(scope = "session")
def config(request):
    return loadconfig(request.config.getoption("--target"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)
    fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture


@pytest.fixture(scope = "session", autouse=True)
def stop(request):
    def logout_and_destroy():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(logout_and_destroy)
    return fixture


@pytest.fixture(scope = "session", autouse=True)
def config_server(request, config):
    install_server_config(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    def finalize():
        restore_server_config(config["ftp"]["host"], config["ftp"]["username"], config["ftp"]["password"])
    request.addfinalizer(finalize)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")


def install_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            remote.remove("config/config_inc.php.bak")
        if remote.path.isfile("config/config_inc.php"):
            remote.rename("config/config_inc.php", "config/config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources/config_inc.php"), "config/config_inc.php")


def restore_server_config(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config/config_inc.php.bak"):
            if remote.path.isfile("config/config_inc.php"):
                remote.remove("config/config_inc.php")
            remote.rename("config/config_inc.php.bak", "config/config_inc.php")
