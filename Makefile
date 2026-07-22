.PHONY: setup index start

# PYRITE_DATA_DIR 指向项目根目录，setup.py 会用这个路径写配置
setup:
	python scripts/setup.py

index:
	python -c "from pyrite.config import load_config; from pyrite.storage.database import PyriteDB; from pyrite.storage.index import IndexManager; c=load_config(); d=PyriteDB(c.settings.index_path); i=IndexManager(d); [i.index_kb(kb.name) for kb in c.knowledge_bases]; d.close()"

start:
	python -m pyrite.server.mcp_server --tier admin
