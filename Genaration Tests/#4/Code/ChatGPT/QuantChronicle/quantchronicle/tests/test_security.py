from app.security import hash_password, verify_password, create_access_token, decode_access_token

def test_password_hashing():
    hashed = hash_password("correct-horse-battery-staple")
    assert hashed != "correct-horse-battery-staple"
    assert verify_password("correct-horse-battery-staple", hashed)
    assert not verify_password("wrong-password", hashed)

def test_jwt_round_trip():
    token = create_access_token("42")
    assert decode_access_token(token) == "42"
