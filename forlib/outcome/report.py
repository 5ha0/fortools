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

    def make_table(self, data):
        table = self.document.add_table(rows=1, cols=len(data[0].keys()))
        table.style = 'Table Grid'
        table.rows[0].style = "borderColor:red;background-color:gray"

        col_list = list(data[0].keys())

        hdr_cells = table.rows[0].cells
        for i in range(0, len(data[0].keys())):
            hdr_cells[i].text = str(col_list[i])

        for i in range(0, len(data)):
            row_cells = table.add_row().cells
            result = list(data[i].values())
            for j in range(0, len(data[0].keys())):
                row_cells[j].text = str(result[j])

    def insert_img(self, path):
        self.document.add_picture(path)

    def save(self, name):
        self.document.save(name + '.docx')

