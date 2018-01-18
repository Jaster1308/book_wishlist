import os


def read(file, cb=None):
    if cb:
        try:
            with open(file) as f:
                data = f.read()
                cb(data)
        except FileNotFoundError:
            # First time program has run. Assume no books.
            pass
    else:
        with open(file) as f:
            try:
                counter = int(f.read())
            except ValueError:
                counter = None
            return counter


def write(directory, file, output):
    try:
        os.mkdir(directory)
    except FileExistsError:
        pass  # Ignore - if directory exists, don't need to do anything.

    with open(file, 'w') as f:
        f.write(str(output))
