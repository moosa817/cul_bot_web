//log stuff




 
 if(sessionStorage.getItem('session')){}

else{
  $.getJSON('http://ip-api.com/json', function(data) {
    ip = data["query"]
  sessionStorage.setItem('session',true)
  $.ajax({
    data: {
      ip,ip
    },
    type: 'POST',
    url: '/log'
  })
  .done(function (data) {});


  
  })
};












//js for image upload page
// document.getElementById("Hidenews").style.display = "none";
// document.getElementById("tab1").className = "highlight";
// document.getElementById("header").innerHTML = "Crafts";
var name_url 
//Set classes and page ^ v
document.getElementById("tab1").addEventListener("click", highlight1);
document.getElementById("tab2").addEventListener("click", highlight2);


document.getElementById("toChange").innerHTML = document.getElementById("page1").innerHTML
document.getElementById('name_for_url').innerHTML = name_url

//What happens when you click on tab 1:
function highlight1() {
  // console.log(name_url)
  document.getElementById('name_for_url').innerHTML = name_url
  document.getElementById("tab1").className = "highlight";
  // document.getElementById("tab2").className = "none";
  // document.getElementById("header").innerHTML = "Crafts";
  document.getElementById("toChange").innerHTML =
    document.getElementById("page1").innerHTML
}
//What happens when you click on tab 2:
function highlight2() {
  document.getElementById("tab2").className = "highlight";
  // document.getElementById("tab1").className = "none";
  // document.getElementById("header").innerHTML = "News page";
  document.getElementById("toChange").innerHTML =
  document.getElementById("page2").innerHTML
  

}


//end 













//modal for image

// Modal Setup
var modal = document.getElementById('modal');

var modalClose = document.getElementById('modal-close');
modalClose.addEventListener('click', function() { 
  modal.style.display = "none";
});

// global handler
document.addEventListener('click', function (e) { 
  if (e.target.className.indexOf('modal-target') !== -1) {
      var img = e.target;
      var modalImg = document.getElementById("modal-content");
      var captionText = document.getElementById("modal-caption");
      modal.style.display = "block";
      modalImg.src = img.src;
      captionText.innerHTML = img.alt;
   }
});


//modal for image end






// modal

// Get all links that start with #modal
const modalLinks = document.querySelectorAll('a[href^="#modal"]');

modalLinks.forEach(function (modalLink, index) {
  // Get modal ID to match the modal
  const modalId = modalLink.getAttribute('href');
  
  // Click on link
  modalLink.addEventListener('click', function (event) {
    
    // Get modal element
    const modal = document.querySelector(modalId);
    // If modal with an ID exists
    if(modal){
      // Get close button
      const closeBtn = modal.querySelector('.dialog__close');
      const closeBtn2 = modal.querySelector('.dialog__close2');

      event.preventDefault();
      modal.showModal(); // Open modal
      
      // Close modal on click
      closeBtn.addEventListener('click', function (event) {
        modal.close();
      });

      closeBtn2.addEventListener('click', function (event){
        modal.close();
      });
      
      // Close modal when clicking outside modal
      document.addEventListener('click', function (event) {
        
        const dialogEl = event.target.tagName;
        const dialogElId = event.target.getAttribute('id');
        if(dialogEl == 'DIALOG'){
          // Close modal
          modal.close();
        }
      }, false);
      
    // If modal ID not exists
    } else {
      console.log('Modal doesn\'t exist');
    }
  });
});

// /modal stop

// / modalfo ading imgs

// Get all links that start with #modal
const modalLinks2 = document.querySelectorAll('a[href^="#modal3"]');

modalLinks2.forEach(function (modalLink, index) {
  // Get modal ID to match the modal
  const modalId = modalLink.getAttribute('href');
  
  // Click on link
  modalLink.addEventListener('click', function (event) {

    // a = document.getElementById('name_for_url');
    // a.innerHTML = "yay"
    // a.style.display = 'block';
    // console.log(a)



    // Get modal element
    const modal = document.querySelector(modalId);
    // If modal with an ID exists
    if(modal){
     




      // Get close button
      const closeBtn = modal.querySelector('.dialog__close');


      event.preventDefault();
      modal.showModal(); // Open modal
      
      // Close modal on click
      closeBtn.addEventListener('click', function (event) {
        modal.close();
      });

      
      // Close modal when clicking outside modal
      document.addEventListener('click', function (event) {
        
        const dialogEl = event.target.tagName;
        const dialogElId = event.target.getAttribute('id');
        if(dialogEl == 'DIALOG'){
          // Close modal
          modal.close();
        }
      }, false);
      
    // If modal ID not exists
    } else {
      console.log('Modal doesn\'t exist');
    }
  });
});

