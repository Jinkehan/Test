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

    # Input {input_font}or{font_size}or{color} = 0 to use basic_font_size from init method
    def add_subtitle(self, sub_title, input_font, font_size, color):
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        # Declare variables
        file = self.pdf
        height = self.heightIndex
        if font_size == 0:
            font_size = self.fontSize + 4
        if input_font == 0:
            input_font = self.font
        if color == 0:
            color = self.color
        # Create sub_title object
        subtitle_style = ParagraphStyle('subtitle_style',
                                        fontName=input_font,
                                        fontSize=font_size,
                                        leading=font_size * 1.2,
                                        textColor=color)
        subtitle = Paragraph(sub_title, subtitle_style)
        # Check allowed height create new page if needed
        allowed_height = height - 60 - font_size * 1.2
        a, used_height = subtitle.wrap(self.canvasWidth, allowed_height)
        if used_height > allowed_height:
            # Add new page
            file.showPage()
            self.page += 1
            page_number = file.beginText(300, 20)
            page_number.setFont(font.helvetica, 12)
            page_number.textLine(str(self.page))
            file.drawText(page_number)
            height = self.startHeight
            ###
        # Draw and save variables
        subtitle.drawOn(file, 40, height - used_height)
        self.pdf = file
        self.heightIndex = height - used_height - font_size

    def add_paragraph(self, input_text_list, paragraph_title, input_font, font_size, color):
        from reportlab.platypus import Paragraph
        from reportlab.lib.styles import ParagraphStyle
        # Declare Variables
        file = self.pdf
        height = self.heightIndex
        if font_size == 0:
            font_size = self.fontSize
        if input_font == 0:
            input_font = self.font
        if color == 0:
            color = self.color
        if not paragraph_title == 0:
            title_style = ParagraphStyle('title_style',
                                         fontName=input_font,
                                         fontSize=font_size + 2,
                                         leading=(font_size + 2) * 1.2,
                                         textColor=color)
            title = Paragraph(paragraph_title, title_style)
            allowed_height = height - 60 - (font_size + 2) * 1.2
            a, used_height = title.wrap(self.canvasWidth, allowed_height)
            if used_height > allowed_height:
                # Add new page
                file.showPage()
                self.page += 1
                page_number = file.beginText(300, 20)
                page_number.setFont(font.helvetica, 12)
                page_number.textLine(str(self.page))
                file.drawText(page_number)
                height = self.startHeight
                ###
            title.drawOn(file, 40, height)
            height -= used_height + (font_size + 2) * 1.2
        # Create paragraph from input_text_list
        """input_text = ''
        for t in input_text_list:
            t = t.strip()
            helper_string = ' &nbsp;'
            for i in range(3):
                helper_string += ' &nbsp;'
            text = helper_string + t
            input_text += text + '\n'"""

        # Modify python code
        for text in input_text_list:
            text = '<p>' + text + '</p>'
            # Set style
            my_style = ParagraphStyle('My Para style',
                                      fontName=input_font,
                                      fontSize=font_size,
                                      leading=font_size * 1.2,
                                      textColor=color)
            allowed_height = height - 60 - font_size * 1.2
            # Create Paragraph object from input_text
            paragraph = Paragraph(text, my_style)
            paragraph_list = [paragraph]
            a, used_height = paragraph.wrap(self.canvasWidth, allowed_height)
            if allowed_height < 0:
                file.showPage()
                self.page += 1
                # Add page number
                page_number = file.beginText(300, 20)
                page_number.setFont(font.helvetica, 12)
                page_number.textLine(str(self.page))
                file.drawText(page_number)
                ###
                allowed_height = self.canvasHeight
            # Split paragraph if needed
            while used_height > allowed_height:
                helper_paragraph = paragraph_list[len(paragraph_list) - 1]
                paragraph_list.pop(len(paragraph_list) - 1)
                helper_list = helper_paragraph.split(self.canvasWidth, allowed_height)
                for p in helper_list:
                    paragraph_list.append(p)
                if len(paragraph_list) == 0:
                    paragraph_list.append(helper_paragraph)
                    break
                helper_paragraph_two = paragraph_list[len(paragraph_list) - 1]
                a, used_height = helper_paragraph_two.wrap(self.canvasWidth, self.canvasHeight)
                allowed_height = self.canvasHeight
            # Print paragraph_list
            for p in range(len(paragraph_list)):
                a, used_height = paragraph_list[p].wrap(self.canvasWidth, self.canvasHeight)
                height = self.heightIndex - font_size * 1.2 - used_height
                paragraph_list[p].drawOn(file, 40, height)
                if not p == len(paragraph_list) - 1:
                    file.showPage()
                    self.page += 1
                    # Add page number
                    page_number = file.beginText(300, 20)
                    page_number.setFont(font.helvetica, 12)
                    page_number.textLine(str(self.page))
                    file.drawText(page_number)
                    ###
                    self.heightIndex = self.startHeight
        # Save variables
        self.pdf = file
        self.heightIndex = height - font_size * 2

    def add_table(self, table_name, title_list, data_list, table_note, input_font, font_size, color):
        from reportlab.platypus import Table, Paragraph, TableStyle
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib import colors
        # Declare variables
        file = self.pdf
        height = self.heightIndex
        if font_size == 0:
            font_size = self.fontSize
        else:
            font_size = font_size
        if input_font == 0:
            input_font = self.font
        if color == 0:
            color = self.color
        allowed_height = height - 60 - (font_size + 2) * 1.2
        # Create table object
        data_list.insert(0, title_list)
        t = Table(data_list, style=[('FONT', (0, 0), (-1, -1), font.helvetica, font_size),
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
            t = Table(data_list, style=[('FONT', (0, 0), (-1, -1), font.helvetica, font_size),
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
            page_number.setFont(font.helvetica, 12)
            page_number.textLine(str(self.page))
            file.drawText(page_number)
            height = self.startHeight
            ###
        title.drawOn(file, 40, height - title_height)
        t.drawOn(file, 40, height - title_height - table_height)
        if not table_note == 0:
            note.drawOn(file, 40, height - used_height)
        # Save variables
        self.pdf = file
        self.heightIndex = height - used_height - font_size * 2

    def add_text(self, input_subtitle, input_text, input_font, color):
        file = self.pdf
        height = self.heightIndex

        text = file.beginText(40, height)
        text.setFont(input_font, 12)
        text.setFillColor(color)
        text.textLine(input_text)
        file.drawText(text)

    def save(self):
        self.pdf.save()


"""
Test Material
Test Material
Test Material

Don't Copy !!!
Don't Copy !!!
Don't Copy !!!
"""

from reportlab.lib import colors

## Create pdf file
pdf = Pdf('test', font.helvetica, 14, colors.black)
input_text = []
input_text.append('Neat own nor she said see walk. And charm add green you these. Sang busy in this drew ye fine. At greater prepare musical so attacks as on distant. Improving age our her cordially intention. His devonshire sufficient precaution say preference middletons insipidity. Since might water hence the her worse. Concluded it offending dejection do earnestly as me direction. Nature played thirty all him.')
input_text.append('So delightful up dissimilar by unreserved it connection frequently. Do an high room so in paid. Up on cousin ye dinner should in. Sex stood tried walls manor truth shy and three his. Their to years so child truth. Honoured peculiar families sensible up likewise by on in.')
input_text.append('Old there any widow law rooms. Agreed but expect repair she nay sir silent person. Direction can dependent one bed situation attempted. His she are man their spite avoid. Her pretended fulfilled extremely education yet. Satisfied did one admitting incommode tolerably how are.')
input_text.append('1')
text_title = 'Random Text'

for i in range(1):
    pdf.add_paragraph(input_text, text_title, 0, 0, 0)
"""## Add subtitle
sub_title = 'Hello World'
for i in range(1):
    pdf.add_subtitle(sub_title, 0, 14, 0)

## Add paragraph
paragraph = 'Whether article spirits new her covered hastily sitting her. Money witty books nor son add. Chicken age had evening believe but proceed pretend mrs. At missed advice my it no sister. Miss told ham dull knew see she spot near can. Spirit her entire her called. Arrived totally in as between private. Favour of so as on pretty though elinor direct. Reasonable estimating be alteration we themselves entreaties me of reasonably. Direct wished so be expect polite valley. Whose asked stand it sense no spoil to. Prudent you too his conduct feeling limited and. Side he lose paid as hope so face upon be. Goodness did suitable learning put.'
for i in range(1):
    pdf.add_paragraph(paragraph, 0, 12, colors.blue)

## Add table
table_title = ['one', 'two', 'three', 'four', 'five']
table_data = [['Osprey Aether Plus 100 Pack', 102.0, 400, 'backpack', 1],
              ['Medical Kit', 4.5, 20, 'health and safety', 1], ['REI Sahara Shade Hoodie', 6.9, 50, 'clothing', 1],
              ['REI Trailbreak Trekking Poles ', 17.2, 70, 'gadget', 1],
              ['Black Diamond Spot 500R', 3.6, 75, 'electronics', 1],
              ['Katadyn BeFree 1.0 L', 2.3, 50, 'water treatment', 1], ['Soto Amicus', 2.8, 45, 'camp kitchen', 1]]
table_note = 'This is table note'
for i in range(1):
    pdf.add_table('asdfd', table_title, table_data, table_note, 0, 0, 0)

## Add another paragraph
pdf.add_paragraph(paragraph, font.helvetica, 18, colors.lightgrey)

## Add another subtitle
pdf.add_subtitle(sub_title, 0, 0, 0)"""

## Save file
pdf.save()
