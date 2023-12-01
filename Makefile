# Define the Python command (change to python3 if required)
PYTHON := python

# Define script paths
CREATE_TASKS := owain_app/create_tasks.py
LEARNING_PROMPTS := owain_app/create_icl_prompts.py
ARTICULATION_PROMPTS:= owain_app/create_articulation_prompts.py
CONVERT_ICL_PROMPTS := owain_app/convert_icl_prompts.py
CONVERT_ARTICULATION_PROMPTS := owain_app/convert_articulation_prompts.py
PROCESS_ICL_RESPONSES := owain_app/process_icl_responses.py
API_REQUESTOR := owain_app/api_request_parallel_processor.py
GENERATE_FIGURES := owain_app/generate_figures.py

# Define output file paths or markers
CREATE_TASKS_OUTPUT := data/tasks
ICL_PROMPTS_OUTPUT := data/icl_prompts
ICL_REQUESTS_OUTPUT := data/icl_requests
ARTICULATION_PROMPTS_OUTPUT := data/articulation_prompts
ICL_RESPONSES_OUTPUT := data/icl_responses

create_tasks: $(CREATE_TASKS)
	@$(PYTHON) $(CREATE_TASKS) --n 5 --r 2

create_icl_prompts: $(CREATE_TASKS_OUTPUT) $(LEARNING_PROMPTS)
	@$(PYTHON) $(LEARNING_PROMPTS)

convert_icl_prompts: $(ICL_PROMPTS_OUTPUT) $(CONVERT_ICL_PROMPTS)
	@$(PYTHON) $(CONVERT_ICL_PROMPTS)

collect_icl_responses: $(ICL_REQUESTS_OUTPUT) $(API_REQUESTOR)
	mkdir -p data/icl_responses
	@poetry run python owain_app/api_request_parallel_processor.py --requests_filepath $(ICL_REQUESTS_OUTPUT)/icl_requests.jsonl \
		--save_filepath data/icl_responses/icl_responses.jsonl \
		--request_url 'https://api.openai.com/v1/chat/completions' \
		--max_requests_per_minute 10000 \
		--max_tokens_per_minute 300000 \
		--token_encoding_name cl100k_base \
		--max_attempts 5 \
		--logging_level 10

create_articulation_prompts: $(CREATE_TASKS_OUTPUT) $(ARTICULATION_PROMPTS)
	@$(PYTHON) $(ARTICULATION_PROMPTS)

convert_articulation_prompts: $(ARTICULATION_PROMPTS_OUTPUT) $(ARTICULATION)
	@$(PYTHON) $(CONVERT_ARTICULATION_PROMPTS)

process_icl_responses: $(ICL_RESPONSES_OUTPUT) $(PROCESS_ICL_RESPONSES)
	@$(PYTHON) $(PROCESS_ICL_RESPONSES)

# Clean-up command (if needed)
.PHONY: clean
clean:
	@rm -f $(DATASET_OUTPUT) $(K_FOLD_OUTPUT) $(OPENAI_OUTPUT)
