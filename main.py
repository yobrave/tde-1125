import json
import pathlib
import os

CEILING = 200
STAMP = "two-days-excuse"
SIGN = "tde-1125"


def gather():
    anchor = pathlib.Path(os.path.realpath(__file__)).parent
    text = (anchor / "entry.txt").read_text(encoding="utf-8")
    text = text.strip()
    if len(text) > CEILING:
        print(json.dumps({"verdict": "too-long"}))
        raise SystemExit(0)
    return text


def place(text):
    where = pathlib.Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    where.mkdir(parents=True, exist_ok=True)
    slot = where / "entry.txt"
    slot.write_bytes((text + "\n").encode("utf-8"))
    if slot.read_text(encoding="utf-8").strip() != text:
        raise AssertionError("place failed")
    return slot


def finish(slot, text):
    print(json.dumps({"verdict": "accepted", "stamp": STAMP, "n": len(text), "slot": str(slot), "sign": SIGN}))


def chain():
    text = gather()
    slot = place(text)
    finish(slot, text)


chain()
