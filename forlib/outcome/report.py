import docx
from datetime import datetime
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
# class MdExport:


class DocxExport:
    def __init__(self):
        document = docx.Document()
        heading = document.add_heading('분석 보고서', 0)
        heading.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        date_info = document.add_paragraph(str(datetime.now()))
        date_info.alignment = WD_PARAGRAPH_ALIGNMENT.RIGHT

        self.document = document

    def make_table(self, data, row, col):
        table = self.document.add_table(rows=row, cols=col)
        table.styles = 'table'

        hdr_cells = table.rows[0].cells
        for i in range(0, len(data["x"])):
            hdr_cells[i].text = data["x"][i]

        row_cells = table.add_rows().cells
        row_cells[0].text = 'in process'

    def insert_img(self, path):
        self.document.add_picture(path)

    def save(self, name):
        self.document.save(name + '.docx')