// /modal stop






// to stop the browser from resubmit
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }
  
  elements = document.getElementsByName("fadeOut")
  
  setTimeout(function() {
    $('div[name=fadeOut]').fadeOut('fast');
  }, 20000);




// index.html , file rename 
// const paragraph = document.getElementById("edit");
o = document.getElementsByClassName("end-btn")
for (var i = 0; i < o.length; i++) {
  o[i].style.display = "none"
}


var orignal_para;

function MakeEditable(id) {
  orignal_para = document.getElementById(id).innerHTML;
  var paragraph = document.getElementById(id);

  paragraph.contentEditable = true;
  paragraph.style.backgroundColor = "#222222";
  paragraph.focus();

  myArray = id.split("-");

  id_no = myArray[1]
  //   console.log(id_no)
  edit_id = "edit-button-" + id_no
  end_id = "end-button-" + id_no
  document.getElementById(end_id).style.display = "inline-block";
  document.getElementById(edit_id).style.display = "none";
};

function StopEditable(id) {
  var paragraph = document.getElementById(id);
  paragraph.contentEditable = false;
  paragraph.style.backgroundColor = "#333333";
  para = document.getElementById("paragraph")
  console.log(paragraph.innerHTML)




  id_no = myArray[1]
  console.log(id_no)
  edit_id = "edit-button-" + id_no
  end_id = "end-button-" + id_no
  document.getElementById(edit_id).style.display = "inline-block";
  document.getElementById(end_id).style.display = "none";


  input1 = paragraph.innerHTML
  input2 = orignal_para



  $.ajax({
    data: {
      input1: input1,
      input2: input2
    },
    type: 'POST',
    url: '/edit_name'
  })
.done(function (data) {
  if (data.error){
    document.getElementById('error').style.display = "block";
    document.getElementById('error').innerHTML = data.error
    console.log(orignal_para)
    paragraph.innerHTML = orignal_para
  }

  

})};



elements = document.getElementsByClassName("edits");

for (var i = 0; i < elements.length; i++) {
  elements[i].addEventListener('keypress', (evt) => {
    if (evt.which === 13) {
      evt.preventDefault();
    }
  })
};

// delete_name
var f 
var id_no
function open_delete(id){
  myArray = id.split("-");
  id_no = myArray[1]
  f = document.getElementById(id).innerHTML
  document.getElementById("stuff").innerHTML  = "You Sure you want to delete " + '<b>'+ f + '</b>' 

}
// file delete
function delete_name(){
  $.ajax({
    data: {
      delete_input: f
    },
    type: 'POST',
    url: '/delete_name'
  })
.done(function (data) {
 if (data.success === true){
  e_id = "f-"+id_no
  console.log(e_id)
  document.getElementById(e_id).remove()
}
})};


function delete_img(id){
  console.log("delete img")
  var img_del = document.getElementById(id)
  lis = id.split("-")
  row_no = lis[1]
  img_no = lis[2] - 1

  console.log(row_no,img_no)

  $.ajax({
    data: {
      row_no: row_no,
      img_no: img_no
    },
    type: 'POST',
    url: '/del_img'
  })
.done(function (data) {
 if (data.success === true){
  console.log("success");
  img_no = img_no + 1
  o = 'I-'+row_no+'-'+img_no
  // console.log(o)
  document.getElementById(o).remove()
}})


}

$(function(){
  var keyStop = {
    8: ":not(input:text, textarea, input:file, input:password)", // stop backspace = back
    13: "input:text, input:password", // stop enter = submit 
 
    end: null
  };
  $(document).bind("keydown", function(event){
   var selector = keyStop[event.which];
 
   if(selector !== undefined && $(event.target).is(selector)) {
       event.preventDefault(); //stop event
   }
   return true;
  });
 });


// on add click
$('#add').click(function(){
// $('[name="thumbnail"]').on('change', function() {
  p = document.getElementById('url').value
  document.getElementById('url-error').style.display = 'none';
  console.log(p)

  a = $('img.preview').prop('src', p);
  document.getElementById('url-submit').style.display = 'block';
  console.log(a)
// });


});


// some stuff for modal of adding image
function do_stuff(name){
  document.getElementById('name_for_url').innerHTML = name
  document.getElementById('name_for_url2').innerHTML = name
  name_url = name
  document.getElementById('name-url').value = name
  document.getElementById('name-url2').value = name

}


     function readURL(input) {
            if (input.files && input.files[0]) {
              document.getElementById('url-submit').style.display = 'inline-block';
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#blah')
                        .attr('src', e.target.result);
                };

                reader.readAsDataURL(input.files[0]);
            }
        }