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

FOUND_REQUEST = "Found non-processed request {}"
PROCESSED = "Request {} processed"
SLEEP_DURATION = 30


class GptExplainerChecker:
    """
    Call gpt explainer to process new files in a given directory.
    """

    def __init__(self):
        self.processed_requests = set()

    def run(self, input_dir: str, output_dir: str):
        """
        Scans an input directory every few seconds and sends the files who weren't processed yet to the
        GptPptxExplainer.
        :param input_dir: str path to scan for new files.
        :param output_dir: str path to save new gpt explained files.
        """
        input_dir_path = Path(input_dir)
        output_dir_path = Path(output_dir)
        while True:
            for file in input_dir_path.iterdir():
                if file.stem not in self.processed_requests:
                    logger.debug(FOUND_REQUEST.format(file.stem))
                    self.processed_requests.add(file.stem)
                    asyncio.run(GptPptxExplainer.explain(file.absolute(), output_dir_path))
                    logger.debug(PROCESSED.format(file.stem))
            time.sleep(SLEEP_DURATION)


if __name__ == '__main__':
    """
    Runs the gpt checker server with input and output directories. 
    """
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
