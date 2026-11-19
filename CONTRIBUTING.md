# Contributing

For LINKIN's maintainers of the plugin. Claude loads none of this.

```bash
claude plugin validate . --strict
evals/check-histories.sh            # the histories, the skills' shared paragraph and allowed-tools, the manifests
claude plugin eval . --runs 1 --ablation none --model opus --judge-model opus --max-cost-usd <n> -j 1 --no-publish
./build.sh <commit> <address>       # a test zip for another connector: dist/linkin-cpq-<version>-dev-<commit>.zip
./build.sh v<version>               # a past version's zip, rebuilt from its tag: dist/linkin-cpq-<version>.zip
```

These need jq, Python 3.9 or later, git 2.39 or later, and Claude Code signed in to Claude.

**The evals are paid.** `claude plugin eval` calls the model on your own Claude sign-in, and the
tools' answers come from `evals/*/mocks`. With the command above, the eval estimated the whole
suite at about $12, at list price, on 18 Nov 2026. It is the command the suite is measured with:
without `--runs 1` each case runs three times, and without `--ablation none` most cases run a
second time without the plugin. Set `--max-cost-usd`: it is checked before each run starts, and
runs already started finish, so the spend can pass it by the runs in flight, one with `-j 1`.
`--case <glob>` runs only the cases it names, and `--tag <tag>` the cases with that tag: `acting`,
the twelve cases run twice before a release, on when Claude issues, submits or revokes; `smoke`,
one case for each skill. Run from a checkout with no other copy of the plugin under it, such as a
git worktree: an eval has been seen to run a worktree's copy of each case too, and its first lines
then warn that cases share a name.

A zip is built with `git archive` from the paths `build.sh` names, so it holds only committed
files: the manifest, the connector, the skills, the icon, and the README, LICENSE, PRIVACY and
CHANGELOG. The eval mocks follow the API's answers, with made-up rates.

- **The tool list:** `evals/mocks/linkin-cpq/_tools.json` is the server's `tools/list` result as
  it serves it, indented two spaces; the server's maintainers provide it. Replace it whole when
  the server's tools change.
- **Generated mocks:** `python3 evals/tools/make_plan_mocks.py` writes the planning cases' priced
  fixtures and `plan_load` answers from made-up figures, as its docstring lists them, and keeps
  the copies `load-plan-inquiry-line`, `load-plan-app-host` and `per-kilo` hold of another case's
  mocks; `git diff` shows what moved. It keeps `load-plan-quotation`'s trucks and crates as written
  and works out their sentences and figures again. Every other mock, the refusals of
  `load-plan-missing-data` and `load-plan-not-theirs` among them, is edited as it stands.
  `python3 evals/tools/check_plan_mocks.py` checks the `plan_load` answers' consistency, and their
  shape too with `--openapi <path>` to the server's OpenAPI document, which its maintainers
  provide. CI runs the checker, without that document, and the generator, which must leave no
  diff.
- **The checks:** `evals/check-histories.sh` fails if a history's chain breaks, or its copy of a
  skill or of a mock's fixed answer is not the file as it stands; if a skill lacks the paragraph on
  a refusal of the account's details, or its paragraph differs from another's (each skill carries
  it whole, so change all five together); if a skill's `allowed-tools` is not exactly the
  connector's nine read-only tools, or those are not the tools `_tools.json` marks `readOnlyHint`;
  if `plugin.json` holds a key beyond its nine; and if the marketplace entry for this folder
  doesn't carry `plugin.json`'s name. CI runs it on every pull request.
- **Recorded histories:** a case's `history.jsonl` is a session recorded on another case and cut
  down to its messages, as its `case.yaml` says. `evals/check-histories.sh` fails where its copy of
  a skill or of a mock's fixed answer is no longer the file: update its copies, or record it again.
  `issue-as-prospect` and `too-many-inquiries` keep copies of `unlinked-inquiry`'s `get_account` and
  `price_inquiry` mocks, `profile-incomplete` of the same `get_account`, and
  `issue-inquiry-on-yes` of `profilink-only-inquiry`'s: change them together. To record one again,
  run the case its `case.yaml` names with `--keep-temp` (`unlinked-inquiry` for both
  `issue-as-prospect` and `too-many-inquiries`, which share one history: write the cut to both),
  cut the kept session's transcript with `python3 evals/tools/cut_history.py` (its docstring gives
  the steps), and run `evals/check-histories.sh`. A recording is a paid run, about $0.30 for one
  case.
- **Graders:** a `regex` grader takes a JavaScript pattern, case-insensitive with `flags: i` (no
  inline `(?i)`), and `match: not_contains` for one that must not appear. A case where a skill
  must not start uses `tool_used` on `Skill` with `min: 0`, `max: 0` and `arm: both`. A fixed
  mock answers the same whatever Claude sends, unless an `expect:` in its front matter stops the
  run, so a grader on what was sent uses `tool_used` with `input_match`, a pattern on the call's
  input as JSON, without flags and so case-sensitive: the quantity, length or coating class asked
  for, or the buyer's `customerReference`. A case's own `mocks/` override the shared
  `evals/mocks/` file by file.

