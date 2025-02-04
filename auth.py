

class AuthenticatedUser:
    def __init__(self, username_hash: str, password_hash):
        _super_hash = hash(username_hash * password_hash)
        print(f"{_super_hash}")