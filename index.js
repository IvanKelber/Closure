let fs = require('fs'),
    PDFParser = require("pdf2json"),
    multer = require('multer'),
    express = require('express'),
    app = express(),
    http = require('http').Server(app),
    spawn = require("child_process").spawn;



let pdfParser = new PDFParser(this,1);

var port = process.env.PORT || 8000;

//Multer middleware.  This determines how to handle the uploaded file (destination and filename)
var storage =   multer.diskStorage({
  destination: function (req, file, callback) {
    callback(null, __dirname + '/static/assets/data/resumes');
  },
  filename: function (req, file, callback) {
    callback(null, file.fieldname + '_' + Date.now());
  }
});

//Callback used when user hits 'upload' button.

var upload = multer({ storage : storage}).single('uploaded_resume');

//SET UP STATIC ASSETS FOLDER
app.use(express.static(__dirname + '/static'));


//==========ROUTES===================
//**GETS**
app.get('/', function(req,res) {
  // res.sendFile(__dirname + "/index.html");
  res.redirect("/upload");
});
app.get('/upload',function(req,res) {
  res.sendFile(__dirname + "/upload.html")
})
app.get('/employer',function(req,res) {
  res.sendFile(__dirname + "/employer.html")
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
          // sendMail()
        }

        setTimeout(function() {
          res.redirect("/upload");
        },1000);
    });
});

//LISTEN
http.listen(port,function() {
  console.log("Listening on ",port);
});


function parseResume(pdf,out) {
  // pdf: a path to a pdf resume
  // out: the specified path for the json output
  pdfParser.on("pdfParser_dataError", errData => console.error(errData.parserError) );
  pdfParser.on("pdfParser_dataReady", pdfData => {
      fs.writeFile(out, pdfParser.getRawTextContent(),function(err){
        if(err) {
          throw err;
        }
        parseText(out,onTextRead);
      });
  });

  pdfParser.loadPDF(pdf);
}

function sendMail() {
  var proc = spawn('python',[__dirname +"/python/emailer.py", "True","The Khal Drogo Venture","urlol.com"]);
  proc.stdout.on('data', function (data){
  // Do something with the data returned from python script
  });
}

function parseText(out,callback) {
  //nothing yet
  fs.readFile(out,'utf-8',callback);
}

function onTextRead(err,data) {
  if (err) {
    throw err;
  }
  var proc = spawn('python',[__dirname+"/python/parser.py"])
  proc.stdout.on('data',function(data) {
    console.log(data);
  });
}
