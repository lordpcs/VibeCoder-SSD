.PHONY: help build up down restart shell verify logs clean install-cli dashboard sdd-lint sdd-verify orchestrator

help:
	@echo "Comandos disponibles para Vibe Coder:"
	@echo "  make build         - Construir la imagen Docker"
	@echo "  make up            - Iniciar el contenedor en segundo plano"
	@echo "  make down          - Detener el contenedor"
	@echo "  make restart       - Reiniciar el contenedor"
	@echo "  make shell         - Abrir terminal interactiva en el contenedor"
	@echo "  make verify        - Verificar versiones de todas las herramientas"
	@echo "  make dashboard     - Iniciar el Orquestador y Dashboard Web (puerto 4040)"
	@echo "  make sdd-lint      - Validar especificaciones, esquemas y contratos SDD"
	@echo "  make sdd-verify    - Verificar invariantes arquitectónicos del sistema"
	@echo "  make logs          - Ver registros del contenedor"
	@echo "  make clean         - Eliminar contenedor y volúmenes de datos"
	@echo "  make install-cli   - Instalar el comando global 'vibe' en tu Mac/Linux (~/.local/bin/vibe)"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

shell:
	docker compose exec vibe-coder /usr/local/bin/vibe-shell

verify:
	docker compose exec vibe-coder ./verify.sh

logs:
	docker compose logs -f vibe-coder

clean:
	docker compose down -v

dashboard:
	@echo "🌐 Abriendo Orquestador y Dashboard Web en http://localhost:4040..."
	docker compose exec -d vibe-coder /usr/local/bin/vibe-orchestrator || python orchestrator/run.py

orchestrator:
	python orchestrator/run.py

sdd-lint:
	python bin/sdd.py lint

sdd-verify:
	python bin/sdd.py invariants

install-cli:
	@mkdir -p ~/.local/bin
	@cp bin/vibe ~/.local/bin/vibe
	@cp bin/sdd ~/.local/bin/sdd
	@cp bin/sdd.py ~/.local/bin/sdd.py
	@chmod +x ~/.local/bin/vibe ~/.local/bin/sdd ~/.local/bin/sdd.py
	@echo "✅ Comandos 'vibe' y 'sdd' instalados en ~/.local/bin/"
	@echo "Ya puedes escribir 'vibe' o 'sdd' en cualquier terminal."
