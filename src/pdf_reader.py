from typing import List

def parse_pdf(path):
    import pypdf

    pdfFileObj = open(path, "rb")
    pdfReader = pypdf.PdfReader(pdfFileObj)

    pages: List[str] = []

    for i, page in enumerate(pdfReader.pages):
        page = page.extract_text()
        pages.append(page)

    pdfFileObj.close()
    return pages
