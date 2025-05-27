def wrap(text, cols):
    """ 
    Wrap Text

    Given a long string and a column width, break the string on spaces into a list of lines such that each line is no longer than the column width.

    Input:
        text: The starting text.
        cols: The target column width, i.e. the maximum length of any single line after wrapping.

    Precondition:
        cols > 0.

    Output:
        An ordered list of strings, each no longer than the column width, such that the concatenation of the strings returns the original text,
    and such that no word in the original text is broken into two parts unless necessary.  The original amount of spaces are preserved (e.g. spaces
    at the start or end of each line aren't trimmed.)
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(cols, int):
        raise TypeError("Column width must be an integer.")
    if cols <= 0:
        raise ValueError("Column width must be greater than zero.")

    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)

    lines.append(text) # Append the last line
    return lines
