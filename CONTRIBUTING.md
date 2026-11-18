# Contributing

For LINKIN's maintainers of the plugin. None of this goes into the plugin's zip.

```bash
claude plugin validate . --strict
evals/check-histories.sh            # each recorded history's lines chained, so a resumed eval keeps them all
claude plugin eval . --no-publish --judge-model opus   # model calls on your own Claude sign-in; answers come from evals/*/mocks
./build.sh                          # dist/linkin-cpq-<version>.zip from HEAD, or ./build.sh <tag>
./build.sh <commit> <address>       # a test zip for another connector: dist/linkin-cpq-<version>-dev-<commit>.zip
```

The zip is built with `git archive` from the paths `build.sh` names, so it holds only committed
files: the manifest, the connector, the skills, the icon, and the README, LICENSE, PRIVACY and
CHANGELOG. The eval mocks follow the API's answers, with made-up rates.

- **The tool list:** `evals/mocks/linkin-cpq/_tools.json` is the server's `tools/list` result as
  it serves it, indented two spaces. Replace it whole when the server's tools change.
- **The planning cases' `plan_load` answers,** and the priced fixtures beside them
  (`fill-truck-minimum`'s, and `load-plan-inquiry-line`'s copy of its 200 bars), are generated:
  `python3 evals/tools/make_plan_mocks.py` rewrites them from made-up figures, and `git diff`
  shows what moved.
  `python3 evals/tools/check_plan_mocks.py` checks their consistency, and their shape too with
  `--openapi <path>` to the server's OpenAPI document.
- **Graders:** a `regex` grader takes a JavaScript pattern, case-insensitive with `flags: i` (no
  inline `(?i)`), and `match: not_contains` for one that must not appear. A case where a skill
  must not start uses `tool_used` on `Skill` with `min: 0`, `max: 0` and `arm: both`. A case's own
  `mocks/` override the shared `evals/mocks/` file by file.

Judge the evals with Opus (`--judge-model opus`): the default judge is too lenient for what a
buyer must not be told. Keep the rubrics short, one claim each, since the judge answers only PASS
or FAIL.

To try the plugin in Claude Code against another server that needs no sign-in, such as a local
one, set `LINKIN_CPQ_MCP_URL`: `LINKIN_CPQ_MCP_URL=<address> claude --plugin-dir .`. Unset, the
address is `https://mcp.linkin.eu/mcp`. The sign-in stays LINKIN's own, since Claude Code reads no
variable in the `oauth` block. The zip holds the default address, written by `build.sh`, since
Claude Desktop and claude.ai take a fixed one.

**A test build for another connector:** `./build.sh <commit> <address>` builds the plugin at that
commit for the connector at that address, given in full with its path, as the default
`https://mcp.linkin.eu/mcp` is. Its file name, its version and its name in Claude say `dev` and
the commit. Its `.mcp.json` names no OAuth client, since the default's client belongs to the
default connector's sign-in: Claude registers its own where the other connector's sign-in lets it.
It keeps the name `linkin-cpq`, so delete the released plugin first, and the two are never
installed at once. To test it in Claude Desktop or claude.ai:

1. Under **Customize › Plugins**, delete **LINKIN CPQ**. If an Owner made it **Required** for your
   organization, ask them to lift that while you test. If a LINKIN connector is also listed under
   **Customize › Connectors**, disconnect it while you test.
2. Choose **Customize › Plugins › Add › Upload plugin** and pick the test zip. It shows as
   `LINKIN CPQ (dev <commit>)`.
3. On its **Connectors** tab, connect **linkin-cpq** and sign in with your account for that
   connector. If Claude asks for an OAuth client ID, enter the one registered with that
   connector's sign-in.
4. Set its tool permissions as in [Get started](README.md#claude-desktop-or-claudeai), step 4.

To go back, delete `LINKIN CPQ (dev <commit>)`, follow
[Get started](README.md#claude-desktop-or-claudeai) from step 2, and connect again any LINKIN
connector you disconnected. If an Owner lifted **Required**, ask them to set it again.

Pull requests go to `dev`, squashed. A release:

1. sets `PRIVACY.md`'s version line to the release day;
2. raises `version` in `.claude-plugin/plugin.json`, which `build.sh` names the zip by, and the
   version in the README's badge and download link, and heads the CHANGELOG's Unreleased section
   with the version;
3. merges `dev` into `main` with a merge commit, then tags `main` `v<version>`: the marketplace
   installs from `main`;
4. attaches `./build.sh v<version>`'s zip to the GitHub release of that tag.
