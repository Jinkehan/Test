class font:
    courier = 'Courier'
    courier_bold = 'Courier-Bold'
    courier_italic = 'Courier-Oblique'
    courier_bold_italic = 'Courier-BoldOblique'
    helvetica = 'Helvetica'
    helvetica_bold = 'Helvetica-Bold'
    helvetica_italic = 'Helvetica-Oblique'
    helvetica_bold_italic = 'Helvetica-BoldOblique'
    time_roman = 'Times-Roman'
    time_bold = 'Times-Bold'
    time_italic = 'Times-Italic'
    time_bold_italic = 'Times-BoldItalic'

def add_new_page(current_page):
    pass
class Pdf:
    def __init__(self, document_title, basic_font, basic_font_size, basic_text_color):
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Paragraph
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import ParagraphStyle
        # Set variables
        w, h = letter  # (width = 612, height = 792)
        self.page = 1
        self.fontSize = basic_font_size
        self.font = basic_font
        self.color = basic_text_color
        self.canvasWidth = w - 80
        self.canvasHeight = 692
        self.startHeight = 762
        file_name = document_title + '.pdf'
        # Create pdf object
        file = canvas.Canvas(file_name, pagesize=letter)
        # Add page number
        page_number = file.beginText(300, 20)
        page_number.setFont(font.helvetica, 12)
        page_number.textLine(str(self.page))
        file.drawText(page_number)
        ###
        # Set and print title
        style = ParagraphStyle('MyPara style',
                               FontName='Helvetica',
                               fontSize=30,
                               leading=30 * 1.2)
        title = Paragraph(document_title, style)
        a, used_height = title.wrap(self.canvasWidth, self.canvasHeight)
        title.drawOn(file, 40, self.startHeight - 40)
        # Set init variables
        self.pdf = file
        self.heightIndex = self.startHeight - used_height * 2