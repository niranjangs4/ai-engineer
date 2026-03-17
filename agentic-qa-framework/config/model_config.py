MODEL_CONFIG = {

    "planner": {
        "model": "llama3.1:8b",
        "temperature": 0
    },

    "executor": {
        "model": "qwen2.5:7b",
        "temperature": 0
    },

    "vision": {
        "model": "qwen2.5vl:7b",
        "temperature": 0
    },

    "code_generator": {
        "model": "deepseek-coder:6.7b",
        "temperature": 0.2
    }

}