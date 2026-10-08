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

## Entrega 3 — O serviço não pode cair

O diretório `e3-replicas/` usa a topologia e o verificador oficiais do
laboratório do professor. Um cliente no segmento A (`10.0.10.10`) acessa três
réplicas HTTP no segmento B através do roteador, com endereços
`10.0.10.254` e `10.0.20.254`.

| Réplica | Endereço | Resposta HTTP |
|---|---|---|
| replica1 | `10.0.20.21:8080` | `replica1` |
| replica2 | `10.0.20.22:8080` | `replica2` |
| replica3 | `10.0.20.23:8080` | `replica3` |

### Como o cliente mantém o serviço disponível

O `cliente.sh` tenta cada réplica em sequência. Cada tentativa tem limite
total de 1 segundo, incluindo a conexão e o recebimento da resposta. Se uma
tentativa falhar, o cliente passa à próxima, sem repetir indefinidamente.
As três tentativas têm um orçamento de rede de até 3 segundos, deixando
margem para terminar antes dos 5 segundos do contrato.

O cliente só imprime o nome que recebeu quando o `curl` termina com sucesso
e o corpo corresponde à réplica consultada. Erros HTTP, respostas vazias,
nomes incorretos e transferências incompletas não contam como sucesso.
Quando encontra uma resposta válida, termina com código 0. Quando nenhuma
réplica responde, imprime apenas `INDISPONIVEL` e termina com código 1.
Uma nova execução tenta as três novamente, permitindo recuperação sem
alterar o cliente.

### Réplica morta × partição de rede

O cliente não consegue distinguir com certeza uma réplica morta de uma
réplica particionada apenas pela ausência de resposta. Em `docker stop`, o
processo da réplica é encerrado. Em `docker network disconnect`, o processo
continua em execução, mas perdeu a comunicação com o cliente. Nos dois
casos, a requisição pode falhar ou atingir o limite de tempo.

Para este serviço de consulta, essa incerteza não impede o funcionamento:
o cliente precisa saber qual réplica respondeu, tenta as demais e avisa
quando nenhuma está alcançável. `INDISPONIVEL` significa indisponível para
este cliente, e não que todas as réplicas necessariamente morreram. Em um
serviço com escritas, a distinção exigiria mais cuidado, pois uma operação
poderia ter sido executada mesmo sem a resposta chegar; repeti-la poderia
duplicar seus efeitos.

### Testes e evidências

```bash
make up E=3
make verificar E=3
make evidencias E=3
python3 e3-replicas/testar-contrato.py
```

O verificador oficial cobre tudo no ar, uma réplica parada, duas paradas,
partição da última réplica e restauração. O teste complementar mede também
o código de saída e o tempo com precisão, cada réplica funcionando sozinha,
todas paradas e partição de uma réplica com outras disponíveis.

O GitHub Actions executa os testes com Docker e grava a saída oficial em
`e3-replicas/evidencias/verificacao.txt`, além das medições complementares
em `e3-replicas/evidencias/contrato.txt`. As evidências da Entrega 1 são
preservadas. Para reproduzir no Cloud Shell, use os comandos acima na
pasta deste repositório.
