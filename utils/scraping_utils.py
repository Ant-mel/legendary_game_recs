def drop_dot_make_int(string):
    """
    Removes '.' from summarised numbers, and drops the extra 0 to accomidate for it
    """

    if '.' in string:
        drop_dot = string.replace('.', '')[:-1]
        value = int(drop_dot)
    else:
        value = int(string)

    return value
