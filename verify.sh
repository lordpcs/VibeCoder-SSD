#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}        VIBE CODER - FULL TOOLCHAIN VERIFICATION      ${NC}"
echo -e "${BLUE}======================================================${NC}"

echo -n "1.  Git:       " && git --version
echo -n "2.  Node.js:   " && node --version
echo -n "3.  NPM:       " && npm --version
echo -n "4.  PNPM:      " && pnpm --version
echo -n "5.  Bun:       " && bun --version
echo -n "6.  GitHub:    " && gh --version | head -n 1
echo -n "7.  Railway:   " && railway --version
echo -n "8.  Claude:    " && claude --version
echo -n "9.  Codex:     " && codex --version
echo -n "10. Lazygit:   " && lazygit --version | head -n 1
echo -n "11. Eza:       " && eza --version | head -n 1
echo -n "12. Bat:       " && bat --version
echo -n "13. FZF:       " && fzf --version

echo -e "${GREEN}======================================================${NC}"
echo -e "${GREEN}✅ 13/13 herramientas instaladas y listas para usar.${NC}"
echo -e "${GREEN}======================================================${NC}"
