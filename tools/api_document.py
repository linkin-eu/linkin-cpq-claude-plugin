"""LINKIN's API document in the integrating-your-systems skill: the customer edition of the
server's OpenAPI document, copied from the server at a named commit and never edited by hand.

    python3 tools/api_document.py update <server checkout> <commit>
        Copies the customer edition at that commit into the skill's reference/ folder as
        openapi.json, writes overview.md from it, and writes stamp.json: the server's commit, the
        document's info.version and x-model-version, and each file's sha256. It prints every text
        of the document that changed since the copy before (all of them on a first copy), for the
        read before a push.
    python3 tools/api_document.py check [<server checkout>]
        Fails where openapi.json, overview.md and stamp.json are not what update writes from the
        document, or where the document fails a check below. Given the server's checkout, it also
        fails where openapi.json is not the server's file at the stamp's commit.

The checks, on every key and text of the document and every example value: no URL, host name,
email address or telephone number; no amount of money (a figure beside a currency, or a figure to
two decimals that is no measure) and no currency sign; no server and no sign-in scheme; and every
run of six digits or more, and every document number, one of the fictional ones in FICTIONAL.
update refuses to write a document that fails them. A finding is mended in the server's build,
never in the copy.

Copy only from a commit where the server's checks passed: there the frozen customer edition
equals the one the server generates. The stamp names the commit, since one version can name more
than one build of the document until that version is frozen for good; once 2.0.0 is released and
frozen for good, its version alone will do.
"""
import decimal
import hashlib
import json
import pathlib
import re
import subprocess
import sys

VERSION = "2.0.0"
SOURCE = f"openapi/customer/v{VERSION}.json"
REFERENCE = pathlib.Path(__file__).resolve().parent.parent / "skills/integrating-your-systems/reference"
DOCUMENT, OVERVIEW, STAMP = "openapi.json", "overview.md", "stamp.json"
METHODS = ("get", "put", "post", "delete", "options", "head", "patch", "trace", "query")
PATH_ITEM_KEYS = {"summary", "description", "parameters"}  # a path's $ref, or its own servers, is refused

# The server's fictional numbers, the only ones of these shapes the document may show: the
# customer 0009999999 (9999999 without its leading zeros), the geometry 7099999, the die 609999,
# an item's number with its zeros, 000010, and the documents LQ26000000 and LI26000000, numbers a
# year's sequence never issues.
FICTIONAL = {"0009999999", "9999999", "7099999", "609999", "000010", "LQ26000000", "LI26000000"}
DOCUMENT_NUMBER = r"(?<![A-Za-z0-9])L[A-Z]\d{8}(?!\d)"
CURRENCY = (r"(?:€|£|¥|лв|zł|\$|\b(?:EUR|BGN|USD|GBP|CHF|PLN|RON|RSD|HUF|CZK|TRY|MKD|DKK|SEK|NOK"
            r"|euros?|leva|lei|dollars?)\b)")
MEASURE = r"(?:mm|cm|m|km|kg|g|t|m²|m2|bytes|s|ms|metres|meters|tonnes|pieces)\b|%"
REFUSED = {
    "a URL": r"://",
    "an email address": r"@",
    "a host name": r"(?i)\blocalhost\b|\b(?:\d{1,3}\.){3}\d{1,3}\b|\b(?:[a-z0-9-]+\.)+(?:com|net|org|io|eu"
                   r"|bg|de|uk|us|ro|pl|gr|at|it|fr|nl|es|ch|cz|hu|rs|mk|tr|info|biz|cloud|app|dev|ai|co"
                   r"|tech|example|local|internal|lan|aws|azure)\b",
    "a telephone number": r"\+\d[\d ()-]{6,}\d",
    "an amount of money": CURRENCY + r"[`*_]*\s?[`*_]*\d|\d[\d,.]*[`*_]*\s?[`*_]*" + CURRENCY
                          + r"|(?<![\w.,])\d[\d,]*\.\d\d(?![\d.])(?!\s?(?:" + MEASURE + r"))",
    "a currency sign": r"[€£¥]|лв|zł|\$(?=\s?\d)|(?<=\d)\s?\$",
}
EXAMPLE_KEYS = {"example", "examples", "default", "const", "enum", "x-extensible-enum"}


def pointer(path, key):
    return f"{path}/{str(key).replace('~', '~0').replace('/', '~1')}"


def texts(node, path=""):
    """Every key and text in the document, and every number under an example's key, each with
    its JSON pointer."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield pointer(path, key) + "#key", key
            yield from texts(value, pointer(path, key))
    elif isinstance(node, list):
        for at, value in enumerate(node):
            yield from texts(value, pointer(path, at))
    elif isinstance(node, str):
        yield path, node
    elif isinstance(node, (int, float, decimal.Decimal)) and not isinstance(node, bool) and set(path.split("/")) & EXAMPLE_KEYS:
        yield path, str(node)


def sign_ins(node, path=""):
    """Where the document names a server or a sign-in, at any level."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("servers", "security", "securitySchemes") and value:
                yield pointer(path, key)
            yield from sign_ins(value, pointer(path, key))
    elif isinstance(node, list):
        for at, value in enumerate(node):
            yield from sign_ins(value, pointer(path, at))


