#!/usr/bin/env bash
set -euo pipefail

# Quick start script for Five-day-line
# - Starts FastAPI backend (uvicorn) with reload
# - Ensures web dependencies and starts Next.js dev server
# Options:
#   --backend-only    Start only backend
#   --frontend-only   Start only frontend
# Env:
#   BACKEND_PORT=8000
#   FRONTEND_PORT=3000

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-3000}"
PID_DIR="$ROOT_DIR/scripts/.pids"
mkdir -p "$PID_DIR"

START_BACKEND=true
START_FRONTEND=true
for arg in "$@"; do
  case "$arg" in
    --backend-only)
      START_FRONTEND=false
      ;;
    --frontend-only)
      START_BACKEND=false
      ;;
    *)
      ;;
  esac
done

have_cmd() { command -v "$1" >/dev/null 2>&1; }
port_in_use() {
  local port="$1"
  if have_cmd lsof; then
    lsof -i TCP:"$port" -sTCP:LISTEN >/dev/null 2>&1
    return $?
  fi
  # Fallback: try nc; if not available, assume free
  if have_cmd nc; then
    nc -z localhost "$port" >/dev/null 2>&1
    return $?
  fi
  return 1
}

if $START_BACKEND; then
  if ! have_cmd uv; then
    echo "ERROR: 'uv' 未安装。请先安装 uv 后再运行："
    echo "  macOS/Linux: curl -Ls https://astral.sh/uv/install.sh | sh"
    echo "  Windows(PowerShell): irm https://astral.sh/uv/install.ps1 | iex"
    exit 1
  fi
  # 自动寻找可用端口
  while port_in_use "$BACKEND_PORT"; do
    BACKEND_PORT=$(( BACKEND_PORT + 1 ))
  done
fi

pids=()
cleanup() {
  echo
  echo ">> 收到退出信号，清理子进程..."
  for pid in "${pids[@]:-}"; do
    if kill -0 "$pid" >/dev/null 2>&1; then
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
    fi
  done
}
trap cleanup INT TERM EXIT

if $START_BACKEND; then
  echo ">> 启动后端: http://localhost:${BACKEND_PORT}"
  ( PYTHONPATH=src uv run uvicorn api.main:app --host 0.0.0.0 --port "${BACKEND_PORT}" --reload ) &
  backend_pid="$!"
  echo "$backend_pid" > "$PID_DIR/backend.pid"
  pids+=("$backend_pid")
fi

if $START_FRONTEND; then
  echo ">> 检查前端依赖..."
  pushd web >/dev/null
  if [ ! -d node_modules ]; then
    echo ">> 安装前端依赖 (npm install)..."
    npm install
  fi
  # 自动寻找可用端口
  while port_in_use "$FRONTEND_PORT"; do
    FRONTEND_PORT=$(( FRONTEND_PORT + 1 ))
  done
  echo ">> 启动前端: http://localhost:${FRONTEND_PORT}"
  # Next.js 支持通过 -p 指定端口
  ( npm run dev -- -p "${FRONTEND_PORT}" ) &
  frontend_pid="$!"
  echo "$frontend_pid" > "$PID_DIR/frontend.pid"
  pids+=("$frontend_pid")
  popd >/dev/null
fi

echo ">> 服务已启动。按 Ctrl+C 退出。"
wait "${pids[@]:-}" || true
