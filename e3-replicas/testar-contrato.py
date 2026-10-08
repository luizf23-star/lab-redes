#!/usr/bin/env python3
"""Testes complementares com as réplicas Docker reais, sem simular respostas."""
import subprocess
import time


def docker(*args, check=True):
    return subprocess.run(
        ["docker", *args], check=check, capture_output=True, text=True,
        timeout=30,
    )


def restaurar():
    for n in (1, 2, 3):
        docker("start", f"e3-replica{n}")
    docker("network", "connect", "--ip", "10.0.20.21", "e3_seg-b",
           "e3-replica1", check=False)
    docker("network", "connect", "--ip", "10.0.20.23", "e3_seg-b",
           "e3-replica3", check=False)
    # A reconexão de uma interface pode remover sua rota estática.
    for n in (1, 2, 3):
        docker("exec", f"e3-replica{n}", "ip", "route", "replace",
               "10.0.10.0/24", "via", "10.0.20.254")
    time.sleep(2)


def parar(*numeros):
    docker("stop", "--time", "1", *(f"e3-replica{n}" for n in numeros))


def medir(cenario, respostas, codigo):
    inicio = time.monotonic()
    resultado = subprocess.run(
        ["docker", "exec", "e3-cliente", "sh", "/lab/cliente.sh"],
        capture_output=True, text=True, timeout=5,
    )
    duracao = time.monotonic() - inicio
    assert resultado.returncode == codigo, (
        cenario, "código inesperado", resultado.returncode, resultado.stderr
    )
    assert resultado.stdout in {r + "\n" for r in respostas}, (
        cenario, "resposta inesperada", resultado.stdout
    )
    assert duracao < 5, (cenario, "demorou 5 s ou mais", duracao)
    assert not resultado.stderr, (cenario, "saída extra", resultado.stderr)
    print(f"OK {cenario}: {resultado.stdout.strip()}, "
          f"código={resultado.returncode}, tempo={duracao:.3f}s", flush=True)


def main():
    print("=== ENTREGA 3 — contrato complementar (Docker real) ===", flush=True)
    try:
        restaurar()
        medir("três réplicas", {"replica1", "replica2", "replica3"}, 0)
        parar(1)
        medir("réplica1 parada", {"replica2", "replica3"}, 0)
        parar(2)
        medir("somente réplica3", {"replica3"}, 0)
        docker("network", "disconnect", "e3_seg-b", "e3-replica3")
        assert docker("inspect", "-f", "{{.State.Running}}",
                      "e3-replica3").stdout.strip() == "true"
        medir("última réplica viva e particionada", {"INDISPONIVEL"}, 1)
        restaurar()
        medir("restaurado", {"replica1", "replica2", "replica3"}, 0)
        parar(2, 3)
        medir("somente réplica1", {"replica1"}, 0)
        parar(1)
        docker("start", "e3-replica2")
        time.sleep(1)
        medir("somente réplica2", {"replica2"}, 0)
        parar(2)
        medir("todas as réplicas paradas", {"INDISPONIVEL"}, 1)
        restaurar()
        docker("network", "disconnect", "e3_seg-b", "e3-replica1")
        assert docker("inspect", "-f", "{{.State.Running}}",
                      "e3-replica1").stdout.strip() == "true"
        medir("réplica1 particionada com alternativas", {"replica2", "replica3"}, 0)
    finally:
        restaurar()
    medir("restauração final", {"replica1", "replica2", "replica3"}, 0)
    print("CONTRATO COMPLETO", flush=True)


if __name__ == "__main__":
    main()
