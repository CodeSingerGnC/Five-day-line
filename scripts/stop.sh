#!/usr/bin/env bash
set -euo pipefail

# Stop script for Five-day-line
# - Gracefully stops FastAPI (uvicorn) and Next.js dev server
# - Uses PID files created by scripts/dev.sh when available
# - Fallbacks to process pattern and port-based detection scoped to project
# Options:
#   --force      Skip grace period and force kill immediately
# Env:
#   BACKEND_PORT_RANGE="8000-8010"
#   FRONTEND_PORT_RANGE="3000-3010"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_DIR="$ROOT_DIR/scripts/.pids"
FORCE=false
for arg in "${@:-}"; do
  case "$arg" in
    --force) FORCE=true ;;
  esac
done

have_cmd() { command -v "$1" >/dev/null 2>&1; }

kill_pid() {
  local pid="$1"
  local name="$2"
  local timeout=5
  if ! kill -0 "$pid" >/dev/null 2>&1; then
    return 0
  fi
  if "$FORCE"; then
    echo ">> Force killing $name (pid=$pid)"
    kill -KILL "$pid" 2>/dev/null || true
    return 0
  fi
  echo ">> Stopping $name (pid=$pid) ..."
  kill -TERM "$pid" 2>/dev/null || true
  for _ in $(seq 1 "$timeout"); do
    sleep 1
    kill -0 "$pid" >/dev/null 2>&1 || return 0
  done
  echo ">> $name not stopped in ${timeout}s, sending SIGKILL"
  kill -KILL "$pid" 2>/dev/null || true
}

stop_by_pidfile() {
  local file="$1"
  local name="$2"
  if [ -f "$file" ]; then
    local pid
    pid="$(cat "$file" || echo "")"
    if [ -n "${pid:-}" ]; then
      kill_pid "$pid" "$name" || true
    fi
    rm -f "$file" || true
  fi
}

stop_by_pattern() {
  local pattern="$1"
  local name="$2"
  if have_cmd pgrep; then
    local pids
    pids="$(pgrep -f "$pattern" || true)"
    if [ -n "$pids" ]; then
      for pid in $pids; do
        # Scope to this project root if possible
        if have_cmd lsof && lsof -p "$pid" 2>/dev/null | grep -q "$ROOT_DIR"; then
          kill_pid "$pid" "$name"
        elif ps -o command= -p "$pid" | grep -q "$ROOT_DIR"; then
          kill_pid "$pid" "$name"
        fi
      done
    fi
  fi
}

stop_by_ports() {
  local range="$1"
  local name="$2"
  local start="${range%-*}"
  local end="${range#*-}"
  if ! have_cmd lsof; then
    return 0
  fi
  for port in $(seq "$start" "$end"); do
    local pids
    pids="$(lsof -ti tcp:"$port" -sTCP:LISTEN 2>/dev/null || true)"
    if [ -n "$pids" ]; then
      for pid in $pids; do
        if lsof -p "$pid" 2>/dev/null | grep -q "$ROOT_DIR"; then
          kill_pid "$pid" "$name(port:$port)"
        fi
      done
    fi
  done
}

echo ">> 停止服务并回收资源 ..."

# 1) 优先使用 PID 文件
stop_by_pidfile "$PID_DIR/backend.pid"  "backend(uvicorn)"
stop_by_pidfile "$PID_DIR/frontend.pid" "frontend(next)"

# 2) 模式匹配作为兜底（限定在项目目录内）
stop_by_pattern "uv run uvicorn api.main:app" "backend(uvicorn)"
stop_by_pattern "uvicorn api.main:app"        "backend(uvicorn)"
stop_by_pattern "next dev"                    "frontend(next)"

# 3) 端口兜底
BACKEND_PORT_RANGE="${BACKEND_PORT_RANGE:-8000-8010}"
FRONTEND_PORT_RANGE="${FRONTEND_PORT_RANGE:-3000-3010}"
stop_by_ports "$BACKEND_PORT_RANGE"  "backend(uvicorn)"
stop_by_ports "$FRONTEND_PORT_RANGE" "frontend(next)"

echo ">> 退出完成。"

