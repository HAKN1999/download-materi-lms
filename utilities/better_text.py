from string import punctuation, whitespace


def clean_string(text):
    for sub in punctuation + whitespace:
        text = text.replace(sub, "_")
    return text
