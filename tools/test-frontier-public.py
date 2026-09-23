"""Acceptance check: newly published public sections enter the selector automatically."""

import importlib.util
import unittest
from pathlib import Path

from bs4 import BeautifulSoup


SCRIPT = Path(__file__).with_name("build-frontier-index.py")
spec = importlib.util.spec_from_file_location("build_frontier_index", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PublicIndexTest(unittest.TestCase):
    def test_new_section_is_included_without_item_rule(self):
        html = "<html><head><meta charset='utf-8'></head><body>"
        for number in range(1, 8):
            html += f"<button id='t{number}'>מושב {number}</button>"
            html += f"<div id='pane-s{number}'><section><h2>נושא {number}</h2><p>תוכן ציבורי {number}.</p></section></div>"
        soup = BeautifulSoup(html + "</body></html>", "html.parser")
        before = builder.build(str(soup).encode("utf-8"))
        section = BeautifulSoup(
            "<section><h2>טיפול בפניות שירות חדשות</h2><p>צוות השירות ממיין פניות חדשות.</p></section>",
            "html.parser",
        ).section
        soup.select_one("#pane-s6").append(section)
        after = builder.build(str(soup).encode("utf-8"))
        self.assertEqual(len(after["items"]), len(before["items"]) + 1)
        added = next(item for item in after["items"] if item["title"] == "טיפול בפניות שירות חדשות")
        self.assertEqual(added["source"], "https://guycoful.github.io/microsoft-frontier-2026/#s6")
        self.assertIn("צוות השירות ממיין פניות חדשות.", added["evidence"])

    def test_question_is_a_separate_item_with_its_answer(self):
        html = "<html><head><meta charset='utf-8'></head><body>"
        for number in range(1, 8):
            html += f"<button id='t{number}'>מושב {number}</button>"
            if number == 7:
                html += "<div id='pane-s7'><section><h2>שאלות ותשובות</h2>"
                html += "<details class='qa'><summary>מתי לבחור Power Automate?</summary><div class='qa-body'>"
                html += "<p>לתהליך קבוע עדיף Power Automate.</p><p>ההרצה דטרמיניסטית.</p>"
                html += "</div></details></section></div>"
            else:
                html += f"<div id='pane-s{number}'><section><h2>נושא {number}</h2><p>תוכן ציבורי {number}.</p></section></div>"
        result = builder.build((html + "</body></html>").encode("utf-8"))
        question = next(item for item in result["items"] if item["title"] == "מתי לבחור Power Automate?")
        self.assertIn("לתהליך קבוע", question["what"])
        self.assertIn("דטרמיניסטית", question["detail"])


if __name__ == "__main__":
    unittest.main()
