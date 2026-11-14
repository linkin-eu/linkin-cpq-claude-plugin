#!/bin/sh
# Zips the plugin for upload in Claude Desktop or claude.ai: dist/linkin-cpq-<version>.zip.
# Takes a commit or tag, HEAD by default. Only the committed files named below go in, and
# .mcp.json with the connector's default address: Claude Desktop and claude.ai take a fixed URL,
# and only Claude Code reads LINKIN_CPQ_MCP_URL.
set -eu
ref=${1:-HEAD}
version=$(git show "$ref:.claude-plugin/plugin.json" | sed -n 's/^ *"version": *"\([^"]*\)".*/\1/p')
mcp=$(git show "$ref:.mcp.json" | sed 's/\${LINKIN_CPQ_MCP_URL:-\([^}]*\)}/\1/')
case $mcp in *'${'*) echo "build.sh: .mcp.json still holds a variable" >&2; exit 1 ;; esac
mcp="$mcp
"
mkdir -p dist
out="dist/linkin-cpq-$version.zip"
# --prefix doesn't reach a virtual file (git's 2.39 manual says it does; git doesn't), so its path
# names the folder.
git archive --format=zip --prefix=linkin-cpq/ --add-virtual-file="linkin-cpq/.mcp.json:$mcp" -o "$out" "$ref" -- \
  .claude-plugin/plugin.json skills assets README.md LICENSE PRIVACY.md CHANGELOG.md
echo "$out"
