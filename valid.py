def is_number(num):
    try:
        int(num)
        return True
    except ValueError:
        return False