def findings(doc):
    """What the document may not show, each with its JSON pointer."""
    found = [(path, "a server or a sign-in, which the skill never gives") for path in sign_ins(doc)]
    for path, text in texts(doc):
        for what, pattern in REFUSED.items():
            for match in re.finditer(pattern, text):
                found.append((path, f"{what}: {match.group(0)!r}"))
        numbers = [m for m in re.finditer(DOCUMENT_NUMBER, text)]
        for match in numbers:
            if match.group(0) not in FICTIONAL:
                found.append((path, f"a document number not among the fictional ones: {match.group(0)!r}"))
        for match in re.finditer(r"(?<!\d)\d{6,}(?!\d)", text):
            inside = any(n.start() < match.start() and match.end() <= n.end() for n in numbers)
            if not inside and match.group(0) not in FICTIONAL:
                found.append((path, f"a run of six digits or more not among the fictional ones: {match.group(0)!r}"))
    return found


def changes(old, new):
    """Every text of the document that changed, for the read before a push."""
    before, after = dict(texts(old)), dict(texts(new))
    for path in sorted(set(before) | set(after)):
        if before.get(path) != after.get(path):
            if path not in after:
                print(f"- {path}\n    {before[path]}")
            elif path not in before:
                print(f"+ {path}\n    {after[path]}")
            else:
                print(f"~ {path}\n    was: {before[path]}\n    now: {after[path]}")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def ref_name(ref):
    return ref.rsplit("/", 1)[-1] if isinstance(ref, str) else None


def resolve(doc, node):
    """A `$ref` within the document, followed."""
    while isinstance(node, dict) and "$ref" in node:
        ref = node["$ref"]
        if not ref.startswith("#/"):
            sys.exit(f"api_document: a reference outside the document: {ref}")
        node = doc
        for part in ref[2:].split("/"):
            node = node[part.replace("~1", "/").replace("~0", "~")]
    return node


def schema_name(content):
    """The schema a request or response carries, by name, or its media type where it names none."""
    for media, body in (content or {}).items():
        schema = (body or {}).get("schema") or {}
        name = ref_name(schema.get("$ref"))
        if name:
            return name
        items = ref_name((schema.get("items") or {}).get("$ref"))
        if items:
            return f"a list of {items}"
        return media
    return None


def codes(text, known):
    """The refusal codes a response's description names, of those the error schema lists."""
    return sorted(set(re.findall(r"`([A-Z][A-Z0-9_]{2,})`", text or "")) & known)


def overview(doc):
    """The overview the skill reads first: each operation in a line, what it needs, answers and
    refuses, then the schemas by name. Written from the document alone."""
    info, schemas = doc["info"], doc.get("components", {}).get("schemas", {})
    error_code = schemas.get("ApiError", {}).get("properties", {}).get("code", {})
    known = set(error_code.get("x-extensible-enum") or error_code.get("enum") or [])
    sections = [line[3:] for line in info.get("description", "").splitlines() if line.startswith("## ")]
    out = [
        "# LINKIN's API: an overview",
        "",
        f"Written by `tools/api_document.py` from `{DOCUMENT}` beside it: never edit it by hand.",
        "",
        f"{info['title']}, version {info['version']}"
        + (f" (model {info['x-model-version']})" if info.get("x-model-version") else "")
        + f", OpenAPI {doc['openapi']}. {info.get('summary', '')}".rstrip(),
        "",
        f"`{DOCUMENT}` is the whole document. Search it for what an answer needs, never read it whole:",
        '- an operation, by `"operationId": "<id>"`;',
        '- a schema, by `"<Name>":`, under `components`;',
        "- its own introduction, `info.description`, whose sections are: " + "; ".join(sections) + ".",
        "",
        "## Operations",
        "",
    ]
    for path, item in doc["paths"].items():
        unknown = set(item) - PATH_ITEM_KEYS - set(METHODS)
        if unknown:
            sys.exit(f"api_document: {path} holds {sorted(unknown)}, which the overview does not know")
        for method in METHODS:
            op = item.get(method)
            if not op:
                continue
            needs = []
            for p in [resolve(doc, p) for p in item.get("parameters", []) + op.get("parameters", [])]:
                needs.append(f"{p['in']} `{p['name']}`" + ("" if p.get("required") else " (optional)"))
            body = resolve(doc, op.get("requestBody"))
            if body:
                name = schema_name(body.get("content"))
                required = schemas.get(name, {}).get("required", []) if name in schemas else []
                needs.append(f"body {name}" + (f" (required: {', '.join(required)})" if required else ""))
            answers, refusals = [], []
            for status, response in op.get("responses", {}).items():
                response = resolve(doc, response)
                if status.startswith("2"):
                    answers.append(f"{status} {schema_name(response.get('content')) or 'no body'}")
                elif status.startswith("3"):
                    answers.append(f"{status} unchanged since asked" if status == "304" else status)
                else:
                    found = codes(response.get("description"), known)
                    refusals.append(f"{status}" + (f" {', '.join(found)}" if found else ""))
            line = f"- `{method.upper()} {path}` ({op.get('operationId', '')}): {op.get('summary', '').rstrip('.')}."
            line += f" Needs: {'; '.join(needs) if needs else 'nothing'}."
            line += f" Answers: {'; '.join(answers) if answers else 'nothing'}."
            if refusals:
                line += f" Refuses: {'; '.join(refusals)}."
            out.append(line)
    out += ["", f"## Schemas ({len(schemas)})", "", ", ".join(sorted(schemas)) + ".", ""]
    return "\n".join(out).encode()


