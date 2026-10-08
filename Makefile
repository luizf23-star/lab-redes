# Laboratório de Redes e Sistemas Distribuídos
# Uso:  make base      → constrói a imagem (uma vez por sessão do Cloud Shell)
#       make up E=1    → sobe a topologia da entrega 1
#       make verificar E=1
#       make down E=1
#       make evidencias E=1

E ?= 1
DIR := $(firstword $(wildcard e$(E)-*))

COMPOSE := $(shell docker compose version >/dev/null 2>&1 && echo "docker compose" || echo "docker-compose")

.PHONY: base prep up down verificar evidencias limpar ajuda

ajuda:
	@echo "make base            constrói a imagem redes-lab-base:1"
	@echo "make up E=<1..5>     sobe a topologia da entrega"
	@echo "make verificar E=<n> roda as provas da entrega"
	@echo "make evidencias E=<n> gera evidencias/ para anexar na entrega"
	@echo "make down E=<n>      derruba a topologia"

base:
	docker build -t redes-lab-base:1 base/

prep:
	@if [ -f /proc/sys/net/bridge/bridge-nf-call-iptables ] && \
	    [ "$$(cat /proc/sys/net/bridge/bridge-nf-call-iptables)" = "1" ]; then \
	  sudo sysctl -w net.bridge.bridge-nf-call-iptables=0 >/dev/null 2>&1 \
	    && echo "filtro de bridge desligado" \
	    || echo "AVISO: nao consegui desligar net.bridge.bridge-nf-call-iptables"; \
	fi

up: prep base
	@test -n "$(DIR)" || (echo "Entrega E=$(E) não existe"; exit 1)
	@# As entregas usam as mesmas sub-redes; remova as outras topologias.
	@for d in e1-* e2-* e3-* e4-* e5-*; do \
	  if [ -d "$$d" ] && [ "$$d" != "$(DIR)" ]; then \
	    (cd "$$d" && $(COMPOSE) down -v --remove-orphans >/dev/null 2>&1) || true; \
	  fi; \
	done
	cd $(DIR) && $(COMPOSE) up -d
	@echo "Topologia da entrega $(E) no ar, a partir de $(CURDIR)/$(DIR)"
	@echo "Rode: make verificar E=$(E)"

down:
	cd $(DIR) && $(COMPOSE) down -v --remove-orphans

verificar:
	@cd $(DIR) && sh verificar.sh

evidencias:
	@cd $(DIR) && mkdir -p evidencias && \
	  sh verificar.sh > evidencias/verificacao.txt 2>&1; \
	  resultado=$$?; cat evidencias/verificacao.txt; exit $$resultado
	@echo "Gravado em $(DIR)/evidencias/ — commite e anexe na entrega."

limpar:
	-@cd $(DIR) && $(COMPOSE) down -v --remove-orphans 2>/dev/null || true
	-@docker network prune -f
