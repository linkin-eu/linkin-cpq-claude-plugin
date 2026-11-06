#!/bin/sh
# Zips the plugin for upload in Claude Desktop or claude.ai: dist/linkin-cpq-<version>.zip.
# Takes a commit or tag, HEAD by default. Only the committed files named below go in.
set -eu
ref=${1:-HEAD}
version=$(git show "$ref:.claude-plugin/plugin.json" | sed -n 's/^ *"version": *"\([^"]*\)".*/\1/p')
mkdir -p dist
out="dist/linkin-cpq-$version.zip"
git archive --format=zip --prefix=linkin-cpq/ -o "$out" "$ref" -- \
  .claude-plugin/plugin.json .mcp.json skills assets README.md LICENSE PRIVACY.md CHANGELOG.md
echo "$out"
