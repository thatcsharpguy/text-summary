import os
import time

import pytest
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.main import create_application
from app.config import get_settings, Settings


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))



@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), "tests", "docker-compose.yml")

@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down

@pytest.fixture(scope="session")
def db_url(docker_ip, docker_services):
    port = docker_services.port_for("web-db", 5432)
    db_name = "web_test"
    url = f"postgres://postgres:postgres@{docker_ip}:{port}/{db_name}"
    def test():
        try:
            v = docker_services._docker_compose.execute(f"exec web-db psql -U postgres -d {db_name} -c \"SELECT 1\"")
            return True
        except:
            return False

    # docker_services.wait_until_responsive(test, timeout=30.0, pause=1)
    time.sleep(2)
    return url

@pytest.fixture(scope="module")
def test_app_with_db(db_url):
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down