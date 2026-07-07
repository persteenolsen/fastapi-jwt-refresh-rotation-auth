import requests

BASE_URL = "http://localhost:8000"


# ==========================================================
# HELPERS
# ==========================================================

def login():

    response = requests.post(
        f"{BASE_URL}/tokens-spa",
        data={
            "username": "testuser",
            "password": "admin",
        },
    )

    assert response.status_code == 200

    print(f"   ✅ HTTP {response.status_code} OK - Login successful")

    return response.json()


def refresh_token_call(token):

    return requests.post(
        f"{BASE_URL}/refresh-token-spa",
        json=token,
    )


def logout_token(token):

    return requests.post(
        f"{BASE_URL}/logout",
        json=token,
    )


def cleanup():

    return requests.post(f"{BASE_URL}/cleanup-tokens")


def admin_purge():

    return requests.post(f"{BASE_URL}/admin/purge-refresh-tokens")


# ==========================================================
# INTEGRATION TESTS
# ==========================================================

def test_full_refresh_rotation_flow():

    print("\n==============================")
    print("REFRESH TOKEN ROTATION FLOW")
    print("==============================")

    session = login()
    refresh_token = session["refreshToken"]

    print("   ▶ Initial refresh token received")

    # First refresh
    response = refresh_token_call(refresh_token)
    assert response.status_code == 200

    print(f"   ✅ HTTP {response.status_code} OK - First refresh successful")

    new_refresh = response.json()["refreshToken"]

    # Old token should be invalid
    response = refresh_token_call(refresh_token)
    assert response.status_code == 401

    print(
        f"   ✅ HTTP {response.status_code} Unauthorized - "
        "Old refresh token correctly rejected"
    )

    # New token should work
    response = refresh_token_call(new_refresh)
    assert response.status_code == 200

    print(f"   ✅ HTTP {response.status_code} OK - Second refresh successful")


def test_logout_flow():

    print("\n==============================")
    print("LOGOUT FLOW")
    print("==============================")

    session = login()
    refresh_token = session["refreshToken"]

    response = logout_token(refresh_token)
    assert response.status_code == 200

    print(f"   ✅ HTTP {response.status_code} OK - Logout successful")


def test_refresh_after_logout_should_fail():

    print("\n==============================")
    print("REVOKED TOKEN REUSE")
    print("==============================")

    session = login()
    refresh_token = session["refreshToken"]

    logout_token(refresh_token)

    response = refresh_token_call(refresh_token)
    assert response.status_code == 401

    print(
        f"   ✅ HTTP {response.status_code} Unauthorized - "
        "Revoked refresh token correctly rejected"
    )


def test_cleanup_endpoint():

    print("\n==============================")
    print("TOKEN CLEANUP")
    print("==============================")

    response = cleanup()
    assert response.status_code == 200

    print(f"   ✅ HTTP {response.status_code} OK - Cleanup executed successfully")


def test_admin_purge():

    print("\n==============================")
    print("ADMIN PURGE")
    print("==============================")

    resp = admin_purge()
    assert resp.status_code == 200

    print(f"   ✅ HTTP {resp.status_code} OK - Admin purge executed successfully")


# ==========================================================
# RUNNER
# ==========================================================

if __name__ == "__main__":

    print("\n========================================")
    print("FASTAPI AUTH INTEGRATION TESTS")
    print("========================================")

    test_full_refresh_rotation_flow()
    test_logout_flow()
    test_refresh_after_logout_should_fail()
    test_cleanup_endpoint()

    # Requires authentication if enabled
    # test_admin_purge()

    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY")