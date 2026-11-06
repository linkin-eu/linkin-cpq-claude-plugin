#!/bin/sh
# Zips the plugin for upload in Claude Desktop or claude.ai: dist/linkin-cpq-<version>.zip.
# Takes a commit or tag, HEAD by default. Only committed files go in; .gitattributes leaves
# out what customers don't need.
set -eu
ref=${1:-HEAD}
version=$(git show "$ref:.claude-plugin/plugin.json" | sed -n 's/^ *"version": *"\([^"]*\)".*/\1/p')
mkdir -p dist
out="dist/linkin-cpq-$version.zip"
git archive --format=zip --prefix=linkin-cpq/ -o "$out" "$ref"
echo "$out"
