import argparse
import time
from pathlib import Path
from .gpt_pptx_explainer import GptPptxExplainer
import asyncio
import logging
from db.orm import DB, Upload
from api.request_status_enum import RequestStatusEnum
from api.utils import get_file_extension
import datetime

db = DB()
logging.basicConfig(
    filename='gpt_explainer_checker.log',
    level=logging.INFO,
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

    def run(self, input_dir: str, output_dir: str):
        """
        Every few seconds, check for pending uploads in the database, save them in an output directory and calls the
        GptPptxExplainer.
        :param input_dir: str path to scan for new files.
        :param output_dir: str path to save new gpt explained files.
        """
        input_dir_path = Path(input_dir)
        output_dir_path = Path(output_dir)
        while True:
            with db.session() as session:
                pending_uploads = session.query(Upload).filter(Upload.status == RequestStatusEnum.PENDING)
                for upload in pending_uploads:
                    logger.info(FOUND_REQUEST.format(upload.filename))
                    upload.status = RequestStatusEnum.PROCESSED
                    session.commit()
                    filename = upload.uid + '.' + get_file_extension(upload.filename)
                    asyncio.run(GptPptxExplainer.explain(Path(input_dir_path / filename), output_dir_path.absolute()))
                    upload.status = RequestStatusEnum.DONE
                    upload.finish_time = datetime.datetime.now()
                    session.commit()
                    logger.info(PROCESSED.format(upload.filename))
            time.sleep(SLEEP_DURATION)


def main():
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


if __name__ == '__main__':
    main()
