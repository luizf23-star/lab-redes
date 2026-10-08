#!/bin/sh
# Contrato: nome da réplica que respondeu e código 0; ou INDISPONIVEL e 1.
# Três tentativas de até 1 s: orçamento de rede de no máximo 3 s.
for n in 1 2 3; do
  ip="10.0.20.$((20 + n))"
  if resposta=$(curl --fail --silent --show-error --noproxy '*' \
      --connect-timeout 1 --max-time 1 "http://$ip:8080/" 2>/dev/null); then
    # Só aceite o corpo recebido de uma requisição HTTP bem-sucedida.
    # O nome deve corresponder à réplica consultada, nunca ser inventado.
    if [ "$resposta" = "replica$n" ]; then
      printf '%s\n' "$resposta"
      exit 0
    fi
  fi
done

printf 'INDISPONIVEL\n'
exit 1
