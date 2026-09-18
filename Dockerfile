FROM node:22-bookworm

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Soporte completo UTF-8 para iconos y Nerd Fonts
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# 1. Instalar herramientas básicas del sistema y utilidades modernas
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    gnupg \
    git \
    openssh-client \
    sudo \
    zsh \
    ripgrep \
    jq \
    tmux \
    nano \
    vim \
    procps \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    fzf \
    bat \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/batcat /usr/local/bin/bat

# 2. Instalar GitHub CLI (gh) y Eza
RUN mkdir -p -m 755 /etc/apt/keyrings \
    && curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | tee /etc/apt/keyrings/githubcli-archive-keyring.gpg > /dev/null \
    && chmod go+r /etc/apt/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | gpg --dearmor -o /etc/apt/keyrings/gierens.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | tee /etc/apt/sources.list.d/gierens.list \
    && chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends gh eza \
    && rm -rf /var/lib/apt/lists/*

# 3. Instalar Lazygit
RUN LAZYGIT_VERSION=$(curl -s "https://api.github.com/repos/jesseduffield/lazygit/releases/latest" | grep -Po '"tag_name": "v\K[^"]*') \
    && ARCH=$(dpkg --print-architecture | sed 's/arm64/arm64/;s/amd64/x86_64/') \
    && curl -Lo /tmp/lazygit.tar.gz "https://github.com/jesseduffield/lazygit/releases/latest/download/lazygit_${LAZYGIT_VERSION}_Linux_${ARCH}.tar.gz" \
    && tar -xf /tmp/lazygit.tar.gz -C /usr/local/bin lazygit \
    && rm -f /tmp/lazygit.tar.gz

# 4. Instalar herramientas de IA, despliegue y gestores de paquetes rápidos (pnpm, bun)
RUN npm install -g \
    @railway/cli \
    @anthropic-ai/claude-code \
    @openai/codex \
    pnpm \
    bun \
    && npm cache clean --force

# 4b. Instalar dependencias del Orquestador Agéntico y SDD Framework
RUN pip3 install --no-cache-dir --break-system-packages \
    fastapi \
    "uvicorn[standard]" \
    pydantic \
    pyyaml \
    jsonschema \
    psutil \
    websockets \
    aiofiles

# 5. Configurar usuario no-root 'node' y cambiar shell por defecto a zsh
RUN echo "node ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && chsh -s /bin/zsh node \
    && mkdir -p /workspace /home/node/.config /home/node/.claude /home/node/.codex /home/node/.railway \
    && chown -R node:node /workspace /home/node

# 6. Instalar Oh My Zsh y plugins como usuario node
USER node
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended \
    && git clone https://github.com/zsh-users/zsh-autosuggestions /home/node/.oh-my-zsh/custom/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting /home/node/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting \
    && git clone https://github.com/zsh-users/zsh-completions /home/node/.oh-my-zsh/custom/plugins/zsh-completions \
    && git clone https://github.com/zsh-users/zsh-history-substring-search /home/node/.oh-my-zsh/custom/plugins/zsh-history-substring-search

USER root

# 7. Copiar scripts y configuraciones completas de tmux y zsh
COPY .zshrc.template /usr/local/etc/zshrc.template
COPY .tmux.conf /usr/local/etc/tmux.conf
COPY .tmux.conf.local /usr/local/etc/tmux.conf.local
COPY welcome.sh /usr/local/bin/vibe-welcome
COPY vibe-shell /usr/local/bin/vibe-shell
COPY help.sh /usr/local/bin/vibe-help
COPY verify.sh /usr/local/bin/vibe-verify
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

COPY bin/sdd.py /usr/local/bin/sdd.py
COPY bin/sdd /usr/local/bin/sdd
COPY scripts/start-orchestrator.sh /usr/local/bin/vibe-orchestrator

RUN chmod +x /usr/local/bin/vibe-welcome /usr/local/bin/vibe-shell /usr/local/bin/vibe-help /usr/local/bin/vibe-verify /usr/local/bin/docker-entrypoint.sh /usr/local/bin/sdd /usr/local/bin/sdd.py /usr/local/bin/vibe-orchestrator \
    && ln -s /usr/local/bin/vibe-verify /usr/local/bin/verify \
    && ln -s /usr/local/bin/vibe-welcome /usr/local/bin/welcome \
    && ln -s /usr/local/bin/vibe-help /usr/local/bin/help \
    && ln -s /usr/local/bin/vibe-help /usr/local/bin/ayuda \
    && ln -s /usr/local/bin/vibe-orchestrator /usr/local/bin/orchestrator \
    && ln -s /usr/local/bin/vibe-orchestrator /usr/local/bin/dashboard \
    && cp /usr/local/etc/zshrc.template /home/node/.zshrc \
    && cp /usr/local/etc/tmux.conf /home/node/.tmux.conf \
    && cp /usr/local/etc/tmux.conf.local /home/node/.tmux.conf.local \
    && chown node:node /home/node/.zshrc /home/node/.tmux.conf /home/node/.tmux.conf.local

# 8. Exponer puertos y configurar usuario
EXPOSE 4040 3000 5173 8000 8080
WORKDIR /workspace
USER node

# Configurar shell por defecto y variables de terminal
ENV SHELL=/bin/zsh
ENV TERM=screen-256color

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["sleep", "infinity"]
