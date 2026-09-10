# Minha pequena internet

Trabalho semestral de Redes e Sistemas Distribuídos.

## Entrega 1 — Dois segmentos e um serviço

### Plano de endereçamento

A topologia utiliza duas sub-redes IPv4 independentes, ambas com prefixo `/24`:

- Segmento A: `10.0.10.0/24`
- Segmento B: `10.0.20.0/24`

Uma rede `/24` possui 24 bits para identificar a rede e 8 bits para endereços dentro da sub-rede. Assim, existem `2^8 = 256` endereços totais. Como o primeiro endereço identifica a rede e o último é reservado para broadcast, cada sub-rede possui `256 - 2 = 254` endereços utilizáveis por hosts.

#### Segmento A — `10.0.10.0/24`

| Máquina | Endereço IPv4 |
|---|---|
| host-a1 | `10.0.10.10` |
| host-a2 | `10.0.10.11` |
| srv-a | `10.0.10.20` |

- Endereço da rede: `10.0.10.0`
- Broadcast: `10.0.10.255`
- Faixa utilizável: `10.0.10.1` até `10.0.10.254`
- Total de hosts possíveis: 254

#### Segmento B — `10.0.20.0/24`

| Máquina | Endereço IPv4 |
|---|---|
| host-b1 | `10.0.20.10` |
| host-b2 | `10.0.20.11` |

- Endereço da rede: `10.0.20.0`
- Broadcast: `10.0.20.255`
- Faixa utilizável: `10.0.20.1` até `10.0.20.254`
- Total de hosts possíveis: 254

### Por que o segmento A não alcança o segmento B?

Os segmentos A e B pertencem a sub-redes diferentes. Na Entrega 1 não existe um roteador configurado para encaminhar pacotes entre essas duas redes.

Além disso, os hosts têm a rota padrão removida ao iniciar. Dessa forma, cada máquina conhece apenas a sua própria sub-rede diretamente conectada. A comunicação entre máquinas do mesmo segmento funciona normalmente, mas, quando uma máquina tenta enviar um pacote para a outra sub-rede, não existe rota disponível para esse destino e o sistema retorna `Network is unreachable`.

Isso prova que os dois segmentos estão funcionando individualmente e, ao mesmo tempo, permanecem isolados entre si.

### Testes da Entrega 1

Na Google Cloud Shell, a verificação pode ser executada com:

```bash
make up E=1
make verificar E=1
```

Depois que todas as provas estiverem verdes, as evidências são geradas com:

```bash
make evidencias E=1
```
