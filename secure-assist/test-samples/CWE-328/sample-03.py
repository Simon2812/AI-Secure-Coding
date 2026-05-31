import hashlib

def hash_token(token: str) -> str:
    return hashlib.md5(token.encode()).hexdigest()

def is_valid_token(token: str, expected_hash: str) -> bool:
    computed = hashlib.md5(token.encode()).hexdigest()
    return computed == expected_hash

if __name__ == "__main__":
    t = "reset-token-abc123"
    h = hash_token(t)
    print(f"Token hash: {h}")
    print(f"Valid: {is_valid_token(t, h)}")
