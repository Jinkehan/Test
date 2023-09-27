# Provide font names for Pdf class
class Font:
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


class Pdf:
    def __init__(self, document_title, basic_font, basic_font_size, basic_font_color):
        # Import libraries
        from reportlab.pdfgen import canvas
        from reportlab.platypus import Paragraph
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import ParagraphStyle
        # Set basic variables
        w, h = letter
        self.canvasWidth = w - 80
        self.canvasHeight = h - 80
        self.startHeight = h - 30
        self.currentHeight = self.startHeight
        self.page = 1
        self.font = basic_font
        self.fontSize = basic_font_size
        self.fontColor = basic_font_color
        # Create pdf object
        file_name = document_title + '.pdf'
        file = canvas.Canvas(file_name, pagesize=letter)
        add_page_num(file, self.page)
        # Print title on file
        title_style = ParagraphStyle('title_style',
                                     fontName=self.font,
                                     fontSize=(self.fontSize * 2),
                                     leading=(self.fontSize * 2) * 1.2)
        title = Paragraph(document_title, title_style)
        used_width, used_height = title.wrap(self.canvasWidth, self.currentHeight)
        title.drawOn(file, 40, self.startHeight - 40)
        # Set leftover variables
        self.currentHeight -= used_height * 2
        self.file = file

    def add_paragraph(self, title, content_list, font, font_size, font_color):
        # import libraries
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        # Declare variables
        paragraph_title = title
        paragraph_content_list = content_list
        if font == 0:
            paragraph_font = self.font
        else:
            paragraph_font = font
        if font_size == 0:
            paragraph_font_size = self.fontSize
        else:
            paragraph_font_size = font_size
        if font_color == 0:
            paragraph_font_color = self.fontColor
        else:
            paragraph_font_color = font_color
        current_height = self.currentHeight
        file = self.file
        ## Print paragraph title
        # Set paragraph_title style and create paragraph_title
        paragraph_title_style = ParagraphStyle('paragraph_title_style',
                                               fontName=paragraph_font,
                                               fontSize=paragraph_font_size+2,
                                               leading=(paragraph_font_size+2) * 1.2,
                                               textColor=paragraph_font_color)
        paragraphTitle = Paragraph(paragraph_title, paragraph_title_style)
        # Access room for paragraph_title
        leftover_height = current_height - 50 - (paragraph_font_size+2)*1.2
        used_width, used_height = paragraphTitle.wrap(self.canvasWidth, leftover_height)
        # Create new page if needed
        if used_height > leftover_height:
            file.showPage()
            self.page += 1
            add_page_num(file, self.page)
            current_height = self.startHeight
        # Draw paragraph_title
        current_height -= used_height
        paragraphTitle.drawOn(file, 40, current_height)
        current_height -= paragraph_font_size
        ## Print paragraph content
            # Modify paragraphs
        leading_space = '&nbsp;'
        for i in range(7):
            leading_space += '&nbsp;'
        for p in paragraph_content_list:
            paragraph = '<p>' + leading_space + p + '</p>'
            # Set paragraph style and create paragraph
            paragraph_style = ParagraphStyle('paragraph_style',
                                             fontName=paragraph_font,
                                             fontSize=paragraph_font_size,
                                             leading=paragraph_font_size * 1.2,
                                             textColor=paragraph_font_color)
            paragraphContent = Paragraph(paragraph, paragraph_style)
            brockenParagraphList = [paragraphContent]
            # Assess room for paragraph
            leftover_height = current_height - 50 - paragraph_font_size * 1.2
            used_width, used_height = paragraphContent.wrap(self.canvasWidth, leftover_height)
            # Break paragraph if not enough room
            break_paragraph = False
            while used_height > leftover_height:
                break_paragraph = True
                helperParagraph = brockenParagraphList[-1]
                brockenParagraphList.pop(-1)
                helperParagraphList = helperParagraph.split(self.canvasWidth, leftover_height)
                for pa in helperParagraphList:
                    brockenParagraphList.append(pa)
                if len(brockenParagraphList) == 0:
                    helperPara = Paragraph('', paragraph_style)
                    brockenParagraphList.append(helperPara)
                    brockenParagraphList.append(helperParagraph)
                helperParagraph = brockenParagraphList[-1]
                leftover_height = self.canvasHeight
                used_width, used_height = helperParagraph.wrap(self.canvasWidth, leftover_height)
            # Print paragraph if no break occurred
            if not break_paragraph:
                current_height -= used_height
                paragraphContent.drawOn(file, 40, current_height)
            # Print paragraph if break occurred
            else:
                for pa in range(len(brockenParagraphList)):
                    leftover_height = current_height-60-paragraph_font_size*1.2
                    used_width, used_height = brockenParagraphList[pa].wrap(self.canvasWidth, leftover_height)
                    current_height -= used_height
                    brockenParagraphList[pa].drawOn(file, 40, current_height)
                    # Create new page
                    if not pa == len(brockenParagraphList) - 1:
                        file.showPage()
                        self.page += 1
                        pageNumber = file.beginText(300, 20)
                        pageNumber.setFont(Font.helvetica, 12)
                        pageNumber.textLine(str(self.page))
                        file.drawText(pageNumber)
                        current_height = self.startHeight
        # Save variables
        self.currentHeight = current_height-paragraph_font_size*2
        self.file = file

    def add_subtitle(self, sub_title, input_font, font_size, color):
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        # Declare variables
        file = self.file
        height = self.currentHeight
        if font_size == 0:
            font_size = self.fontSize + 4
        if input_font == 0:
            input_font = self.font
        if color == 0:
            color = self.fontColor
        # Create sub_title object
        subtitle_style = ParagraphStyle('subtitle_style',
                                        fontName=input_font,
                                        fontSize=font_size,
                                        leading=font_size * 1.2,
                                        textColor=color)
        subtitle = Paragraph(sub_title, subtitle_style)
        # Check allowed height create new page if needed
        allowed_height = height - 50 - font_size * 1.2
        a, used_height = subtitle.wrap(self.canvasWidth, allowed_height)
        if used_height > allowed_height:
            # Add new page
            file.showPage()
            self.page += 1
            page_number = file.beginText(300, 20)
            page_number.setFont(Font.helvetica, 12)
            page_number.textLine(str(self.page))
            file.drawText(page_number)
            height = self.startHeight
            ###
        # Draw and save variables
        subtitle.drawOn(file, 40, height - used_height)
        self.file = file
        self.currentHeight = height - used_height - font_size

    def add_table(self, table_name, title_list, data_list, table_note, input_font, font_size, color):
        from reportlab.platypus import Table, Paragraph, TableStyle
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        # Declare variables
        file = self.file
        height = self.currentHeight
        if font_size == 0:
            font_size = self.fontSize
        else:
            font_size = font_size
        if input_font == 0:
            input_font = self.font
        if color == 0:
            color = self.fontColor
        allowed_height = height - 60 - (font_size + 2) * 1.2
        # Create table object
        data_list.insert(0, title_list)
        t = Table(data_list, style=[('FONT', (0, 0), (-1, -1), input_font, font_size),
                                    ('RIGHTPADDING', (0, 0), (-1, -1), 20),
                                    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                                    ('TOPPADDING', (0, 0), (-1, -1), 5),
                                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                                    ('BOX', (0, 0), (-1, -1), 1, colors.silver),
                                    ('TEXTCOLOR', (0, 1), (-1, -1), color)])
        table_width, table_height = t.wrap(self.canvasWidth, self.canvasHeight)
        # Adjust table font_size if width to big
        while table_width > self.canvasWidth:
            font_size -= 0.1
            t = Table(data_list, style=[('FONT', (0, 0), (-1, -1), input_font, font_size),
                                        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
                                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                                        ('TOPPADDING', (0, 0), (-1, -1), 5),
                                        ('LEFTPADDING', (0, 0), (-1, -1), 10),
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]),
                                        ('BOX', (0, 0), (-1, -1), 1, colors.silver),
                                        ('TEXTCOLOR', (0, 1), (-1, -1), color)])
            table_width, table_height = t.wrap(self.canvasWidth, self.canvasHeight)
            allowed_height = height - 60 - (font_size + 2) * 1.2
        # Print table title
        title_style = ParagraphStyle('title_style',
                                     fontName=input_font,
                                     fontSize=font_size + 4,
                                     leading=(font_size + 2) * 2)
        title = Paragraph(table_name, title_style)
        a, title_height = title.wrap(self.canvasWidth, allowed_height)
        # Print table_note
        if not table_note == 0:
            note_style = ParagraphStyle('note_style',
                                        fontName=input_font,
                                        fontSize=font_size - 4,
                                        leading=font_size * 1.2,
                                        textColor=colors.gray)
            note = Paragraph(table_note, note_style)
            a, note_height = note.wrap(self.canvasWidth, allowed_height)
        else:
            note_height = 0
        # Check available height
        used_height = title_height + table_height + note_height
        if used_height > allowed_height:
            # Add new page
            file.showPage()
            self.page += 1
            page_number = file.beginText(300, 20)
            page_number.setFont(Font.helvetica, 12)
            page_number.textLine(str(self.page))
            file.drawText(page_number)
            height = self.startHeight
            ###
        title.drawOn(file, 40, height - title_height)
        t.drawOn(file, 40, height - title_height - table_height)
        if not table_note == 0:
            note.drawOn(file, 40, height - used_height)
        # Save variables
        self.file = file
        self.currentHeight = height - used_height - font_size * 2
        # Remove the title added to data_list on line below # Create table object
        data_list.pop(0)
    def save(self):
        self.file.save()


