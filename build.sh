#!/bin/sh
# Zips the plugin for upload in Claude Desktop or claude.ai: dist/linkin-cpq-<version>.zip.
# Takes a commit or tag, HEAD by default. Only the committed files named below go in, and
# .mcp.json with the connector's default address: Claude Desktop and claude.ai take a fixed URL,
# and only Claude Code reads LINKIN_CPQ_MCP_URL.
#
# A connector's https address after the commit builds a test zip for that connector instead:
# dist/linkin-cpq-<version>-dev-<commit>.zip, its version and display name marked dev and the
# commit. Its .mcp.json has no oauth block, since the default's client belongs to the default
# connector's sign-in: Claude registers its own where the other connector's sign-in lets it.
set -eu
ref=${1:-HEAD}
url=${2-}
version=$(git show "$ref:.claude-plugin/plugin.json" | sed -n 's/^ *"version": *"\([^"]*\)".*/\1/p')
mcp=$(git show "$ref:.mcp.json" | sed 's/\${LINKIN_CPQ_MCP_URL:-\([^}]*\)}/\1/')
[ -n "$version" ] || { echo "build.sh: no version in plugin.json" >&2; exit 1; }
case $mcp in *'${'*) echo "build.sh: .mcp.json still holds a variable" >&2; exit 1 ;; esac
mkdir -p dist
if [ -z "$url" ]; then
  mcp="$mcp
"
  out="dist/linkin-cpq-$version.zip"
  # --prefix doesn't reach a virtual file (git's 2.39 manual says it does; git doesn't), so its path
  # names the folder.
  git archive --format=zip --prefix=linkin-cpq/ --add-virtual-file="linkin-cpq/.mcp.json:$mcp" -o "$out" "$ref" -- \
    .claude-plugin/plugin.json skills assets README.md LICENSE PRIVACY.md CHANGELOG.md
else
  case $url in https://*) ;; *) echo "build.sh: the connector's address must start with https://" >&2; exit 1 ;; esac
  commit=$(git rev-parse --short "$ref^{commit}")
  version="$version-dev-$commit"
  mcp=$(git show "$ref:.mcp.json" | python3 -c '
import json, sys
d = json.load(sys.stdin)
for server in d["mcpServers"].values():
    server["url"] = sys.argv[1]
    server.pop("oauth", None)
print(json.dumps(d, indent=2))' "$url")
  manifest=$(git show "$ref:.claude-plugin/plugin.json" | python3 -c '
import json, sys
d = json.load(sys.stdin)
d["version"] = sys.argv[1]
d["displayName"] += " (dev " + sys.argv[2] + ")"
print(json.dumps(d, indent=2, ensure_ascii=False))' "$version" "$commit")
  out="dist/linkin-cpq-$version.zip"
  git archive --format=zip --prefix=linkin-cpq/ --add-virtual-file="linkin-cpq/.mcp.json:$mcp
" --add-virtual-file="linkin-cpq/.claude-plugin/plugin.json:$manifest
" -o "$out" "$ref" -- skills assets README.md LICENSE PRIVACY.md CHANGELOG.md
fi
echo "$out"
