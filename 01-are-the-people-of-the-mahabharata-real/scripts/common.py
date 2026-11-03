"""Shared name normalisation (transliteration- and OCR-insensitive)."""
import re, unicodedata
def ascii_fold(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if not unicodedata.combining(ch))
def norm(s):
    s = ascii_fold(s).lower()
    s = s.replace("^", "s").replace("$", "s").replace("!", "i")
    s = re.sub(r"[^a-z ]", "", s)
    for a, b in [("sh", "s"), ("ch", "c"), ("ri", "r"), ("ee", "i"), ("oo", "u"), ("w", "v"), ("ph", "p"), ("bh", "b"),
                 ("dh", "d"), ("th", "t"), ("kh", "k"), ("gh", "g"), ("jh", "j"), ("aa", "a"), ("ii", "i"), ("uu", "u")]:
        s = s.replace(a, b)
    s = re.sub(r"m(?=[tdsckgjn])", "n", s)          # Amendment 2: anusvara (Samtanu = Santanu)
    s = re.sub(r"(.)\1+", r"\1", s)
    return s.strip()
def ocr_variants(w):
    """OCR of the 1912 Index often reads long i as l (Pratlpa) or 1; generate both readings."""
    out = {w}
    if "l" in w: out.add(w.replace("l", "i"))
    return out
def skeleton(s):
    """Consonant skeleton, used to compare a father's name with a patronymic (Pariksit -> Pariksita)."""
    return re.sub(r"[aeiouy ]", "", norm(s))
def key(s):
    """Blocking key: normalised name without final vowel."""
    w = norm(s).split()[0] if norm(s) else ""
    return re.sub(r"[aeiou]+$", "", w)
