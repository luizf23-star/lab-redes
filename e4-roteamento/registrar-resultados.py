#!/usr/bin/env python3
"""Registra no README somente as medições produzidas pelos testes reais."""
import hashlib
import json
import os
from pathlib import Path
import re

here = Path(__file__).resolve().parent
evidence = here / "evidencias"
result = json.loads((evidence / "convergencia.json").read_text())
official = (evidence / "verificacao.txt").read_text()
assert "ENTREGA 4 COMPLETA" in official, "Verificação oficial incompleta"
match = re.search(r"levou (\d+)s", official)
assert match, "Tempo oficial ausente"
result["oficial_recuperacao_s"] = int(match.group(1))
result["commit_testado"] = os.environ["GITHUB_SHA"]
result["execucao"] = (f"https://github.com/{os.environ['GITHUB_REPOSITORY']}"
                     f"/actions/runs/{os.environ['GITHUB_RUN_ID']}")
result["verificador_sha256"] = hashlib.sha256((here / "verificar.sh").read_bytes()).hexdigest()
(evidence / "convergencia.json").write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + "\n")

block = f"""<!-- E4-RESULTADOS-INICIO -->
Medição em Docker real, em {result['data_utc']}:

| Verificação | Resultado medido |
|---|---|
| Roteiro oficial: recuperação após queda das duas pontas de t1 | {result['oficial_recuperacao_s']} s |
| Teste complementar: desvio confirmado e ping nos dois sentidos | {result['recuperacao_s']:.3f} s |
| Teste complementar: volta ao caminho curto nos dois sentidos | {result['restauracao_s']:.3f} s |

Os resultados são de execuções distintas: o roteiro oficial mede em segundos
inteiros; o complementar usa relógio monotônico, consulta aproximadamente a cada
segundo e inclui as operações Docker. Os valores não são uma garantia de tempo
para outra máquina ou para outra fase dos temporizadores do RIP.

Commit testado: `{result['commit_testado']}`.
[Execução e logs]({result['execucao']}).
<!-- E4-RESULTADOS-FIM -->"""
readme = here.parent / "README.md"
text = readme.read_text()
text, replacements = re.subn(
    r"<!-- E4-RESULTADOS-INICIO -->.*?<!-- E4-RESULTADOS-FIM -->",
    lambda _: block, text, flags=re.S)
assert replacements == 1, "Bloco de resultados do README ausente ou duplicado"
readme.write_text(text)
