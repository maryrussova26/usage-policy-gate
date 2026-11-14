"""Text normalisation used ONLY to detect obfuscated requests (never to help produce them)."""
import re
import unicodedata

_ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍⁠﻿­"), None)

# Cyrillic letters that look like Latin ones.
_CYR2LAT = str.maketrans({
    "а": "a", "в": "b", "е": "e", "к": "k", "м": "m", "н": "h", "о": "o", "р": "p",
    "с": "c", "т": "t", "у": "y", "х": "x", "і": "i", "ј": "j",
})
_LAT2CYR = str.maketrans({v: k for k, v in {
    "а": "a", "в": "b", "е": "e", "к": "k", "м": "m", "н": "h", "о": "o", "р": "p",
    "с": "c", "т": "t", "у": "y", "х": "x"}.items()})
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s"})
_SPACED = re.compile(r"\b(?:[a-zа-яё][\s.\-_*]){4,}[a-zа-яё]\b", re.I)


def basic(text: str) -> str:
    t = unicodedata.normalize("NFKC", text).translate(_ZERO_WIDTH)
    return t.casefold()


def _fix_mixed_script(tok: str) -> str:
    has_cyr = re.search(r"[а-яё]", tok) is not None
    has_lat = re.search(r"[a-z]", tok) is not None
    return tok.translate(_CYR2LAT) if has_cyr and has_lat else tok


def _fix_mixed_to_cyr(tok: str) -> str:
    has_cyr = re.search(r"[а-яё]", tok) is not None
    has_lat = re.search(r"[a-z]", tok) is not None
    return tok.translate(_LAT2CYR) if has_cyr and has_lat else tok


def variants(text: str):
    """Yield (normalised_text, obfuscation_flag). First item is the plain form."""
    base = basic(text)
    yield base, False
    out = []
    flagged = False
    zero = unicodedata.normalize("NFKC", text) != unicodedata.normalize("NFKC", text).translate(_ZERO_WIDTH)
    if zero:
        flagged = True
    toks = re.split(r"(\s+)", base)
    fixed = [_fix_mixed_script(t) for t in toks]
    if fixed != toks:
        flagged = True
    s = "".join(fixed)
    # collapse "m a l w a r e" / "m.a.l.w.a.r.e"
    def _join(m):
        return re.sub(r"[\s.\-_*]", "", m.group(0))
    s2 = _SPACED.sub(_join, s)
    if s2 != s:
        flagged = True
    # leetspeak only for tokens mixing letters and digits/symbols
    def _leet(m):
        w = m.group(0)
        return w.translate(_LEET) if re.search(r"[a-z]", w) and re.search(r"[01345@$7]", w) else w
    s3 = re.sub(r"\S+", _leet, s2)
    if s3 != s2:
        flagged = True
    if flagged and s3 != base:
        yield s3, True
    cyr = "".join(_fix_mixed_to_cyr(t) for t in toks)
    if cyr != base:
        yield cyr, True
