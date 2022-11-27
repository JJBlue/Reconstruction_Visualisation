#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "$(dirname "$SCRIPT_DIR")"
python3.11 "${SCRIPT_DIR}/src/main/python/main.py" -workdir "${SCRIPT_DIR}/config"
