import re
_BLACK = {"ciao","hello","hi","hola","bonjour","salve","grazie","thanks",
          "permesso","soggiorno","cittadinanza","help","info","servizi"}
_PATTERNS = [
    r"(?:mi chiamo|sono)\s+([A-Za-zÀ-ÖØ-öø-ÿ']{2,})",
    r"my name is\s+([A-Za-z]{2,})",
    r"je m'appelle\s+([A-Za-zÀ-ÖØ-öø-ÿ']{2,})",
    r"me llamo\s+([A-Za-zÀ-ÖØ-öø-ÿñÑ']{2,})",
    r"أنا اسمي\s+([^\s]{2,})",
]

def extract(text:str)->str|None:
    for p in _PATTERNS:
        m = re.search(p, text, flags=re.I)
        if m:
            cand = m.group(1).title()
            if cand.lower() not in _BLACK:
                return cand
    # fallback: single word
    tokens=[t for t in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ']{2,}",text)]
    if len(tokens)==1 and tokens[0].lower() not in _BLACK:
        return tokens[0].title()
    return None 