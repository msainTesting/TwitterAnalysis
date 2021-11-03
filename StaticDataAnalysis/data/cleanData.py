import re

import emoji


#Making use of functiosn to clean data

def removeURLS(data):
    text = re.sub(r'https?:\/\/\S*', '', str(data), flags=re.MULTILINE)
    return text


def removeEmojis(data):
    text = emoji.get_emoji_regexp().sub("", data)
    return text
