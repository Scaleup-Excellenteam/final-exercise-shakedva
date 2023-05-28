from pptx import Presentation


class PptxParser:

    @classmethod
    def parse(cls, filepath):
        prs = Presentation(filepath)
        for index, slide in enumerate(prs.slides):
            slide_text = []
            for shape in slide.shapes:
                if not shape.has_text_frame:
                    continue
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run_text = run.text.strip()
                        if run_text:
                            slide_text.append(run_text)

            slide_text = " ".join(slide_text)
            yield index, slide_text
