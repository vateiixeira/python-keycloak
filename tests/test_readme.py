import pytest

from keycloak.keycloak_admin import KeycloakAdmin


def find_code_blocks(readme_text):
    code_blocks = list()
    start_index = readme_text.find("```python")
    if start_index == -1:
        return list()
    code_block_full = readme_text[start_index + 9 :]  # noqa: E203
    end_index = code_block_full.find("```")
    code_block = code_block_full[:end_index]
    code_blocks.append(code_block)
    code_blocks.extend(find_code_blocks(code_block_full[end_index + 3 :]))  # noqa: E203
    return code_blocks


# @pytest.mark.skip()
def test_readme(admin: KeycloakAdmin):
    admin.create_realm(payload={"realm": "example_realm", "enabled": True})
    admin.realm_name = "example_realm"
    admin.create_client(
        payload={
            "name": "example_client",
            "enabled": True,
            "protocol": "openid-connect",
            "publicClient": False,
            "redirectUris": ["http://localhost/*"],
            "webOrigins": ["+"],
            "clientId": "example_client",
            "secret": "secret",
            "clientAuthenticatorType": "client-secret",
        }
    )
    admin.create_user(
        payload={
            "username": "user",
            "email": "user@test.test",
            "enabled": True,
            "credentials": [{"type": "password", "value": "password"}],
        }
    )

    with open("README.md", "r") as fp:
        readme = fp.read()
    code_blocks = find_code_blocks(readme)
    for code in code_blocks:
        print("=" * 50)
        print(code)
        exec(code)
        print("OK")
        print("=" * 50)
