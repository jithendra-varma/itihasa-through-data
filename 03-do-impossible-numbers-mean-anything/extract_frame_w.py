"""Stage A, Frame W: year, battle, article and location from the pinned revision. The description column,
which can contain army figures, is dropped without being written or printed.
Run: python -I -X utf8 extract_frame_w.py <raw.wiki> <out.csv>"""
import csv
import re
import sys

raw = open(sys.argv[1], encoding="utf-8").read().replace("\r", "")

def strip_attr(cell):
    # "rowspan=2 | text" -> (attrs, text); a link's | is inside [[ ]], so only split outside brackets
    depth, i = 0, 0
    while i < len(cell):
        two = cell[i:i + 2]
        if two in ("[[", "{{"):
            depth += 1; i += 2; continue
        if two in ("]]", "}}"):
            depth -= 1; i += 2; continue
        if cell[i] == "|" and depth == 0:
            head = cell[:i]
            if head.strip() == "" or ("=" in head and not head.strip().startswith(("[[", "{{"))):
                return head, cell[i + 1:]
            break
        i += 1
    return "", cell

def split_inline(line):
    # split "a || b" outside brackets
    out, depth, cur, i = [], 0, "", 0
    while i < len(line):
        two = line[i:i + 2]
        if two in ("[[", "{{"):
            depth += 1; cur += two; i += 2; continue
        if two in ("]]", "}}"):
            depth -= 1; cur += two; i += 2; continue
        if two == "||" and depth == 0:
            out.append(cur); cur = ""; i += 2; continue
        cur += line[i]; i += 1
    out.append(cur)
    return out

def battle_fields(text):
    links = re.findall(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]", text)
    article = links[0][0].strip() if links else ""
    plain = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", text)
    plain = re.sub(r"\{\{[^}]*\}\}|<ref[^>]*/>|<ref.*?</ref>|<[^>]+>|'''?", "", plain, flags=re.S)
    return " ".join(plain.split()), article

def locations(text):
    names = re.findall(r"\{\{\s*(?:flag(?:icon|country|deco)?|flagu)\s*\|\s*([^|}]+)", text, flags=re.I)
    rest = re.sub(r"\{\{[^}]*\}\}", "", text)
    extra = re.sub(r"\[\[(?:[^\]|]+\|)?([^\]]+)\]\]", r"\1", rest).strip(" ,;?")
    out = [n.strip() for n in names]
    if extra and not out:
        out = [extra]
    uncertain = "?" in text or " or " in rest
    return "; ".join(out), uncertain

def year_num(y):
    y = y.replace("–", "-").replace("—", "-")
    m = re.search(r"(\d[\d,]*)\s*(BC|BCE|AD|CE)?", y)
    if not m:
        return ""
    n = int(m.group(1).replace(",", ""))
    era = m.group(2) or ("BC" if "BC" in y else "AD")
    if "century" in y.lower() and n < 40:
        n = n * 100 - 50
    return -n if era.startswith("BC") else n

rows, section, bad = [], "", []
spans = {}  # column -> [remaining rows, text]
for block in re.split(r"\n(?==)", raw):
    h = re.match(r"=+\s*(.*?)\s*=+", block)
    if h:
        section = h.group(1)
    for table in re.findall(r"\{\|.*?\n\|\}", block, flags=re.S):
        spans = {}
        for chunk in re.split(r"\n[ \t]*\|-", table)[1:]:
            cells = []
            for line in (l.lstrip() for l in chunk.split("\n")):
                if line.startswith("!") or line.startswith("|}"):
                    cells = None
                    break
                if line.startswith("|"):
                    cells += split_inline(line[1:])
                elif cells:
                    cells[-1] += " " + line
            if not cells:
                continue
            row, col, k = {}, 0, 0
            while k < len(cells) or col in spans:
                if col in spans:
                    spans[col][0] -= 1
                    row[col] = spans[col][1]
                    if spans[col][0] == 0:
                        del spans[col]
                    col += 1
                    continue
                attrs, text = strip_attr(cells[k]); k += 1
                rs = re.search(r"rowspan\s*=\s*\"?(\d+)", attrs)
                if rs and int(rs.group(1)) > 1:
                    spans[col] = [int(rs.group(1)) - 1, text]
                row[col] = text
                col += 1
            if 1 not in row:
                continue
            if len(row) == 5 and "{{flag" in row.get(2, "").lower():
                row = {0: row[0], 1: row[1], 2: row[2], 3: ""}  # extra cell is on the description side; never read
            if len(row) != 4:
                bad.append((section, len(row), battle_fields(row[1])[0][:40]))
                continue
            year = " ".join(re.sub(r"<ref.*?</ref>|<ref[^>]*/>|\{\{[^}]*\}\}|<[^>]+>", "", row.get(0, ""), flags=re.S).split())
            battle, article = battle_fields(row[1])
            loc, unc = locations(row.get(2, ""))
            rows.append(dict(section=section, year=year, year_num=year_num(year), battle=battle, article=article,
                             locations=loc, location_uncertain=unc))

with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "section", "year", "year_num", "battle", "article", "locations", "location_uncertain"])
    w.writeheader()
    for i, r in enumerate(rows, 1):
        w.writerow(dict(id=f"W{i:03d}", **r))
print("rows not 4 columns (dropped, flagged):", len(bad), bad[:8])
print(len(rows), "battles;", "sections:", sorted({r["section"] for r in rows}, key=lambda s: [r["section"] for r in rows].index(s)))
print("missing year:", sum(1 for r in rows if r["year_num"] == ""), "| missing article:", sum(1 for r in rows if not r["article"]),
      "| missing location:", sum(1 for r in rows if not r["locations"]))
