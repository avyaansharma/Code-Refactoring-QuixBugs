
def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
        if len(text) > 0 and text[0] == ' ':
            text = text[1:]

    lines.append(text)
    return lines
