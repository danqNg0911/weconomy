.PHONY: install test lint schema collect graph-cycle dataset-status export-dataset

# Optional convenience targets; direct `uv` commands work on Windows without make.
install:
	uv sync --locked --extra dev --extra nlp

test:
	uv run --no-sync pytest -q tests

lint:
	uv run --no-sync ruff check src/weconomy tests

schema:
	uv run --no-sync weconomy schema

DATASET ?= data/datasets/international-business-katana
GRAPH_DATASET ?= data/datasets/international-business-gliner-coref-v2
OUTPUT ?= data/exports/international-business-katana
CONFIG ?= config/collection.yaml
TARGETS ?=
ARTICLES ?=
NODES ?= 2000
RELATIONS ?= 5000
RELATION_TYPES ?= 11
MAX_CANDIDATES ?= 10000
BATCH_SIZE ?= 20
RESUME ?= 0
FORCE ?= 0

COLLECT_ARGS = $(foreach target,$(TARGETS),--target $(target)) \
	$(if $(filter-out 0,$(ARTICLES)),--articles $(ARTICLES)) \
	$(if $(filter-out 0,$(NODES)),--nodes $(NODES)) \
	$(if $(filter-out 0,$(RELATIONS)),--relations $(RELATIONS)) \
	$(if $(filter-out 0,$(RELATION_TYPES)),--relation-types $(RELATION_TYPES))

collect:
	uv run --no-sync weconomy collect --config "$(CONFIG)" --dataset "$(DATASET)" --max-candidates $(MAX_CANDIDATES) --batch-size $(BATCH_SIZE) $(COLLECT_ARGS) $(if $(filter-out 0,$(RESUME)),--resume) $(if $(filter-out 0,$(FORCE)),--force)

graph-cycle:
	uv run --no-sync weconomy graph-cycle --config "$(CONFIG)" --dataset "$(GRAPH_DATASET)" --nodes $(NODES) --relations $(RELATIONS) --relation-types $(RELATION_TYPES) --max-candidates $(MAX_CANDIDATES) --batch-size $(BATCH_SIZE)

dataset-status:
	uv run --no-sync weconomy dataset-status "$(DATASET)"

export-dataset:
	uv run --no-sync weconomy export-dataset "$(DATASET)" --output "$(OUTPUT)"
