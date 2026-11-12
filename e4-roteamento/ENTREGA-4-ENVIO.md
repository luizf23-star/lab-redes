# Entrega 4 - A rota se refaz sozinha

**Submissao separada no site do professor:** selecione a opcao referente a Entrega 4 / roteamento RIP. Nao confundir com Entrega 5 - Captura e Cartilha.

## Identificacao
Repositorio: https://github.com/luizf23-star/lab-redes
Pasta: https://github.com/luizf23-star/lab-redes/tree/main/e4-roteamento

## Comprovacoes reais (5/11/2026)
- Verificacao oficial: `evidencias/verificacao.txt` - todos os criterios OK; mensagem `ENTREGA 4 COMPLETA`.
- Recuperacao apos queda das duas pontas do transito 1: **29 segundos** no verificador oficial.
- Teste complementar: **25,765 s** ate recuperacao pelo desvio e **0,283 s** na restauracao, medidos em execucoes proprias.
- Prova do caminho alternativo: r1 -> r3 (`10.0.40.13`), em vez de r1 -> r2 (`10.0.30.12`).
- Configuracoes BIRD: `bird-r1.conf`, `bird-r2.conf` e `bird-r3.conf`; o r2 tem ID proprio.
- Discussao sobre 50 roteadores e limitacao do RIP: `README.md` do repositorio, secao Entrega 4.

## Arquivos de evidencia
- [Saida do verificador](evidencias/verificacao.txt)
- [Teste complementar](evidencias/complementar.txt)
- [Tempos JSON](evidencias/convergencia.json)
- [Ambiente, roteadores e tabelas de roteamento](evidencias/ambiente.txt)
- [Controle com rotas estaticas](evidencias/controle-estatico.txt)

**Execucao auditavel:** https://github.com/luizf23-star/lab-redes/actions/runs/42124323897

**Observacao:** este arquivo documenta uma verificacao historica real. A submissao no site do professor continua sendo uma acao separada.
