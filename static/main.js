
var inputString = document.getElementById("input-txt")
var resultBox = document.getElementById("result-box");

function submitImage() {
  // action for the submit button
  console.log("submit");

  var inputString = document.getElementById("input-txt")
  // call the predict function of the backend
  console.log(inputString.value);
  predictImage(inputString.value);
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

function displayResult(data) {
  // display the result
  // hide(loader);
  console.log(data)
  var resultString = data.icon_d; 
  resultString += "\r\n" + data.icon_t + "\r\nDescription: " + data.desc_e +  "\r\nPositive: " + data.pos + " Neutral: "+ data.neu + " Negative: " + data.neg
  console.log(resultString)

  var resultBox = document.getElementById("result-box");
  console.log(resultBox)
  // predResult.innerHTML = resultString 
  resultBox.innerHTML = resultString;

   // show(predResult);
   //show(resultBox);
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
