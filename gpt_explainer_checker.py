import argparse
import time
from pathlib import Path
from gpt_pptx_explainer import GptPptxExplainer
import asyncio


class GptExplainerChecker:
    def __init__(self):
        self.processed_uids = set()

    def run(self):
        while (True):
            for uid_dir in Path(args.target_dir).iterdir():
                if uid_dir not in self.processed_uids:
                    self.processed_uids.add(uid_dir)
                    file_path = next(uid_dir.glob("*.pptx"))  # todo make sure it has a pptx file
                    asyncio.run(GptPptxExplainer.explain(file_path))
            time.sleep(30)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target-dir",
        type=str,
        help="Directory to scan for new pptx files to run GptExplainer on",
        default='upload'
    )
    args = parser.parse_args()
    checker = GptExplainerChecker()
    checker.run()
