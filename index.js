let fs = require('fs'),
    PDFParser = require("pdf2json"),
    multer = require('multer'),
    express = require('express'),
    app = express(),
    http = require('http').Server(app);

var port = process.env.PORT || 8000

var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, __dirname + '/static/assets/data/resumes');
  },
  filename: function (req, file, callback) {
    callback(null, file.fieldname + '_' + Date.now());
  }
});


var upload = multer({ storage : storage}).single('uploaded_resume');

//SET UP STATIC ASSETS FOLDER
app.use(express.static(__dirname + '/static'));


//==========ROUTES===================
//**GETS**
app.get('/', function(req,res) {
  res.sendFile(__dirname + "/index.html");
});
app.get('/lol',function(req,res) {
  res.sendFile(__dirname + "/lol.html")
})
//**POSTS**
app.post('/api/photo',function(req,res){
    upload(req,res,function(err) {
        if(err) {
            return res.end("Error uploading file: ",err);
        }
        //If file was successfully uploaded, convert pdf to text
        if(req.file) {
          var out = __dirname + "/resume_data/" + req.file.filename;
          parseResume(req.file.path,out)
        }
        res.end("File is uploaded");
    });
});

//LISTEN
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
