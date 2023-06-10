import asyncio
import json

from openai_api.openai_api import OpenaiApi
from pptx_parser.pptx_parser import PptxParser


class GptPptxExplainer:
    """
    Connects between the parsing of the presentation and calling the OpenAi API asynchronously to receive the
    explanation of each slide.
    """

    @classmethod
    async def explain(cls, input_file_path, output_dir):
        """
        Receives a path to a pptx file, connects to OpenAi asynchronously and receives the explanation to each slide.
        Creates a json file with the explanation of the presentation.
        :param input_file_path: str path to a pptx file
        """
        tasks = []
        gpt_outputs = []
        # Parse the presentation
        for index, slide_text in PptxParser.parse(input_file_path):
            prompt_content = {
                'slide_index': index,
                'file_title': input_file_path.name,
                'slide_text': slide_text
            }
            # save the openai_api explanation results
            tasks.append(
                OpenaiApi.get_model_response(gpt_outputs, prompt_content)
            )
        await asyncio.gather(*tasks)
        # save the results in json
        with open(output_dir / input_file_path.with_suffix('.json').name, 'w') as f:
            f.write(json.dumps(gpt_outputs))

#
# if __name__ == "__main__":
#     file_path = input("Enter a pptx file path: ")
#     asyncio.run(GptPptxExplainer.explain(file_path))
