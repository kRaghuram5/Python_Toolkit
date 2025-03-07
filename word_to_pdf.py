import comtypes.client

word = comtypes.client.CreateObject("Word.Application")
doc = word.Documents.Open("E:\\Doc1.docx")
doc.SaveAs("output2.pdf", FileFormat=17)  # 17 = PDF format
doc.Close()
word.Quit()

print("Word converted to PDF successfully!")