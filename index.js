let fs = require('fs'),
    PDFParser = require("pdf2json");

let pdfParser = new PDFParser(this,1);

function parseResume(pdf,out) {
  // pdf: a path to a pdf resume
  // out: the specified path for the json output
  pdfParser.on("pdfParser_dataError", errData => console.error(errData.parserError) );
  pdfParser.on("pdfParser_dataReady", pdfData => {
      fs.writeFile(out, pdfParser.getRawTextContent());
  });

  pdfParser.loadPDF(pdf);
}
