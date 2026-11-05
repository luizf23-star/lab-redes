#!/bin/sh
# Controle experimental: reproduz as rotas estáticas do laboratório original.
# Usado somente com docker-compose.estatico.yml, nunca no make up E=4 normal.
set -eu
ip route del default 2>/dev/null || true
case "${ROLE:-}" in
  r1) ip route add 10.0.20.0/24 via 10.0.30.12 ;;
  r2) ip route add 10.0.10.0/24 via 10.0.30.11 ;;
  r3) : ;;
  *) echo "ROLE deve ser r1, r2 ou r3" >&2; exit 1 ;;
esac
exec sleep infinity
