import argparse
import logging
import os

import autogen
from dotenv import load_dotenv

from agents.factory import init_agents
from utils.config_loader import get_dynamic_model, get_llm_config

# Load environment variables from .env file
load_dotenv()

# Global Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("SOC-Agent")


def parse_args():
    """
    Configures and parses command-line interface arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Agentic-SOC-Response: Autonomous threat mitigation orchestrator."
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input network log file."
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable full orchestration traces."
    )
    parser.add_argument(
        "--rounds",
        "-r",
        type=int,
        default=12,
        help="Max conversation rounds per session.",
    )
    return parser.parse_args()


def main(input_file, verbose=False, rounds=12):
    """
    Main entry point for the SOC Agentic Workflow.
    """
    if not os.path.exists(input_file):
        logger.error(f"IO Error: Input file '{input_file}' not found.")
        return

    # Execute dynamic model discovery
    selected_model = get_dynamic_model(logger)
    llm_settings = get_llm_config(selected_model)

    # Log management based on verbosity level
    if not verbose:
        logging.getLogger("autogen").setLevel(logging.WARNING)

    try:
        with open(input_file, "r") as f:
            log_data = f.read()
    except Exception as e:
        logger.error(f"File access error: {e}")
        return

    # MAS instantiation and orchestration
    analyst, architect, validator, executor = init_agents(llm_settings)

    group_chat = autogen.GroupChat(
        agents=[executor, analyst, architect, validator],
        messages=[],
        max_round=rounds,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )

    manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config=llm_settings,
        is_termination_msg=lambda x: "TERMINATE" in (x.get("content") or ""),
    )

    logger.info(f"Incident Analysis Pipeline started: {input_file}")

    # Initiate autonomous negotiation
    executor.initiate_chat(
        manager,
        message=f"Threat detection log provided for mitigation:\n\n{log_data}\n\nNOTE: If real mitigation fails due to environment restrictions, provide a simulation script that logs the intended actions and exit with code 0.",
        silent=not verbose,
    )

    logger.info("Mitigation workflow terminated.")


if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args.input, verbose=cli_args.verbose, rounds=cli_args.rounds)
