let fs = require('fs'),
    PDFParser = require("pdf2json");

let pdfParser = new PDFParser(this,1);

function parseResume(pdf) {
  pdfParser.on("pdfParser_dataError", errData => console.error(errData.parserError) );
  pdfParser.on("pdfParser_dataReady", pdfData => {
      fs.writeFile("./resume1.json", pdfParser.getRawTextContent());
  });

  pdfParser.loadPDF("./resume1.pdf");
}