Judge the evals with Opus (`--judge-model opus`): the default judge is too lenient for what a
buyer must not be told. Keep the rubrics short, one claim each, since the judge answers only PASS
or FAIL. `evals/connector-only.sh` runs the suite on the connector alone, with no skills and the
same judge, to show what the skills add over the tool descriptions alone; there a grader on the
Skill tool passes or fails by construction. Pass it `--runs 1 --model opus --max-cost-usd <n>`,
and compare it with the command above. Neither run carries the server's instructions: the
eval's mock server is built from `_tools.json`, a `tools/list` result, which holds none, while
Claude Code in use also loads the server's instructions.

The repository's `.mcp.json` names LINKIN's connector by its fixed address,
`https://cpq.mcp.linkin.eu/mcp`, and no OAuth client, as Anthropic's plugin docs have it, with a
fixed callback port, `47819`. The marketplace serves the file as it stands to every Claude app,
and Claude Desktop and claude.ai take only a fixed address. The connector's sign-in registers each
Claude app's own client: for claude.ai's callback, Claude Desktop's
`claude://claude.ai/mcp-auth-callback/sdk`, and Claude Code's loopback callback on port 47819, at
`localhost` or `127.0.0.1`. The port is fixed because the sign-in matches a callback exactly, port
included, so Claude Code registers its own client on the one port it accepts ("set `callbackPort`
on its own", Claude Code's MCP docs). The connector's earlier address, `https://mcp.linkin.eu/mcp`,
still answers for connectors added there, and the plugin no longer names it.

Every skill's `allowed-tools` lists the same nine tools, the connector's read-only ones, by full
name (`mcp__plugin_linkin-cpq_linkin-cpq__<tool>`), as a space-separated string, the Agent Skills
format's form. Claude Code runs them without asking in the turn that invokes the skill, and the
grant clears at the user's next message. Never a tool that issues, submits or revokes, and never a
wildcard, which would cover those too. `.claude-plugin/plugin.json` holds only `name`,
`displayName`, `description`, `version`, `author`, `homepage`, `repository`, `license` and
`keywords`: the directory listing fields (`icon`, `supportUrl`, `privacyPolicyUrl` and their kin)
are read only by Anthropic's directory, and Claude Desktop's marketplace strips them with a
warning. `evals/check-histories.sh` checks both. `assets/icon.png` is kept for a listing in
Anthropic's directory; `plugin.json` doesn't name it, for that reason.

**A test build for another connector:** `./build.sh <commit> <address>` builds the plugin at that
commit for the connector at that address, given in full with its path, as the default
`https://cpq.mcp.linkin.eu/mcp` is. Its file name, its version and its name in Claude say `dev` and
the commit. Its `.mcp.json` carries that address and the commit's `oauth` block, the callback port
with no client. It keeps the name `linkin-cpq`, so the two are never installed at once. To try it
in Claude Code, turn off any installed `linkin-cpq`, unzip the build and start
`claude --plugin-dir <folder>/linkin-cpq`. The address must start with `https://`, so a local
server without TLS can't be tried this way. To test it in Claude Desktop or claude.ai:

1. Under **Customize › Plugins**, delete **LINKIN CPQ**. If an Owner made it **Required** for your
   organization, ask them to lift that while you test. If a LINKIN connector is also listed under
   **Customize › Connectors**, disconnect it while you test.
2. Choose **Customize › Plugins › Add › Upload plugin** and pick the test zip. It shows as
   `LINKIN CPQ (dev <commit>)`.
3. On its **Connectors** tab, connect **linkin-cpq** and sign in with your account for that
   connector.
4. Set its tool permissions as in [Get started](README.md#claude-desktop-or-claudeai), step 5.

To go back, delete `LINKIN CPQ (dev <commit>)`, install **LINKIN CPQ** again from LINKIN's
marketplace ([Get started](README.md#claude-desktop-or-claudeai), steps 3 to 5), and connect again
any LINKIN connector you disconnected. If an Owner lifted **Required**, ask them to set it again.

Pull requests go to `dev`, squashed. One that changes what a customer gets adds a line under the
CHANGELOG's `## Unreleased`, in the words a customer reads. A release:

1. sets `PRIVACY.md`'s version line to the release day, and the Claude Code version CI installs
   (`.github/workflows/validate.yml`) to the one the release's evals ran on;
2. raises `version` in `.claude-plugin/plugin.json` and the version in the README's badge, and
   heads the CHANGELOG's Unreleased section with the version. Claude Code takes a new version
   only when this field changes;
3. merges `dev` into `main` with a merge commit, once the connector it needs is live: the
   marketplace serves `main`, and every Claude app takes the new version from there;
4. tags `main` `v<version>`. A tag marks what each version was, and lets a Claude Code user pin
   one, as `linkin-eu/linkin-cpq-claude-plugin#v<version>`.

Nothing else is published: no GitHub release and no zip. A past version's zip can be rebuilt from
its tag with `./build.sh v<version>`.
