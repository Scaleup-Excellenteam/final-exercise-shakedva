import argparse
import time
from pathlib import Path
from .gpt_pptx_explainer import GptPptxExplainer
import asyncio
import logging

logging.basicConfig(
    filename='../gpt_explainer_checker.log',
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)
logger = logging.getLogger(__name__)


class GptExplainerChecker:
    def __init__(self):
        self.processed_requests = set()

    def run(self, input_dir: str, output_dir: str):
        input_dir_path = Path(input_dir)
        output_dir_path = Path(output_dir)
        while True:
            for file in input_dir_path.iterdir():
                if file.stem not in self.processed_requests:
                    logger.debug(f"Found non-processed request {file.stem} ")
                    self.processed_requests.add(file.stem)
                    asyncio.run(GptPptxExplainer.explain(file.absolute(), output_dir_path))
                    logger.debug(f"Request {file.stem} processed")
            time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input-dir",
        type=str,
        help="Directory to scan for new pptx files to run GptExplainer on",
        default='uploads'
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        help="Directory to save explained pptx files",
        default='outputs'
    )
    args = parser.parse_args()
    checker = GptExplainerChecker()
    checker.run(args.input_dir, args.output_dir)