# Add page number function
def add_page_num(file, page_number):
    pageNumber = file.beginText(300, 20)
    pageNumber.setFont(Font.helvetica, 12)
    pageNumber.textLine(str(page_number))
    file.drawText(pageNumber)


"""
Test material
"""
# Create pdf
from reportlab.lib import colors

test_pdf = Pdf('pdf_editor_test', Font.helvetica, 14, colors.black)

# Paragraph
paragraph_title = 'Paragraph Title'
paragraph_content = [
    'Ye on properly handsome returned throwing am no whatever. In without wishing he of picture no exposed talking minutes. Curiosity continual belonging offending so explained it exquisite. Do remember to followed yourself material mr recurred carriage. High drew west we no or at john. About or given on witty event. Or sociable up material bachelor bringing landlord confined. Busy so many in hung easy find well up. So of exquisite my an explained remainder. Dashwood denoting securing be on perceive my laughing so.',
    'In friendship diminution instrument so. Son sure paid door with say them. Two among sir sorry men court. Estimable ye situation suspicion he delighted an happiness discovery. Fact are size cold why had part. If believing or sweetness otherwise in we forfeited. Tolerably an unwilling arranging of determine. Beyond rather sooner so if up wishes or.',
    'She suspicion dejection saw instantly. Well deny may real one told yet saw hard dear. Bed chief house rapid right the. Set noisy one state tears which. No girl oh part must fact high my he. Simplicity in excellence melancholy as remarkably discovered. Own partiality motionless was old excellence she inquietude contrasted. Sister giving so wicket cousin of an he rather marked. Of on game part body rich. Adapted mr savings venture it or comfort affixed friends.']
for i in range(1):
    test_pdf.add_paragraph(paragraph_title, paragraph_content, 0, 0, 0)

# Subtitle
subtitle = 'This is a subtitle'
for i in range(1):
    test_pdf.add_subtitle(subtitle, 0, 0, 0)

# Table
table_title = ['one', 'two', 'three', 'four', 'five']
table_data = [['Osprey Aether Plus 100 Pack', 102.0, 400, 'backpack', 1],
              ['Medical Kit', 4.5, 20, 'health and safety', 1], ['REI Sahara Shade Hoodie', 6.9, 50, 'clothing', 1],
              ['Katadyn BeFree 1.0 L', 2.3, 50, 'water treatment', 1], ['Soto Amicus', 2.8, 45, 'camp kitchen', 1]]
table_note = 'This is table note'
for i in range(1):
    test_pdf.add_table('asdfd', table_title, table_data, table_note, 0, 0, 0)

# Everything together
for i in range(10):
    test_pdf.add_subtitle(subtitle, 0, 0, 0)
    test_pdf.add_paragraph(paragraph_title, paragraph_content, 0, 0, 0)
    test_pdf.add_table('asdfd', table_title, table_data, table_note, 0, 0, 0)
# Save
test_pdf.save()
