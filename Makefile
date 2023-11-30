# Define the Python command (change to python3 if required)
PYTHON := python

# Define script paths
CREATE_TASKS := owain_app/create_tasks.py
LEARNING_PROMPTS := owain_app/create_icl_prompts.py
ARTICULATION_PROMPTS:= owain_app/create_articulation_prompts.py
ARTICULATION := owain_app/articulation.py
GENERATE_FIGURES := owain_app/generate_figures.py

# Define output file paths or markers
DATASET_OUTPUT := data/dataset_output_marker
K_FOLD_OUTPUT := data/k_fold_output_marker
OPENAI_OUTPUT := data/openai_output_marker
CREATE_TASKS_OUTPUT := data/tasks

create_tasks: $(CREATE_TASKS)
	@$(PYTHON) $(CREATE_TASKS) --n 5 --r 2

create_icl_prompts: $(CREATE_TASKS_OUTPUT) $(LEARNING_PROMPTS)
	@$(PYTHON) $(LEARNING_PROMPTS)

create_articulation_prompts: $(CREATE_TASKS_OUTPUT) $(ARTICULATION_PROMPTS)
	@$(PYTHON) $(ARTICULATION_PROMPTS)

# Clean-up command (if needed)
.PHONY: clean
clean:
	@rm -f $(DATASET_OUTPUT) $(K_FOLD_OUTPUT) $(OPENAI_OUTPUT)