def stamp(commit, doc, document, written):
    return (json.dumps({
        "note": "Written by tools/api_document.py: never edit this folder by hand.",
        "serverCommit": commit,
        "infoVersion": doc["info"]["version"],
        "modelVersion": doc["info"].get("x-model-version"),
        "sha256": {DOCUMENT: sha256(document), OVERVIEW: sha256(written)},
    }, indent=2) + "\n").encode()


def load(document):
    """The document, its figures as written: 190.50 stays 190.50, never the float 190.5."""
    return json.loads(document, parse_float=decimal.Decimal)


def update(checkout, commit):
    git = ["git", "-C", checkout]
    full = subprocess.run(git + ["rev-parse", "--verify", f"{commit}^{{commit}}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    document = subprocess.run(git + ["show", f"{full}:{SOURCE}"], capture_output=True, check=True).stdout
    doc = load(document)
    if doc["info"]["version"] != VERSION:
        sys.exit(f"{SOURCE} at {full} is version {doc['info']['version']}, not {VERSION}")
    found = findings(doc)
    if found:
        for path, what in found:
            print(f"{path}: {what}", file=sys.stderr)
        sys.exit(f"{SOURCE} at {full}: {len(found)} findings, nothing written; mend them in the server's build")
    written = overview(doc)
    before = load((REFERENCE / DOCUMENT).read_bytes()) if (REFERENCE / DOCUMENT).exists() else {}
    print("Every text of the document that changed since the copy before (all of them on a first copy):")
    changes(before, doc)
    REFERENCE.mkdir(parents=True, exist_ok=True)
    (REFERENCE / DOCUMENT).write_bytes(document)
    (REFERENCE / OVERVIEW).write_bytes(written)
    (REFERENCE / STAMP).write_bytes(stamp(full, doc, document, written))
    print(f"{REFERENCE / DOCUMENT}: {len(document):,} bytes from {full}")


def check(checkout=None):
    faults = []
    try:
        document = (REFERENCE / DOCUMENT).read_bytes()
        written = (REFERENCE / OVERVIEW).read_bytes()
        stamped_bytes = (REFERENCE / STAMP).read_bytes()
        commit = json.loads(stamped_bytes).get("serverCommit", "")
        doc = load(document)
    except (OSError, ValueError) as error:
        sys.exit(f"api_document: {error}")
    if written != overview(doc):
        faults.append(f"{OVERVIEW} is not what update writes from {DOCUMENT}")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        faults.append(f"{STAMP} names no server commit")
    if stamped_bytes != stamp(commit, doc, document, written):
        faults.append(f"{STAMP} is not what update writes for {DOCUMENT} and {OVERVIEW}: copy it again with update")
    if checkout:
        server = subprocess.run(["git", "-C", checkout, "show", f"{commit}:{SOURCE}"], capture_output=True)
        if server.returncode:
            faults.append(f"git could not read {SOURCE} at {commit} in {checkout}: {server.stderr.decode().strip()}")
        elif server.stdout != document:
            faults.append(f"{DOCUMENT} is not the server's {SOURCE} at {commit}")
    faults += [f"{path}: {what}" for path, what in findings(doc)]
    for fault in faults:
        print(f"api_document: {fault}", file=sys.stderr)
    if faults:
        sys.exit(1)
    print(f"api_document: {DOCUMENT}, {OVERVIEW} and {STAMP} agree ({commit[:8]})"
          + (", and the document is the server's" if checkout else ""))


if __name__ == "__main__":
    if sys.argv[1:2] == ["update"] and len(sys.argv) == 4:
        update(sys.argv[2], sys.argv[3])
    elif sys.argv[1:2] == ["check"] and len(sys.argv) in (2, 3):
        check(sys.argv[2] if len(sys.argv) == 3 else None)
    else:
        sys.exit(__doc__)
