.PHONY: install test lint schema collect dataset-status export-dataset

# Optional convenience targets; direct `uv` commands work on Windows without make.
install:
	uv sync --locked --extra dev --extra nlp
	uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
	uv run python -c "import stanza; stanza.download('vi', processors='tokenize,pos,depparse')"

test:
	uv run --no-sync pytest -q tests

lint:
	uv run --no-sync ruff check src/weconomy tests

schema:
	uv run --no-sync weconomy schema

DATASET ?= data/datasets/international-business-katana
OUTPUT ?= data/exports/international-business-katana
CONFIG ?= config/collection.yaml
TARGETS ?=
ARTICLES ?=
NODES ?= 1000
RELATIONS ?= 5000
RELATION_TYPES ?= 10
MAX_CANDIDATES ?= 10000
BATCH_SIZE ?= 20
RESUME ?= 0

COLLECT_ARGS = $(foreach target,$(TARGETS),--target $(target)) \
	$(if $(filter-out 0,$(ARTICLES)),--articles $(ARTICLES)) \
	$(if $(filter-out 0,$(NODES)),--nodes $(NODES)) \
	$(if $(filter-out 0,$(RELATIONS)),--relations $(RELATIONS)) \
	$(if $(filter-out 0,$(RELATION_TYPES)),--relation-types $(RELATION_TYPES))

collect:
	uv run --no-sync weconomy collect --config "$(CONFIG)" --dataset "$(DATASET)" --max-candidates $(MAX_CANDIDATES) --batch-size $(BATCH_SIZE) $(COLLECT_ARGS) $(if $(filter-out 0,$(RESUME)),--resume)

dataset-status:
	uv run --no-sync weconomy dataset-status "$(DATASET)"

export-dataset:
	uv run --no-sync weconomy export-dataset "$(DATASET)" --output "$(OUTPUT)"
