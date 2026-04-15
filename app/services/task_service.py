from app.core.llm import call_llm

def run_task(user_input: str) -> str:
    """
    最小任务执行流程：
    input -> LLM -> output
    """

    result = call_llm(user_input)

    return result