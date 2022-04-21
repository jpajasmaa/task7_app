
// file handling

var fileSelect = document.getElementById("file-upload");
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileSelectHandler(e) {
  // handle file selecting
  var files = e.target.files || e.dataTransfer.files;
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

var inputString = document.getElementById("input-txt")

imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

var resultBox = document.getElementById("result-box");

function submitImage() {
  // action for the submit button
  console.log("submit");

  var inputString = document.getElementById("input-txt")
  //loader.classList.remove("hidden");
  //imageDisplay.classList.add("loading");

  // call the predict function of the backend
  console.log(inputString.value);
  predictImage(inputString.value);
}


function previewFile(file) {
  // show the preview of the image
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reset
    predResult.innerHTML = "";
    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}


// Prediction part

function predictImage(image) {
  fetch("/classify", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("An error occured", err.message);
    });
}


// Display

function displayImage(image, id) {
  // display image on given id <img> element
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // display the result
  // imageDisplay.classList.remove("loading");
  hide(loader);
  console.log(data)
  var resultString = data.result.toString(); 
  // predResult.innerHTML = resultString 
  resultBox.innerHTML = resultString;

   show(predResult);
   show(resultBox);
}

// utility

function hide(el) {
  // hide an element
  el.classList.add("hidden");
}

function show(el) {
  // show an element
  el.classList.remove("hidden");
}

function clearImage() {
  // reset selected files
  fileSelect.value = "";

  // remove image sources and hide them
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";
  resultBox.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  hide(resultBox);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}
