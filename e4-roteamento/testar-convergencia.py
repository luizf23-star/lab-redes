#!/usr/bin/env python3
"""Teste de integração real: rotas, ping nos dois sentidos e restauração."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import time

HERE = Path(__file__).resolve().parent
TRANSIT = "e4_seg-t1"
SHORT = ("10.0.30.12", "10.0.30.11")
DETOUR = ("10.0.40.13", "10.0.50.13")
ENDS = (("e4-r1", "10.0.30.11"), ("e4-r2", "10.0.30.12"))


def docker(*args, check=True):
    return subprocess.run(
        ["docker", *args], text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=check, timeout=15,
    )


def route(router, destination):
    result = docker("exec", router, "ip", "route", "get", destination, check=False)
    return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()


def routes():
    return {
        "r1_para_b": route("e4-r1", "10.0.20.10"),
        "r2_para_a": route("e4-r2", "10.0.10.10"),
    }


def has_via(line, address):
    return re.search(r"\bvia\s+" + re.escape(address) + r"(?:\s|$)", line) is not None


def ping_both():
    for host, destination in (("e4-host-a", "10.0.20.10"),
                              ("e4-host-b", "10.0.10.10")):
        if docker("exec", host, "ping", "-c1", "-W2", destination,
                  check=False).returncode != 0:
            return False
    return True


def wait_for(label, expected, limit=90):
    start = time.monotonic()
    latest = {}
    while time.monotonic() - start < limit:
        latest = routes()
        if (has_via(latest["r1_para_b"], expected[0])
                and has_via(latest["r2_para_a"], expected[1]) and ping_both()):
            seconds = time.monotonic() - start
            print(f"OK {label}: {seconds:.3f}s; ping A->B e B->A", flush=True)
            for key, value in latest.items():
                print(f"   {key}: {value}", flush=True)
            return seconds, latest
        time.sleep(1)
    raise AssertionError(f"{label}: não convergiu em {limit}s; rotas: {latest}")


def reconnect():
    errors = []
    for router, address in ENDS:
        result = docker("network", "connect", "--ip", address, TRANSIT,
                        router, check=False)
        # Conectar uma ponta que já estava conectada é inofensivo. Outros
        # erros precisam aparecer, para não esconder falha da infraestrutura.
        if result.returncode and "already exists" not in result.stderr:
            errors.append(f"{router}: {result.stderr.strip()}")
    if errors:
        raise RuntimeError("Falha ao restaurar o trânsito: " + "; ".join(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aguardar", action="store_true",
                        help="aguarda somente o estado normal, sem derrubar enlaces")
    args = parser.parse_args()
    print("=== E4 — convergência complementar (Docker real) ===", flush=True)
    wait_for("caminho curto nos dois sentidos", SHORT)
    if args.aguardar:
        return

    result = {"data_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "antes": routes()}
    must_restore = False
    try:
        # A flag é marcada antes da primeira desconexão para que o finally
        # restaure inclusive uma falha durante a segunda desconexão.
        must_restore = True
        start = time.monotonic()
        for router, _ in ENDS:
            docker("network", "disconnect", TRANSIT, router)
        disconnected = time.monotonic()
        print("Trânsito 1 desconectado nas DUAS pontas.", flush=True)
        recovery, after = wait_for("desvio por r3 nos dois sentidos", DETOUR)
        result.update({"recuperacao_s": round(time.monotonic() - start, 3),
                       "apos_desconexao_s": round(recovery, 3),
                       "desconectar_s": round(disconnected - start, 3),
                       "durante_falha": after})

        start = time.monotonic()
        reconnect()
        _, restored = wait_for("retorno automático ao caminho curto", SHORT)
        result.update({"restauracao_s": round(time.monotonic() - start, 3),
                       "restaurado": restored})
        must_restore = False
    finally:
        if must_restore:
            reconnect()

    for router in ("e4-r1", "e4-r2", "e4-r3"):
        status = docker("exec", router, "birdc", "show", "status").stdout
        print(f"--- {router} ---\n{status.strip()}", flush=True)
    target = HERE / "evidencias" / "convergencia.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print("CONVERGÊNCIA COMPLEMENTAR COMPLETA", flush=True)


if __name__ == "__main__":
    main()
