#!/bin/sh
# Runs the eval suite against the connector alone: this plugin with the same name, .mcp.json and
# mocks, but no skills. Compare its scores with CONTRIBUTING's eval command to see what the
# skills add over the tool descriptions alone: the eval's mock server is built from
# _tools.json, which holds no server instructions. With no skills, a grader on the Skill tool
# passes or fails by construction: compare the cases' other graders. Extra arguments go to
# `claude plugin eval`, such as --case, --runs 1, --model opus or --max-cost-usd.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir "$tmp/linkin-cpq"
cp -r "$root/.claude-plugin" "$root/.mcp.json" "$root/evals" "$tmp/linkin-cpq/"
rm -rf "$tmp/linkin-cpq/evals/results"
claude plugin eval "$tmp/linkin-cpq" --ablation none --judge-model opus --trust-plugin \
  --no-publish --output-dir "$root/evals/results/connector-only-$(date +%Y%m%dT%H%M%S)" "$@"
