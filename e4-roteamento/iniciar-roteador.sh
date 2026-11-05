#!/bin/sh
# O BIRD mantém as rotas dos três roteadores e roda em primeiro plano.
set -eu

case "${ROLE:-}" in
  r1|r2|r3) ;;
  *) echo "ROLE deve ser r1, r2 ou r3" >&2; exit 1 ;;
esac

ip route del default 2>/dev/null || true
test "$(cat /proc/sys/net/ipv4/ip_forward)" = 1 || {
  echo "O encaminhamento IPv4 deve estar habilitado pelo compose" >&2
  exit 1
}
mkdir -p /run/bird
exec bird -f -c "/lab/bird-${ROLE}.conf"
