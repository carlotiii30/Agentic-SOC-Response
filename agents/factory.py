import autogen

from agents.profiles import (
    ANALYST_SYSTEM_MESSAGE,
    ARCHITECT_SYSTEM_MESSAGE,
    VALIDATOR_SYSTEM_MESSAGE,
)


def init_agents(llm_config):
    """
    Initializes the Multi-Agent System (MAS) architecture.

    Args:
        llm_config (dict): Common LLM settings for all agents.

    Returns:
        tuple: Initialized instances of AssistantAgents and UserProxyAgent.
    """
    analyst = autogen.AssistantAgent(
        name="Security_Analyst",
        llm_config=llm_config,
        system_message=ANALYST_SYSTEM_MESSAGE,
    )

    architect = autogen.AssistantAgent(
        name="Script_Architect",
        llm_config=llm_config,
        system_message=ARCHITECT_SYSTEM_MESSAGE,
    )

    validator = autogen.AssistantAgent(
        name="Security_Validator",
        llm_config=llm_config,
        system_message=VALIDATOR_SYSTEM_MESSAGE,
    )

    executor = autogen.UserProxyAgent(
        name="System_Executor",
        human_input_mode="NEVER",
        code_execution_config={
            "work_dir": "network_logs",
            "use_docker": False,
        },
        is_termination_msg=lambda x: "TERMINATE" in (x.get("content") or ""),
    )

    return analyst, architect, validator, executor
