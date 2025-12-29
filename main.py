"""
Main entry point for web automation demo - CLI runner.
"""
import logging
import json
import argparse
from automations.login import login
from automations.download_file import download_file
from automations.fill_form import fill_form
from automations.scrape_paginated_table import scrape_paginated_table
from automations.dynamic_loading import dynamic_loading

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

TASKS = {
    "login": login,
    "download": download_file,
    "form": fill_form,
    "scrape": scrape_paginated_table,
    "dynamic": dynamic_loading
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web automation framework")
    parser.add_argument(
        "--task",
        choices=list(TASKS.keys()),
        default="login",
        help="Task to run: login, download, form, scrape, or dynamic"
    )
    
    args = parser.parse_args()
    task_func = TASKS[args.task]
    
    logger = logging.getLogger(__name__)
    logger.info(f"Running task: {args.task}")
    
    result = task_func()
    print(json.dumps(result, indent=2))
