#!/usr/bin/env python3
"""Build a small public-only index from the published Frontier conference page."""

import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup


SOURCE = "https://raw.githubusercontent.com/guycoful/microsoft-frontier-2026/main/index.html"
PUBLIC_PAGE = "https://guycoful.github.io/microsoft-frontier-2026/"
OUTPUT = Path(__file__).with_name("frontier-public-index.json")


def clean(value):
    return re.sub(r"\s+([.,!?׃])", r"\1", re.sub(r"\s+", " ", value)).strip()


def first_sentence(value, maximum=280):
    value = clean(value)
    match = re.search(r"[.!?׃](?=\s|$)", value)
    if match and match.end() <= maximum:
        return value[: match.end()]
    return value[:maximum].rsplit(" ", 1)[0].rstrip(" ,;:") + ("…" if len(value) > maximum else "")


def evidence_sentences(container):
    """Keep source sentences intact so a role can select a concrete action."""
    result = []
    for node in container.find_all(("p", "li")):
        if node.name == "p" and node.find_parent("li"):
            continue
        if "srcs" in (node.get("class") or []):
            continue
        value = clean(node.get_text(" ", strip=True))
        for sentence in re.split(r"(?<=[.!?׃])\s+", value):
            sentence = clean(sentence)
            if len(sentence) >= 30 and sentence not in result:
                result.append(sentence[:320])
    return result[:40]


def build(html):
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for number in range(1, 8):
        pane = soup.select_one(f"#pane-s{number}")
        tab = soup.select_one(f"#t{number}")
        if not pane or not tab:
            raise ValueError(f"Missing public session {number}")
        session = clean(tab.get_text(" ", strip=True))
        for section_number, heading in enumerate(pane.select("section > h2"), start=1):
            section = heading.parent
            questions = section.select("details.qa")
            if questions:
                for question_number, question in enumerate(questions, start=1):
                    summary = question.find("summary")
                    body = question.select_one(".qa-body")
                    if not summary or not body:
                        continue
                    answers = [clean(p.get_text(" ", strip=True)) for p in body.find_all("p", recursive=False)
                               if "srcs" not in (p.get("class") or [])]
                    if not answers:
                        answers = [clean(p.get_text(" ", strip=True)) for p in body.find_all("p")]
                    answers = [answer for answer in answers if answer]
                    if not answers:
                        continue
                    items.append({
                        "id": f"s{number}-q{section_number}-{question_number}",
                        "session": session,
                        "title": clean(summary.get_text(" ", strip=True)),
                        "what": first_sentence(answers[0]),
                        "detail": first_sentence(answers[1]) if len(answers) > 1 else "",
                        "text": clean(question.get_text(" ", strip=True))[:2400],
                        "evidence": evidence_sentences(body),
                        "source": f"{PUBLIC_PAGE}#s{number}",
                    })
                continue
            paragraphs = [clean(p.get_text(" ", strip=True)) for p in section.find_all("p", recursive=False)]
            paragraphs = [p for p in paragraphs if p]
            if not paragraphs:
                continue
            title = clean(heading.get_text(" ", strip=True))
            text = clean(section.get_text(" ", strip=True))[:2400]
            items.append({
                "id": f"s{number}-{section_number}",
                "session": session,
                "title": title,
                "what": first_sentence(paragraphs[0]),
                "detail": first_sentence(paragraphs[1]) if len(paragraphs) > 1 else "",
                "text": text,
                "evidence": evidence_sentences(section),
                "source": f"{PUBLIC_PAGE}#s{number}",
            })
    if len(items) < 7:
        raise ValueError("Public source contained too few sourced sections")
    return {"source": PUBLIC_PAGE, "source_sha256": hashlib.sha256(html).hexdigest(), "items": items}


def main():
    with urlopen(Request(SOURCE, headers={"User-Agent": "Valor-Frontier-Public-Indexer"}), timeout=30) as response:
        html = response.read()
    index = build(html)
    result = json.dumps(index, ensure_ascii=False, separators=(",", ":")) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != result:
        OUTPUT.write_text(result, encoding="utf-8")
        print(f"Indexed {len(index['items'])} public sections")
    else:
        print(f"Unchanged: {len(index['items'])} public sections")


if __name__ == "__main__":
    main()
