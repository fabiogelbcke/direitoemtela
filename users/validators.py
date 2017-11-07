def validate_password(pwd):
    if pwd is None:
        return False
    if len(pwd) < 8:
        return False
    return True
