def non_empty_string(s):
    s = str(s)
    if not s:
        raise ValueError("Must not be empty string")
    return s
