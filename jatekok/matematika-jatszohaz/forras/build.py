"""A feladatsorokból önálló index.html fájlt készít."""

import json
from pathlib import Path
import re
import sys
from tempfile import TemporaryDirectory


SOURCE_DIR = Path(__file__).resolve().parent
DATA_DIR = SOURCE_DIR / "feladatsorok"
TEMPLATE = SOURCE_DIR / "index.template.html"
OUTPUT = SOURCE_DIR.parent / "index.html"
MARKER = "@@FELADATSOROK@@"
IDENTIFIER = re.compile(r"[a-zA-Z0-9_-]+")


def need(condition, location, message):
    if not condition:
        raise ValueError(f"{location} — {message}")


def is_text(value):
    return isinstance(value, str) and bool(value.strip())


def is_number(value):
    return type(value) is int and value >= 0


def is_number_list(value):
    return isinstance(value, list) and bool(value) and all(map(is_number, value))


def check_item(item, location, seen, text_fields):
    need(isinstance(item, dict), location, "JSON-objektumot vártam.")
    for key in ("id", *text_fields):
        need(is_text(item.get(key)), location, f"Hiányzó vagy üres mező ({key}).")
    identifier = item["id"]
    need(IDENTIFIER.fullmatch(identifier), location, f"Érvénytelen azonosító ({identifier}).")
    need(identifier not in seen, location, f"Ismétlődő azonosító ({identifier}).")
    seen.add(identifier)


def check_field(field, location):
    kind = field["kind"]
    answer = field.get("answer")
    if kind == "text":
        return
    if kind == "number":
        need(is_number(answer), location, "A válasz nemnegatív egész szám legyen.")
    elif kind in {"numberSequence", "numberSet"}:
        need(is_number_list(answer), location, "A válasz nemnegatív egész számokból álló lista legyen.")
    elif kind == "numberGroups":
        need(isinstance(answer, list) and bool(answer) and all(map(is_number_list, answer)),
             location, "A válasz egész számokat tartalmazó listákból álljon.")
    elif kind in {"cards", "choice"}:
        options = field.get("options")
        need(isinstance(options, list) and bool(options) and all(map(is_text, options)),
             location, "Legalább egy szöveges választási lehetőség kell (options).")
        correct = answer in options if kind == "choice" else (
            isinstance(answer, list) and bool(answer) and all(value in options for value in answer)
        )
        need(correct, location, "A helyes válasz a megadott lehetőségek közül kerüljön ki.")
    else:
        raise ValueError(f"{location} — Ismeretlen válaszmezőtípus ({kind}).")


def check_series(series, filename, seen_series):
    check_item(series, filename, seen_series, ("title", "description"))
    tasks = series.get("tasks")
    need(isinstance(tasks, list) and bool(tasks), filename, "Legalább egy feladat kell (tasks).")
    seen_tasks = set()
    for index, task in enumerate(tasks, start=1):
        location = f"{filename}, {index}. feladat"
        check_item(task, location, seen_tasks, ("title", "text", "solution"))
        for key in ("topics", "tags", "hints"):
            values = task.get(key)
            need(isinstance(values, list) and all(map(is_text, values)),
                 location, f"Szöveges elemekből álló lista szükséges ({key}).")
        need(len(task["hints"]) == 2, location, "Két segítséget kell megadni (hints).")
        fields = task.get("fields")
        need(isinstance(fields, list) and bool(fields), location, "Legalább egy válaszmező kell (fields).")
        seen_fields = set()
        for position, field in enumerate(fields, start=1):
            field_location = f"{location}, {position}. válaszmező"
            check_item(field, field_location, seen_fields, ("label", "kind"))
            check_field(field, field_location)


def build():
    series_list = []
    seen_series = set()
    for path in sorted(DATA_DIR.glob("*.json")):
        try:
            series = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"{path.name}, {error.lineno}. sor — Érvénytelen JSON.") from error
        check_series(series, path.name, seen_series)
        series_list.append(series)
    need(bool(series_list), DATA_DIR.name, "Nincs beolvasható JSON-feladatsor.")

    template = TEMPLATE.read_text(encoding="utf-8")
    need(template.count(MARKER) == 1, TEMPLATE.name, "A feladatsorok helyének egyszer kell szerepelnie.")
    payload = json.dumps(series_list, ensure_ascii=False, indent=2).replace("<", r"\u003c")
    html = template.replace(MARKER, payload, 1)

    with TemporaryDirectory(dir=OUTPUT.parent) as staging:
        temporary_file = Path(staging) / OUTPUT.name
        temporary_file.write_text(html, encoding="utf-8")
        temporary_file.replace(OUTPUT)
    task_count = sum(len(series["tasks"]) for series in series_list)
    print(f"Elkészült az {OUTPUT.name} ({len(series_list)} feladatsor, {task_count} feladat).")


if __name__ == "__main__":
    try:
        build()
    except (OSError, ValueError) as error:
        sys.exit(f"A build leállt. {error}")
