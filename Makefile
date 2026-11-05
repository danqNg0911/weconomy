.PHONY: install test lint schema collect dataset-status export-dataset

# Optional convenience targets; direct `uv` commands work on Windows without make.
install:
	uv sync --locked --extra dev --extra nlp
	uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
	uv run python -c "import stanza; stanza.download('vi', processors='tokenize,pos,depparse')"

# test_core.py is the legacy pilot suite and requires its separate pilot dependencies.
test:
	uv run --no-sync pytest -q tests --ignore tests/test_core.py

lint:
	uv run --no-sync ruff check src/weconomy tests --exclude test_core.py

schema:
	uv run --no-sync weconomy schema

DATASET ?= data/datasets/international-business
OUTPUT ?= data/exports/international-business
SOURCES ?=
FROM_RUNS ?=
ARTICLES ?=
NODES ?=
RELATIONS ?=
RELATION_TYPES ?=
MAX_CANDIDATES ?= 1000
BATCH_SIZE ?= 20
NER ?= models
RESUME ?= 0

COLLECT_ARGS = $(foreach source,$(SOURCES),--source $(source)) \
	$(foreach run,$(FROM_RUNS),--from-run "$(run)") \
	$(if $(filter-out 0,$(ARTICLES)),--articles $(ARTICLES)) \
	$(if $(filter-out 0,$(NODES)),--nodes $(NODES)) \
	$(if $(filter-out 0,$(RELATIONS)),--relations $(RELATIONS)) \
	$(if $(filter-out 0,$(RELATION_TYPES)),--relation-types $(RELATION_TYPES))

collect:
	uv run --no-sync weconomy collect-dataset --dataset "$(DATASET)" --max-candidates $(MAX_CANDIDATES) --batch-size $(BATCH_SIZE) --ner $(NER) $(COLLECT_ARGS) $(if $(filter-out 0,$(RESUME)),--resume)

dataset-status:
	uv run --no-sync weconomy dataset-status "$(DATASET)"

export-dataset:
	uv run --no-sync weconomy export-dataset "$(DATASET)" --output "$(OUTPUT)"
