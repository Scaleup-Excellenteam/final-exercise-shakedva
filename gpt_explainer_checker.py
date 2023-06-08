import argparse
import time
from pathlib import Path
from gpt_pptx_explainer import GptPptxExplainer
import asyncio


class GptExplainerChecker:
    def __init__(self):
        self.processed_uids = set()

    def run(self, input_dir: str, output_dir: str):
        input_dir_path = Path(input_dir)
        output_dir_path = Path(output_dir)
        while True:
            for file in input_dir_path.iterdir():
                if file.stem not in self.processed_uids:
                    self.processed_uids.add(file.stem)
                    asyncio.run(GptPptxExplainer.explain(file.absolute(), output_dir_path))
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
