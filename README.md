# 🚀 Entorno Contenerizado para Vibe Coder Next (Hybrid SDD + Vibe Coding)

Este proyecto combina la velocidad del **"Vibe Coding"** con el rigor y determinismo del marco **SDD (System-Driven Development)**: *"Spec on the Trunk, Vibe on the Leaves"*. 

Incluye un **Orquestador Agéntico con Dashboard Web (puerto 4040)** para supervisar agentes de IA (Claude Code, OpenAI Codex, subagentes autónomos), compilar especificaciones estructuradas y ejecutar compuertas de verificación y autocorrección (*self-healing loops*) en tiempo real.

> 🌐 **Dashboard Web en Vivo:** Inicia con `make dashboard` o `vibe dashboard` y abre [http://localhost:4040](http://localhost:4040).  
> 🛡️ **Comando SDD:** Valida contratos y especificaciones con `sdd lint` y comprueba invariantes con `sdd invariants`.

---

## 📦 Herramientas Incluidas (13/13)

| Herramienta | Comando CLI | Propósito |
| :--- | :--- | :--- |
| **Git** | `git --version` | Control de versiones |
| **Node.js** | `node --version` | Entorno JavaScript / TypeScript (v22 LTS) |
| **NPM** | `npm --version` | Gestor de paquetes tradicional |
| **PNPM** | `pnpm --version` | Gestor de paquetes ultrarrápido con ahorro de disco |
| **Bun** | `bun --version` | Runtime y ejecutor directo de TypeScript (`bun run file.ts`) |
| **GitHub CLI** | `gh --version` | Gestión de repositorios, PRs e issues desde la terminal |
| **Railway CLI** | `railway --version` | Despliegue e infraestructura en Railway |
| **Claude Code** | `claude --version` | Agente CLI oficial de Anthropic (`@anthropic-ai/claude-code`) |
| **OpenAI Codex** | `codex --version` | Agente CLI oficial de OpenAI (`@openai/codex`) |
| **Lazygit** | `lazygit --version` | Interfaz gráfica interactiva de Git en terminal |
| **Eza** | `eza --version` | Reemplazo moderno de `ls` con colores, iconos y árboles |
| **Bat** | `bat --version` | Reemplazo de `cat` con resaltado de sintaxis y paginación |
| **FZF** | `fzf --version` | Buscador interactivo difuso (*fuzzy finder*) |
| **Oh My Zsh** | `zsh` | Shell enriquecido con tema RobbyRussell |
| **Oh My Tmux** | `tmux` | Multiplexor de terminales con prefijos duales y paneles |

---

## ⚡ Aliases Rápidos para Vibe Coding

Dentro del contenedor tienes configurados estos atajos de 1 y 2 letras:

| Alias | Comando Real | Descripción |
| :--- | :--- | :--- |
| `help` | `vibe-help` | Mostrar guía completa de atajos y herramientas |
| `verify` | `vibe-verify` | Comprobar el estado de las 13 herramientas |
| `c` | `claude` | Iniciar Claude Code CLI |
| `cx` | `codex` | Iniciar OpenAI Codex CLI |
| `rw` | `railway` | CLI de despliegues en Railway |
| `lg` | `lazygit` | Abrir interfaz visual de Git |
| `pn` | `pnpm` | Ejecutar PNPM |
| `b` | `bun` | Ejecutar Bun |
| `dev` | `npm run dev` | Iniciar servidor de desarrollo |
| `build` | `npm run build` | Compilar proyecto |
| `ls` | `eza --icons=always` | Listar archivos con iconos |
| `ll` | `eza -la --icons=always` | Listar detalles y permisos |
| `tree` | `eza --tree --icons=always` | Vista de árbol del proyecto |
| `cat` | `bat --paging=never` | Ver archivo con código coloreado |

---

## 🔌 Plugins de Oh My Zsh: Guía de Uso y Atajos

| Plugin | ¿Qué hace? | Atajo / Cómo usarlo |
| :--- | :--- | :--- |
| **`zsh-autosuggestions`** | Muestra en gris la sugerencia más probable según tu historial. | • **`→` (Flecha derecha)** o **`End`**: Aceptar sugerencia completa.<br>• **`Alt + →`**: Aceptar solo la siguiente palabra. |
| **`zsh-syntax-highlighting`** | Colorea comandos en tiempo real para evitar errores de tipeo. | • **Verde**: Comando o ruta válida existente.<br>• **Rojo**: Comando desconocido o error de sintaxis.<br>• **Subrayado**: Ruta de archivo existente. |
| **`zsh-completions`** | Autocompletado interactivo extendido para `npm`, `git`, `docker`, `gh`, `railway`, etc. | • **`Tab`**: Abrir menú de opciones.<br>• **`Tab` repetido** o **Flechas `← ↑ ↓ →`**: Navegar y presionar `Enter` para elegir. |
| **`history-substring-search`** | Busca en el historial escribiendo cualquier parte del comando. | • Escribe cualquier parte del comando (ej: `login`).<br>• Presiona **`↑` (Flecha arriba)** para buscar hacia atrás.<br>• Presiona **`↓` (Flecha abajo)** para avanzar. |

---

## 🔍 Búsqueda Interactiva con FZF

* **`Ctrl + T`**: Busca cualquier archivo o carpeta en tu proyecto de forma difusa y lo inserta en la terminal.
* **`Ctrl + R`**: Abre el buscador interactivo de todo tu historial de comandos. Escribe lo que recuerdes y presiona `Enter`.

---

## 🪟 Atajos Básicos de Tmux (*Oh My Tmux*)

Prefijo configurado: **`Ctrl + a`** (o `Ctrl + b`)

| Acción | Atajo de Teclado |
| :--- | :--- |
| **Dividir panel horizontalmente** | `Ctrl + a` seguido de `-` (o `_`) |
| **Dividir panel verticalmente** | `Ctrl + a` seguido de `|` (o `\`) |
| **Moverse entre paneles** | `Ctrl + a` seguido de las flechas `← ↑ ↓ →` o `h j k l` |
| **Crear nueva ventana/pestaña** | `Ctrl + a` seguido de `c` |
| **Cambiar entre ventanas** | `Ctrl + a` seguido del número (`0`, `1`, `2`...) o `n` (siguiente) / `p` (anterior) |
| **Maximizar / Restaurar panel actual** | `Ctrl + a` seguido de `z` |
| **Activar / Desactivar Mouse** | `Ctrl + a` seguido de `m` *(Activo por defecto)* |
| **Seleccionar panel / Cambiar ventana** | **Clic con el mouse** |
| **Redimensionar paneles** | **Arrastrar bordes con el mouse** |
| **Scroll en historial** | **Rueda del mouse / Trackpad** |
| **Desconectarse de la sesión (sin cerrarla)** | `Ctrl + a` seguido de `d` (vuelves con `make shell` o `vibe`) |
| **Cerrar panel actual** | Escribir `exit` o `Ctrl + d` |

---

## 🧭 Marco Híbrido SDD (System-Driven Development) & Vibe Coding

El enfoque de este proyecto resuelve la fragilidad del *Vibe Coding* puro (alucinaciones, deriva arquitectónica y regresiones) encapsulando la experimentación rápida dentro de contratos e invariantes estrictos:

```
┌────────────────────────────────────────────────────────┐
│             Plano SDD (specs/system-blueprint.yaml)    │
│           Esquemas JSON, OpenAPI 3.1 & Invariantes     │
└───────────────────────────┬────────────────────────────┘
                            │ Compilación de Contexto
                            ▼
┌────────────────────────────────────────────────────────┐
│             Orquestador Agéntico (Puerto 4040)         │
│  Despacho de Tareas Estructuradas & Bucle de Calidad   │
└──────────────┬───────────────────────────┬─────────────┘
               │ Instrucciones             │ Auto-corrección
               ▼                           ▲
┌──────────────────────────────┐    ┌──────┴──────────────────────┐
│        Vibe Coding           │    │    Compuertas de Calidad    │
│ (Claude Code, Codex, Agents) │───▶│   (Tests, Linter, Esquemas) │
└──────────────────────────────┘    └─────────────────────────────┘
```

### Comandos SDD disponibles:
* `sdd lint`: Valida la integridad de `specs/system-blueprint.yaml`, contratos OpenAPI y manifiestos de tareas JSON.
* `sdd invariants`: Comprueba reglas de arquitectura (ej. usuario no-root, no fuga de API keys, scripts de verificación).
* `sdd compile-prompt <archivo.json>`: Sintetiza un paquete de prompts estructurado con contexto del sistema y compuertas de test.

---

## 🎛️ Dashboard Web de Operaciones (Mission Control)

El orquestador incluye una consola web reactiva construida en React + Vite + Tailwind CSS + xterm.js:

1. **Mission Control (Vibe Console):** Escribe en lenguaje natural lo que deseas construir, asocia el componente SDD objetivo y despacha misiones a **Claude Code**, **OpenAI Codex** o al **Subagente Autónomo**.
2. **Terminal Stream en Vivo:** Visualiza en streaming por WebSockets la terminal y salida del agente, con reconexión y auto-scroll.
3. **Bucle de Auto-Corrección (*Self-Healing*):** Si los tests o contratos fallan al finalizar la tarea del agente, el orquestador captura el error, prepara un prompt de recuperación y re-ejecuta el agente automáticamente (hasta 3 iteraciones).
4. **SDD Blueprint Studio:** Explora interactivamente la topología de componentes, puertos, contratos e invariantes.
5. **Salud del Sistema (13/13):** Monitoreo de uso de CPU/RAM, estado de claves de entorno y disponibilidad de las 13 herramientas CLI.

Para iniciar el dashboard:
```bash
make dashboard
# O desde tu terminal anfitrión:
python orchestrator/run.py
```
Accede desde tu navegador a: **[http://localhost:4040](http://localhost:4040)**

---

## ⚡ Inicio Rápido

### 1. Variables de Entorno (Opcional)
Copia la plantilla de entorno si cuentas con API Keys:
```bash
cp .env.example .env
```
Edita `.env` y agrega tus claves:
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

---

## 🛠️ Modos de Uso

### Opción A: Usando `make` (Recomendada)

1. **Construir e iniciar el contenedor:**
   ```bash
   make up
   ```
2. **Verificar todas las herramientas:**
   ```bash
   make verify
   ```
3. **Entrar a la terminal interactiva:**
   ```bash
   make shell
   ```
4. **Detener el contenedor:**
   ```bash
   make down
   ```

---

### Opción B: Visual Studio Code (Dev Containers)

1. Abre esta carpeta en VS Code.
2. Haz clic en **"Reopen in Container"** en la esquina inferior derecha.
3. VS Code abrirá la terminal directamente dentro del contenedor con las extensiones configuradas.

---

### Opción C: Comando Global `vibe` (En CUALQUIER carpeta de tu Mac)

Ya tienes instalado el comando `vibe` en tu sistema (`~/.local/bin/vibe`). Puedes navegar a cualquier carpeta o proyecto de tu computadora y lanzar el contenedor al instante:

```bash
# Entrar a cualquier carpeta
cd ~/Documents/mi-otro-proyecto

# Lanzar el entorno Vibe Coder ahí mismo con 1 comando:
vibe

# O ejecutar comandos específicos directamente:
vibe pnpm install
vibe claude
vibe lazygit
```

*(Si necesitas reinstalar el comando global en otra máquina, ejecuta `make install-cli`).*

---

## 🔑 Autenticación Centralizada en tu Mac (`~`)

Las credenciales se almacenan directamente en tu directorio personal de macOS (`~`):

* `~/.config/gh`: Configuración y tokens de GitHub CLI (**sin usar el Keychain de Mac**)
* `~/.railway`: Credenciales de Railway
* `~/.claude` y `~/.claude.json`: Sesiones de Claude Code
* `~/.codex`: Sesiones de OpenAI Codex

Esto permite:
1. **Compartir logins entre múltiples proyectos** en tu Mac.
2. **Inmunidad a Docker**: Reconstruir o recrear el contenedor no borra tus sesiones.

Dentro del contenedor (`make shell`):
* **GitHub:** `gh auth login`
* **Railway:** `railway login --browserless`
* **Claude Code:** `c` (o `claude`)
* **Codex CLI:** `cx` (o `codex`)

---

## 📜 Historial de Comandos por Proyecto (`.zsh_history` / `.bash_history`)

El historial de terminal es **independiente para cada proyecto**:
* Se guarda automáticamente en `.zsh_history` en la raíz de cada carpeta.
* Cada proyecto recuerda únicamente los comandos ejecutados en ese proyecto.
* Está protegido en `.gitignore` para no compartirse en tus commits.

---

## 🌐 Puertos Mapeados para Desarrollo Web

El contenedor expone hacia `localhost`:
- `3000`: Next.js / React / Remix
- `5173`: Vite / Vue / Svelte
- `8000`: FastAPI / Django
- `8080`: Servidores HTTP generales
