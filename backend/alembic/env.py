"""
Alembic migration environment for CUBER project
----------------------------------------------

运行 `alembic revision --autogenerate -m "<msg>"` 时会执行本文件，
把 ORM 元数据与数据库结构做差分，生成迁移脚本。
"""

from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from typing import Any, Dict

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# ------------------------------------------------------------------
# 1. 读取 .env，以便拿到 DATABASE_URL / SECRET_KEY 等
# ------------------------------------------------------------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# ------------------------------------------------------------------
# 2. 把 backend/ 加入 sys.path，确保能 import app.*
# ------------------------------------------------------------------
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# ------------------------------------------------------------------
# 3. 导入 ORM Base 与所有模型
#    （建议在 app/models/__init__.py 里逐个 from .user import User）
# ------------------------------------------------------------------
from app.db.base import Base  # noqa: E402
from app import models        # noqa: F401  # side-effect: register models

target_metadata = Base.metadata  # Alembic 用来“对比”的表清单

# ------------------------------------------------------------------
# 4. Alembic Config 对象
# ------------------------------------------------------------------
config = context.config

# 动态写入数据库 URL（优先 .env）
config.set_main_option("sqlalchemy.url", os.environ["DATABASE_URL"])

# 5. 配置日志（保持默认）
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------
# 6. 迁移运行函数
# ------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Offline 模式：不创建 Engine，直接输出 SQL。"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # ★ 比较列类型
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Online 模式：创建 Engine，与数据库建立连接后执行 SQL。"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),  # type: ignore[arg-type]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,      # ★ 比较列类型
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------------
# 7. 入口
# ------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
