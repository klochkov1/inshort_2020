/* скрипт по открытию окна для добавление url */
window.onload = function () {
   var modal = document.querySelector(".window");
   var btn = document.querySelector(".btn_modal_window");
   var long_url = document.getElementById('long_url');
   long_url.addEventListener("keydown", function (event) {
      if (event.keyCode === 13) {
         event.preventDefault();
      }
   });   
       /* добавление  ошибки,
         потому что при типе кнопке button пропадает возможность валидации с фронта */
   btn.addEventListener('click', function (e) {
      
      var inp=document.getElementById('long_url');
      if(inp.checkValidity())
      {
       modal.style.display = "block";
       
      }
      else
      {
     
        inp.reportValidity();
        
      }
   })
   $.getJSON("/urls/generate", function (data) {
      $("#short_url").val(data['url'])
   });
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
/* на копирование url */
function copyToClipboard(elem) {
   var element = document.getElementById(elem);
   var new_range = document.createRange();
   new_range.selectNode(element); 
   window.getSelection().addRange(new_range); 
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
