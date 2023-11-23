# Define the Python command (change to python3 if required)
PYTHON := python

# Define script paths
DATASET_PARTITIONER := owain_app/dataset_partitioner.py
K_FOLD_VALIDATION := owain_app/k_fold_validation.py
OPENAI_INTERACTION := owain_app/openai_interaction.py
GENERATE_FIGURES := owain_app/generate_figures.py

# Define default target
.PHONY: all
all: partition_data k_fold_validation openai_interaction generate_figures

# Target for dataset partitioning
.PHONY: partition_data
partition_data:
	@echo "Partitioning dataset..."
	@$(PYTHON) $(DATASET_PARTITIONER) --n 4 --r 2

# Target for k-fold cross-validation
.PHONY: k_fold_validation
k_fold_validation:
	@echo "Running k-fold cross-validation..."
	@$(PYTHON) $(K_FOLD_VALIDATION)

# Target for interacting with OpenAI
.PHONY: openai_interaction
openai_interaction:
	@echo "Interacting with OpenAI API..."
	@$(PYTHON) $(OPENAI_INTERACTION) --prompt_dir path_to_prompt_files --response_dir path_to_save_responses

# Target for generating figures
.PHONY: generate_figures
generate_figures:
	@echo "Generating figures..."
	@$(PYTHON) $(GENERATE_FIGURES)

# Clean-up command (if needed)
.PHONY: clean
clean:
	@echo "Cleaning up..."
	# Add clean-up commands here (e.g., removing generated files)
