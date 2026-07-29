#!/bin/sh
# Install the codex-security Agent Skill into a coding agent's skills directory.
#
# Usage:
#   ./install.sh claude            # Claude Code, personal   -> ~/.claude/skills/
#   ./install.sh claude-project    # Claude Code, this repo  -> ./.claude/skills/
#   ./install.sh codex             # OpenAI Codex CLI        -> ~/.codex/skills/
#   ./install.sh pi                # pi coding agent         -> ~/.pi/agent/skills/
#   ./install.sh dir <path>        # any agent: copy into <path>/codex-security
set -eu

here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
src="$here/skills/codex-security"

usage() {
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
  exit 2
}

[ -d "$src" ] || { echo "error: $src not found" >&2; exit 1; }
[ $# -ge 1 ] || usage

case "$1" in
  claude)         dest="$HOME/.claude/skills" ;;
  claude-project) dest="$PWD/.claude/skills" ;;
  codex)          dest="$HOME/.codex/skills" ;;
  pi)             dest="$HOME/.pi/agent/skills" ;;
  dir)            [ $# -ge 2 ] || usage; dest="$2" ;;
  *)              usage ;;
esac

mkdir -p "$dest"
rm -rf "$dest/codex-security"
cp -R "$src" "$dest/codex-security"
echo "Installed codex-security skill to $dest/codex-security"
echo "Restart your agent (or reload skills) to pick it up."
