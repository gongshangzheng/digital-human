#!/bin/bash
# 启动 Digital Human 数字人研发管理平台全部服务
# 端口分配：后端=8812  前端=3212

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Node 版本：切到 nvm 的 v22，避免 conda 自带 node 20.17 触发 Vite 引擎告警 ---
# 注：nvm use 在 conda/cmux 环境下 prepend 不生效，故手动把 nvm v22 bin 插到 PATH 最前
NVM_NODE_BIN="$(printf '%s\n' "$HOME"/.nvm/versions/node/v22.*/bin | sort -V | tail -1)"
if [ -n "$NVM_NODE_BIN" ] && [ -x "$NVM_NODE_BIN/node" ]; then
  export PATH="$NVM_NODE_BIN:$PATH"
  hash -r 2>/dev/null
fi

# 检查端口是否被占用，如果是则报告冲突并退出
check_port_conflict() {
  local port=$1
  local service_name=$2

  if lsof -i :$port -sTCP:LISTEN >/dev/null 2>&1; then
    local pid=$(lsof -ti :$port -sTCP:LISTEN | head -1)
    local proc_info=$(ps -p $pid -o args= 2>/dev/null || echo "unknown")
    echo "ERROR: $service_name ($port) already occupied by PID $pid"
    echo "  Process: $proc_info"
    echo "  Stop it first: kill $pid"
    return 1
  fi
  return 0
}

# --- 检查端口冲突 ---
if ! check_port_conflict 8812 "Backend" || ! check_port_conflict 3212 "Frontend"; then
  echo ""
  echo "Port conflict detected. Stop the conflicting processes and retry."
  exit 1
fi

# --- 1. Backend (port 8812) ---
echo "Starting Backend (8812)..."
cd "$BASE_DIR"
nohup python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8812 </dev/null > /tmp/digital-human-backend.log 2>&1 & disown
sleep 2

# --- 2. Frontend (port 3212) ---
echo "Starting Frontend (3212)..."
cd "$BASE_DIR/web"
nohup npx vite --port 3212 --strict-port </dev/null > /tmp/digital-human-frontend.log 2>&1 & disown
sleep 3

# --- 验证 ---
echo ""
echo "=== Service Status ==="
echo "Backend   (8812): $(curl -s --max-time 3 http://localhost:8812/api/health | head -c 60)"
echo "Frontend  (3212): $(curl -s --max-time 3 http://localhost:3212 | head -c 40)"
