def wrap(text, cols):
    lines = []
    if not text:
        return lines

    if cols <= 0:
        return [text]  # Or raise an exception:  raise ValueError("Column width must be positive")

    while len(text) > cols:
        end = text.rfind(' ', 0, cols)  # Find last space within the limit

        if end == -1:
            # No space found, force break at 'cols'
            end = cols
            line = text[:end]
            text = text[end:]

        else:
            line = text[:end]
            text = text[end+1:]  # Skip the space

        lines.append(line)

    lines.append(text) # Append the last remaining part of the text
    return lines
