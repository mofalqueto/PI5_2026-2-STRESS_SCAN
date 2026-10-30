#!/usr/bin/env bash
set -euo pipefail

target_sha="${SSH_ORIGINAL_COMMAND:-${1:-}}"

if [[ ! "$target_sha" =~ ^[0-9a-f]{40}$ ]]; then
    echo "Informe o SHA completo do commit."
    exit 2
fi

cd /home/nathan/PI5_2026-2-STRESS_SCAN

exec 9>/home/nathan/.stress-scan-deploy.lock
flock -n 9 || {
    echo "Outra publicação está em andamento."
    exit 1
}

if [[ -n "$(git status --porcelain)" ]]; then
    echo "Publicação cancelada: existem alterações locais."
    exit 1
fi

git fetch origin main

git merge-base --is-ancestor "$target_sha" origin/main || {
    echo "O commit não está integrado à main."
    exit 1
}

git checkout --detach "$target_sha"

api/.venv/bin/python -m pip install \
    --no-cache-dir -r api/requirements.txt

api/.venv/bin/python -m pip check

(
    cd api
    .venv/bin/python -c \
        'import main; assert main.modelo is not None'
)

sudo -n /usr/bin/systemctl restart stress-scan.service

for attempt in {1..30}; do
    if curl -fsS --max-time 3 http://127.0.0.1:8000/ |
        api/.venv/bin/python -c \
        'import json,sys; assert json.load(sys.stdin)["aplicacao"] == "Stress Scan"'
    then
        echo "Publicação concluída: $target_sha"
        exit 0
    fi
    sleep 2
done

echo "A API não respondeu. Consulte: journalctl -u stress-scan"
exit 1
