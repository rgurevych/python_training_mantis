
import pytest
import json
import os.path
import importlib
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

@pytest.fixture
def app(request):
    global fixture
    browser = request.config.getoption("--browser")
    web_config = loadconfig(request.config.getoption("--target"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, base_url=web_config["baseURL"])
    #fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


@pytest.fixture(scope = "session", autouse=True)
def stop(request):
    def logout_and_destroy():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(logout_and_destroy)
    return fixture


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--target", action="store", default="target.json")

