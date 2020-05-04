
window.onload = function () {
   var modal = document.querySelector(".modal");
   var btn = document.querySelector(".btn_modal_window");
   var span = document.querySelector(".close_modal_window");
   var el = document.getElementsByName('long_url');
   var long_url = document.getElementById('long_url');
   var btn_error = document.getElementsByName('long_url')[0];

   long_url.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
         event.preventDefault();
         display_modal_window();
      }
   });   
   btn.addEventListener('click', function (e) {
      
      var inp=document.getElementById('long_url');
      if(inp.checkValidity())
      {
       modal.style.display = "block";
       return false;
      }else{
      
        inp.reportValidity();
         // результат функции валидации
  
      

      }
     
   })

   $.getJSON("/urls/generate", function (data) {
      $("#short_url").val(data['url'])
   });

   span.addEventListener('click', function () {
      modal.style.display = "none";
   })

   window.onclick = function (event) {
      if (event.target == modal) {
         modal.style.display = "none";
      }
   }
   
   //async check url availability
   $('#short_url').keyup(delay(function (e) {
      var $su = $("#short_url");
      var url = "/urls/" + $su.val();
      $.ajax({
         type: "GET",
         url: url,
         data: {},
         success: function (xhr, statusText, err) {
            console.log("sucsess");
            $("#short_url")[0].setCustomValidity("Це скорочення вже зайняте");
         },
         error: function (xhr, statusText, err) {
            console.log("error");
            if (xhr.status == 404) {
               $("#short_url")[0].setCustomValidity("");
            }
         }
      });
   }, 500));
}
function copyToClipboard(elem) {
   var ta = document.getElementById(elem);
   var range = document.createRange();
   range.selectNode(ta); 
   window.getSelection().addRange(range); 
   document.execCommand('copy'); 
   window.getSelection().removeAllRanges();
}

function delay(callback, ms) {
   var timer = 0;
   return function () {
      var context = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () {
         callback.apply(context, args);
      }, ms || 0);
   };
}
