#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if ! command -v manimgx >/dev/null 2>&1; then
    uv tool install --python 3.14 manimgx
    export PATH="$HOME/.local/bin:$PATH"
fi
manimgx --version
manimgx inspect solar_system.py -t 4,10,20,29,end
manimgx render solar_system.py -r 1920x1080 --fps 30
xdg-open "$PWD/SolarSystem.mp4"
