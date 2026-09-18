# 📖 Guía de Clonación e Instalación — Vibe Coder Next

Esta guía está diseñada para que cualquier compañero del curso pueda clonar este repositorio y tener el entorno completo con **13 herramientas de IA y desarrollo** funcionando en menos de 3 minutos, sin importar si usa **Linux**, **Windows (WSL2)** o **macOS**.

---

## 📋 Requisitos Previos por Sistema Operativo

### 🐧 1. Si estás en Linux (Ubuntu / Debian / Fedora / Arch)
1. Tener instalado **Docker** y **Docker Compose**:
   ```bash
   # En Ubuntu/Debian:
   sudo apt update && sudo apt install -y docker.io docker-compose-v2 make git
   ```
2. Asegurar que tu usuario pueda usar Docker sin `sudo`:
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

---

### 🪟 2. Si estás en Windows (Recomendado con WSL2)
1. **Instalar WSL2 (Ubuntu):**
   Abre PowerShell como Administrador y ejecuta:
   ```powershell
   wsl --install -d Ubuntu
   ```
   *(Reinicia tu PC si te lo solicita).*
2. **Instalar Docker Desktop para Windows:**
   - Descárgalo desde [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
   - En la configuración de Docker Desktop:  
     `Settings` $\rightarrow$ `General` $\rightarrow$ Marca **"Use the WSL 2 based engine"**.  
     `Settings` $\rightarrow$ `Resources` $\rightarrow$ `WSL Integration` $\rightarrow$ Activa tu distribución **Ubuntu**.
3. **⚠️ IMPORTANTE para Windows:**  
   Abre tu terminal de **Ubuntu (WSL2)** y clona el proyecto **dentro del sistema de archivos de Linux** (ej: `/home/tu-usuario/proyectos/`), **NO** en la unidad `C:\` de Windows. Esto garantiza que el rendimiento sea hasta 10x más rápido.

---

### 🍏 3. Si estás en macOS (Intel o Apple Silicon)
1. Tener instalado **Docker Desktop** para Mac: [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop).
2. Tener instaladas las Command Line Tools de Xcode (para tener `make` y `git`):
   ```bash
   xcode-select --install
   ```

---

### 🔤 Fuente Recomendada para Ver Todos los Iconos (Nerd Fonts)
Para ver los iconos de archivos de `eza` (logos de Docker, Git, JS, etc.) y los símbolos de Tmux en tu terminal:
* **En VS Code:** Ya está preconfigurado automáticamente en el contenedor.
* **En tu terminal (iTerm2, Terminal.app, Warp, Windows Terminal):** Instala una **Nerd Font** como **FiraCode Nerd Font** o **MesloLGS NF** ([nerdfonts.com](https://www.nerdfonts.com/font-downloads)) y selecciónala como fuente de tu terminal.
  ```bash
  # En macOS con Homebrew:
  brew install --cask font-fira-code-nerd-font
  ```

---

## 🚀 Paso a Paso: Clonar y Poner en Marcha

### Paso 1: Clonar el Repositorio
Abre tu terminal (en Linux/Mac) o tu terminal de **Ubuntu WSL2** (en Windows):

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DE_LA_CARPETA>
```

---

### Paso 2: Crear el archivo de Variables de Entorno (Opcional)
Si cuentas con tus API Keys de Anthropic (Claude) u OpenAI (Codex), crea tu archivo `.env`:

```bash
cp .env.example .env
```
Edita `.env` con tu editor favorito (`nano .env` o `code .env`) y coloca tus claves:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
```
*(Si no tienes claves todavía, puedes omitir este paso o autenticarte luego interactivamente).*

---

### Paso 3: Construir e Iniciar el Contenedor

#### Con `make` (Linux / macOS / WSL2 con make instalado):
```bash
make build
make up
```

#### O con `docker compose` directamente:
```bash
docker compose up -d --build
```

---

### Paso 4: Verificar que todo esté instalado correctamente
Ejecuta la comprobación automática:
```bash
make verify
# o:
docker compose exec vibe-coder ./verify.sh
```
Deberías ver las **13 herramientas** con un check verde ✅:
* Git, Node.js v22, NPM, PNPM, Bun
* GitHub CLI (`gh`), Railway CLI
* Claude Code (`claude`), OpenAI Codex (`codex`)
* Lazygit, Eza, Bat, FZF

---

### Paso 5: Entrar a Desarrollar en la Terminal

```bash
make shell
# o:
docker compose exec vibe-coder /usr/local/bin/vibe-shell
```

Al entrar, verás el banner **Vibe Coder Next** y se iniciará tu sesión de **Tmux** con **Oh My Zsh**.

---

### Paso 6: (Opcional) Instalar el comando global `vibe`
Si quieres poder escribir `vibe` en **cualquier carpeta** de tu computadora sin tener que volver a esta ruta:

```bash
make install-cli
```
A partir de ese momento, puedes hacer `cd ~/otra-carpeta` y ejecutar `vibe` para abrir el contenedor montado en esa carpeta.

---

## 💻 Alternativa Recomendada: Abrir con VS Code (1 Clic)

Si utilizas **Visual Studio Code**:
1. Instala la extensión oficial **Dev Containers** (`ms-vscode-remote.remote-containers`).
2. Abre la carpeta del proyecto en VS Code:
   ```bash
   code .
   ```
3. VS Code detectará la configuración y mostrará una notificación en la esquina inferior derecha:  
   👉 **"Reopen in Container"** (Reabrir en contenedor).
4. Haz clic en el botón. VS Code montará el entorno automáticamente y abrirá la terminal integrada lista con Zsh, Tmux y todas las herramientas.

---

## 🔑 Autenticación de Cuentas (Solo se hace la primera vez)

Dentro del shell del contenedor (`make shell`):

1. **GitHub CLI:**
   ```bash
   gh auth login
   ```
   *(Sigue las instrucciones en pantalla para vincular tu cuenta de GitHub).*

2. **Railway CLI:**
   ```bash
   rw login --browserless
   # o: railway login --browserless
   ```
   *(Copia el enlace y código que te muestre en la terminal y ábrelo en el navegador de tu computadora).*

3. **Claude Code & OpenAI Codex:**
   ```bash
   c     # Inicia Claude Code
   cx    # Inicia OpenAI Codex
   ```

> [!NOTE]
> Las sesiones se guardan automáticamente en la carpeta de usuario de tu máquina anfitriona (`~`). No tendrás que volver a iniciar sesión aunque apagues o reconstruyas el contenedor.

---

## ⚡ Comandos y Atajos Principales del Entorno

| Comando / Atajo | ¿Qué hace? |
| :--- | :--- |
| `help` | Muestra la **guía interactiva completa de atajos** |
| `verify` | Comprueba el **estado de las 13 herramientas** |
| `c` | Inicia **Claude Code CLI** |
| `cx` | Inicia **OpenAI Codex CLI** |
| `rw` | Inicia **Railway CLI** |
| `lg` | Abre **Lazygit** (interfaz interactiva para Git) |
| `pn` | Ejecuta **PNPM** |
| `b` | Ejecuta **Bun** (`b run archivo.ts`) |
| `tree` | Muestra el árbol de directorios con iconos (`eza`) |
| `cat <archivo>` | Muestra el código con colores y formato (`bat`) |
| `Ctrl + T` | Buscador interactivo de archivos en el proyecto (**FZF**) |
| `Ctrl + R` | Buscador interactivo en el historial de comandos (**FZF**) |
| `Ctrl + a` seguido de `-` | Dividir panel de Tmux horizontalmente |
| `Ctrl + a` seguido de `\|` | Dividir panel de Tmux verticalmente |
| `Ctrl + a` seguido de `d` | Desconectarse de Tmux sin cerrar tus procesos |
| **Clic con el mouse** | Seleccionar panel o cambiar de pestaña |
| **Arrastrar con el mouse** | Redimensionar tamaño de los paneles |
| **Rueda / Trackpad** | Scroll y desplazamiento en el historial |

---

## 🛠️ Comandos de Mantenimiento

| Acción | Comando |
| :--- | :--- |
| **Iniciar entorno** | `make up` |
| **Entrar a la terminal** | `make shell` |
| **Verificar herramientas** | `make verify` |
| **Detener entorno** | `make down` |
| **Ver logs del contenedor** | `make logs` |
| **Reconstruir imagen tras cambios** | `make build` |

---

## ❓ Preguntas Frecuentes y Solución de Problemas

### Error: `Cannot connect to the Docker daemon`
* **Solución:** Asegúrate de que Docker Desktop o el servicio de Docker esté abierto y ejecutándose en tu máquina.

### En Windows: `\r: command not found` o error de intérprete de bash
* **Causa:** Git convirtió los saltos de línea a formato Windows (CRLF).
* **Solución:** Este repositorio incluye un archivo `.gitattributes` para prevenirlo. Si ocurre, ejecuta dentro de WSL: `dos2unix verify.sh docker-entrypoint.sh welcome.sh vibe-shell`.

### ¿Dónde se guardan mis archivos de código?
* Todos los archivos que crees dentro de `/workspace` se reflejan instantáneamente en la carpeta local de tu computadora.
