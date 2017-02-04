let fs = require('fs'),
    PDFParser = require("pdf2json"),
    express = require('express'),
    app = express(),
    http = require('http').Server(app);

var port = process.env.PORT || 8000
//SET UP STATIC ASSETS FOLDER
app.use(express.static(__dirname + '/static'));

//SERVE HTML AND BEGIN LISTENING
app.get('/', function(req,res) {
  res.sendFile(__dirname + "/index.html");
});
http.listen(port,function() {
  console.log("Listening on ",port);
});


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

parseResume(__dirname + "/static/assets/data/resumes/resume2.pdf",__dirname+ "/resume_data/resume2.json")
