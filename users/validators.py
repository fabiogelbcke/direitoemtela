def validate_password(pwd):
    if pwd is None:
        return False
    if len(pwd) < 8:
        return False
    if (any(x.isalpha() for x in pwd)
        and any(x.isdigit() for x in pwd)):
        return True
    else:
        return False
