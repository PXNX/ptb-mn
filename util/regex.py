import re

WHITESPACE = re.compile(r"[\s\n]+$")
HASHTAG = re.compile(r"#\S+")
FLAG_EMOJI = re.compile(r"🏴|🏳️|([🇦-🇿]{2})")
BREAKING = re.compile(r"#eilmeldung[\r\n\s]*", re.IGNORECASE)
PATTERN_HTMLTAG = re.compile(r"<[^a>]+>")
