

// /admin 
var djangoData = $('#my-data').data();
ips = djangoData.ips;
times = djangoData.times;

var a = ips
a = a.replace(/'/g, '"');
ips = JSON.parse(a)

var a = times
a = a.replace(/'/g, '"');
times = JSON.parse(a)




// Get the modal
var modals = document.querySelectorAll(`[id^="myModal"]`);;


// Get the button that opens the modal
var btn = document.querySelectorAll(`[id^="myBtn"]`);


// Get the <span> element that closes the modal
var spans = document.getElementsByClassName("close");

// When the user clicks the button, open the modal 



function btnclick(id) {
  // console.log("here")
  btn2 = btn[id]
  modal = modals[id]
  
  modal.style.display = "block";
  // console.log("Modal opened");
  ip = ips[id]
  var heading = document.getElementById("in-heading-"+id)
  var body = document.getElementById("in-stuff-"+id)
  
  
  
  heading.innerHTML = "Some info about: " + ip
  
  
  
 $.getJSON('https://ipinfo.io/json', function(data) {

      country = data["country"]

      regionname = data["region"]
      city = data["city"]
      zip = data["postal"]
      loc= data["loc"]
      timezone = data["timezone"]
      isp = data["org"]

      html = `<b>Country</b>: ${country}<br>
              <b>Region Name</b>: ${regionname}<br>
              <b>City</b>: ${city}<br>
              <b>Zip Code</b>: ${zip}<br>
              <b>Location</b> : ${loc}<br>
              <b>Timezone</b>: ${timezone}<br>
              <b>ISP</b> : ${isp}<br>
      `

      body.innerHTML= html
      // console.log(body)
  })
  
  
}
// {"status":"success","country":"Pakistan","countryCode":"PK","region":"SD","regionName":"Sindh","city":"Karachi","zip":"75300","lat":24.9246,"lon":67.087,"timezone":"Asia/Karachi","isp":"Cyber Internet Services Pakistan","org":"Cyber","as":"AS9541 Cyber Internet Services (Pvt) Ltd.","query":"202.47.36.157"}


// When the user clicks on <span> (x), close the modal
for (var i = 0; i < spans.length; i++) {
  span = spans[i];
span.onclick = function() {
  modal.style.display = "none";
}
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

