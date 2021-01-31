import pdfkit

with open('test.html') as f:
    pdfkit.from_file(f, 'out.pdf')