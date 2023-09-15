from reportlab.lib import colors
## Create pdf file
pdf = Pdf('test', font.helvetica, 14, colors.black)

## Add subtitle
sub_title = 'Hello World'
for i in range(1):
    pdf.add_subtitle(sub_title, 0, 0, 0)

## Add paragraph
paragraph = 'Whether article spirits new her covered hastily sitting her. Money witty books nor son add. Chicken age had evening believe but proceed pretend mrs. At missed advice my it no sister. Miss told ham dull knew see she spot near can. Spirit her entire her called. Arrived totally in as between private. Favour of so as on pretty though elinor direct. Reasonable estimating be alteration we themselves entreaties me of reasonably. Direct wished so be expect polite valley. Whose asked stand it sense no spoil to. Prudent you too his conduct feeling limited and. Side he lose paid as hope so face upon be. Goodness did suitable learning put.'
for i in range(1):
    pdf.add_paragraph(paragraph, 0, 0, colors.blue)

## Add table
table_title = ['one', 'two', 'three', 'four', 'five']
table_data = [['Osprey Aether Plus 100 Pack', 102.0, 400, 'backpack', 1], ['Medical Kit', 4.5, 20, 'health and safety', 1]]
table_note = 'This is table note'
for i in range(1):
    pdf.add_table('Gear List', table_title, table_data, table_note, 0, 0, 0)

## Add another paragraph
pdf.add_paragraph(paragraph, font.helvetica, 18, colors.lightgrey)

## Add another subtitle
pdf.add_subtitle(sub_title, 0, 0, 0)

## Save file
pdf.save()