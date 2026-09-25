"""Existing authenticated Life Patterns app plus the isolated birth-test route."""
from .birth_test_api import install_birth_test
from .life_patterns_v2_owner_deployed_app import create_secured_owner_app

app = create_secured_owner_app()
install_birth_test(app)
