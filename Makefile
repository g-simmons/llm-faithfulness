# Define the Python command (change to python3 if required)
PYTHON := python

# Define script paths
DATASET_PARTITIONER := owain_app/dataset_partitioner.py
K_FOLD_VALIDATION := owain_app/k_fold_validation.py
OPENAI_INTERACTION := owain_app/openai_interaction.py
GENERATE_FIGURES := owain_app/generate_figures.py

# Define output file paths or markers
DATASET_OUTPUT := data/dataset_output_marker
K_FOLD_OUTPUT := data/k_fold_output_marker
OPENAI_OUTPUT := data/openai_output_marker

# Define default target
.PHONY: all
all: generate_figures

# Target for generating figures, depends on k_fold_validation
generate_figures: $(K_FOLD_OUTPUT)
	@echo "Generating figures..."
	@$(PYTHON) $(GENERATE_FIGURES)

# Target for k-fold cross-validation, depends on openai_interaction
k_fold_validation: $(OPENAI_OUTPUT)
	@echo "Running k-fold cross-validation..."
	@$(PYTHON) $(K_FOLD_VALIDATION)
	@touch $(K_FOLD_OUTPUT)

# Target for interacting with OpenAI, depends on partition_data
openai_interaction: $(DATASET_OUTPUT)
	@echo "Interacting with OpenAI API..."
	@$(PYTHON) $(OPENAI_INTERACTION) --prompt_dir path_to_prompt_files --response_dir path_to_save_responses
	@touch $(OPENAI_OUTPUT)

# Target for dataset partitioning
partition_data: 
	@echo "Partitioning dataset..."
	@$(PYTHON) $(DATASET_PARTITIONER) --n 4 --r 2
	@touch $(DATASET_OUTPUT)

# Clean-up command (if needed)
.PHONY: clean
clean:
	@echo "Cleaning up..."
	# Add clean-up commands here (e.g., removing generated files)
	@rm -f $(DATASET_OUTPUT) $(K_FOLD_OUTPUT) $(OPENAI_OUTPUT)
