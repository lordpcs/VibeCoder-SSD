#!/usr/bin/env bash

# Colores ANSI
BOLD='\033[1m'
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
MAGENTA='\033[1;35m'
BLUE='\033[1;34m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

echo -e "${CYAN}================================================================================${NC}"
echo -e "${BOLD}${CYAN}               🚀 GUÍA DE ATAJOS Y HERRAMIENTAS — VIBE CODER NEXT               ${NC}"
echo -e "${CYAN}================================================================================${NC}"

echo -e "\n${BOLD}${MAGENTA}🤖 AGENTES DE IA Y CONTROL DE VERSIONES:${NC}"
echo -e "  ${YELLOW}c${NC}                 Inicia ${BOLD}Claude Code CLI${NC} (@anthropic-ai/claude-code)"
echo -e "  ${YELLOW}cx${NC}                Inicia ${BOLD}OpenAI Codex CLI${NC} (@openai/codex)"
echo -e "  ${YELLOW}rw${NC}                CLI de despliegues en ${BOLD}Railway${NC}"
echo -e "  ${YELLOW}lg${NC}                ${BOLD}Lazygit${NC} (interfaz gráfica interactiva de Git en terminal)"
echo -e "  ${YELLOW}gh${NC}                ${BOLD}GitHub CLI${NC} (gh auth login, gh pr, gh repo, etc.)"

echo -e "\n${BOLD}${BLUE}⚡ GESTORES DE PAQUETES Y EJECUCIÓN:${NC}"
echo -e "  ${YELLOW}pn${NC}                ${BOLD}PNPM${NC} (gestor de paquetes ultrarrápido)"
echo -e "  ${YELLOW}b${NC}                 ${BOLD}Bun${NC} (ejecutar TypeScript directo: ${GRAY}b run archivo.ts${NC})"
echo -e "  ${YELLOW}npm / node${NC}        Node.js v22 LTS y npm oficial"
echo -e "  ${YELLOW}dev${NC}               ${BOLD}npm run dev${NC} (iniciar servidor de desarrollo)"
echo -e "  ${YELLOW}build${NC}             ${BOLD}npm run build${NC} (compilar proyecto)"

echo -e "\n${BOLD}${GREEN}📂 UTILIDADES VISUALES MODERNAS (con iconos):${NC}"
echo -e "  ${YELLOW}ls${NC}                Listar archivos con iconos (${BOLD}eza${NC})"
echo -e "  ${YELLOW}ll${NC}                Listar detalles, permisos y tamaños con iconos"
echo -e "  ${YELLOW}tree${NC}              Vista de árbol de directorios con iconos"
echo -e "  ${YELLOW}cat <archivo>${NC}     Visualizar código con sintaxis coloreada (${BOLD}bat${NC})"

echo -e "\n${BOLD}${CYAN}🔍 BÚSQUEDA INTERACTIVA DIFUSA (FZF):${NC}"
echo -e "  ${MAGENTA}Ctrl + T${NC}          Buscador interactivo de archivos y carpetas en el proyecto"
echo -e "  ${MAGENTA}Ctrl + R${NC}          Buscador interactivo de comandos en tu historial"

echo -e "\n${BOLD}${YELLOW}🔌 PLUGINS DE OH MY ZSH:${NC}"
echo -e "  ${MAGENTA}→ (Flecha der)${NC}    Aceptar sugerencia de autocompletado (${GRAY}zsh-autosuggestions${NC})"
echo -e "  ${MAGENTA}Tab${NC}               Menú interactivo de opciones (${GRAY}zsh-completions${NC})"
echo -e "  ${MAGENTA}↑ / ↓${NC}             Buscar en el historial filtrando por cualquier texto"
echo -e "  ${GRAY}Sintaxis en vivo:${NC} ${GREEN}Verde${NC} = comando existente | ${BOLD}\033[31mRojo\033[0m = error de sintaxis"

echo -e "\n${BOLD}${MAGENTA}🪟 TMUX Y RATÓN / MOUSE (Prefijo: Ctrl + a  o  Ctrl + b):${NC}"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}-${NC}   Dividir panel horizontalmente"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}|${NC}   Dividir panel verticalmente"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}z${NC}   Maximizar / restaurar tamaño del panel actual"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}c${NC}   Crear nueva ventana/pestaña"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}d${NC}   Desconectarse de Tmux sin cerrar tus procesos"
echo -e "  ${MAGENTA}Ctrl+a${NC} seguido de ${YELLOW}m${NC}   Alternar soporte de ratón (On / Off)"
echo -e "  ${GREEN}Clic con Mouse${NC}    Seleccionar panel / Cambiar de pestaña"
echo -e "  ${GREEN}Arrastrar bordes${NC}  Redimensionar paneles con el ratón"
echo -e "  ${GREEN}Scroll Trackpad${NC}   Desplazarse por el historial de la consola"

echo -e "\n${BOLD}${CYAN}🔑 COMANDOS GLOBALES, SDD Y DASHBOARD:${NC}"
echo -e "  ${YELLOW}dashboard${NC}                 Iniciar el Orquestador y Dashboard Web (puerto 4040)"
echo -e "  ${YELLOW}sdd lint${NC}                  Validar especificaciones, esquemas y contratos SDD"
echo -e "  ${YELLOW}sdd invariants${NC}            Comprobar invariantes y compuertas del sistema"
echo -e "  ${YELLOW}help${NC}                      Mostrar esta pantalla de ayuda"
echo -e "  ${YELLOW}verify${NC}                    Comprobar el estado de las 13 herramientas"
echo -e "  ${YELLOW}welcome${NC}                   Volver a mostrar el banner de bienvenida"
echo -e "  ${YELLOW}gh auth login${NC}             Iniciar sesión en GitHub"
echo -e "  ${YELLOW}rw login --browserless${NC}    Iniciar sesión en Railway"
echo -e "${CYAN}================================================================================${NC}\n"
