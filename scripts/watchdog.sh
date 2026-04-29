#!/bin/bash
# Watchdog pro download_transcripts.py
# Každých 5 minut zkontroluje jestli skript běží — pokud ne, restartuje ho.
# Použití: bash watchdog.sh &

SCRIPTS_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPTS_DIR/.." && pwd)"
LOG="$ROOT_DIR/watchdog.log"
DOWNLOAD_LOG="$ROOT_DIR/download.log"
PYTHON="/usr/bin/python3"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" | tee -a "$LOG"
}

log "Watchdog spuštěn (ROOT: $ROOT_DIR)"

while true; do
    if ! pgrep -f "download_transcripts.py" > /dev/null 2>&1; then
        log "Skript neběží — restartuji"
        cd "$ROOT_DIR" && $PYTHON "$SCRIPTS_DIR/download_transcripts.py" >> "$DOWNLOAD_LOG" 2>&1 &
        log "Spuštěno (PID: $!)"
    fi
    sleep 300
done
