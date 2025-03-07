# This to convert from WORD to PDF
# --REQUIRMENTS ** Document file(.docx) to be converted
import comtypes.client

word = comtypes.client.CreateObject("Word.Application")
doc = word.Documents.Open("example.docx") #-- Enter the document name here!!
doc.SaveAs("output.pdf", FileFormat=17)  # Enter the output file name here!!
doc.Close()
word.Quit()

print("Word converted to PDF successfully!")
