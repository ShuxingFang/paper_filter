import re
import unicodedata

def normalize_text(text):
    """
    Normalize Chinese and related punctuation and symbols in the input text to their English counterparts.

    Parameters:
        text (str): The input string containing Chinese and related symbols.

    Returns:
        str: The normalized string with English punctuation and symbols.
    """
    # 1. Normalize accented characters (optional)
    # Uncomment the following lines if you want to normalize accented characters
    normalized_text = unicodedata.normalize('NFKD', text)
    text = ''.join([c for c in normalized_text if not unicodedata.combining(c)])

    # 2. Replace IDEOGRAPHIC SPACE and other space variants with standard space
    text = text.replace("\u3000", " ")  # IDEOGRAPHIC SPACE
    text = text.replace("\u00a0", " ")  # Non-breaking space
    text = text.replace("\u2009", " ")  # Thin space

    # 3. Replace various dash characters with standard hyphen
    text = re.sub(r'[\u2010\u2013\u2014\u2212—]', '-', text)

    # 4. Create a translation table for punctuation and symbols
    punctuation_mapping = {
        '，': ',',
        '。': '.',
        '：': ':',
        '；': ';',
        '？': '?',
        '！': '!',
        '“': '"',
        '”': '"',
        '‘': "'",
        '’': "'",
        '（': '(',
        '）': ')',
        '【': '[',
        '】': ']',
        '《': '<',
        '》': '>',
        '…': '...',  # Ellipsis
        '＋': '+',
        '－': '-',    # Minus sign
        '×': '*',
        '÷': '/',
        '％': '%',
        '＃': '#',
        '＆': '&',
        '＠': '@',
        '｜': '|',
        '＼': '\\',
        '｀': '`',
        '＄': '$',
        '＾': '^',
        '＿': '_',
        '＝': '=',
        '｛': '{',
        '｝': '}',
        '￥': '¥',
        '≤': '<=',     # Less-than or equal to
        '®': '(R)',    # Registered sign
        '©': '(C)',    # Copyright sign
        '•': '-',       # Bullet
    }

    # 5. Add replacements for special characters
    # Depending on your context, decide how to handle these:
    special_characters_mapping = {
        'ï': 'i',        # Replace with 'i' or remove
        'β': 'beta',     # Replace with 'beta' or remove
    }

    # 6. Combine all mappings
    combined_mapping = {**punctuation_mapping, **special_characters_mapping}

    # 7. Create translation table
    translation_table = str.maketrans(combined_mapping)
    text = text.translate(translation_table)

    # 8. Optionally, remove any remaining unwanted characters
    # For example, remove any standalone 'ï' or 'β' if not handled
    # Uncomment if needed:
    # text = re.sub(r'[ïβ]', '', text)

    return text.strip()
