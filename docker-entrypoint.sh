#!/usr/bin/env bash
set -e

# ── 1. DB가 올라올 때까지 대기 ─────────────────────────────
echo "⏳ Waiting for postgres at $SQLALCHEMY_DATABASE_URI"
while ! python - <<EOF 2>/dev/null
import sys, time, sqlalchemy as sa, os, urllib.parse
uri = os.environ['SQLALCHEMY_DATABASE_URI']
try:
    sa.create_engine(uri).connect().close()
except Exception as e:
    print(e, file=sys.stderr)
    time.sleep(1)
    sys.exit(1)
EOF
do
  sleep 1
done
echo "✅ Postgres is ready"

# ── 2. 마이그레이션 실행 ───────────────────────────────────
echo "🚀 Running flask db upgrade"
flask db migrate || true
flask db upgrade || true

# ── 3. 최종 명령 실행 (CMD) ────────────────────────────────
echo "🎉 Starting application"
exec "$@"