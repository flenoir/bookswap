window.addEventListener('load', function(){
 var opensearchmodal = document.querySelectorAll('.searchmodal-open')
 console.log("found search modal")
 for (var i = 0; i < opensearchmodal.length; i++) {
   opensearchmodal[i].addEventListener('click', function(event){
     event.preventDefault()
     console.log("clicked")
     toggleModal()
   })
 }
 
 const searchoverlay = document.querySelector('.searchmodal-overlay')
 searchoverlay.addEventListener('click', toggleModal)
 
 var closesearchmodal = document.querySelectorAll('.searchmodal-close')
 for (var i = 0; i < closesearchmodal.length; i++) {
   closesearchmodal[i].addEventListener('click', toggleModal)
 }
 
 document.onkeydown = function(evt) {
   evt = evt || window.event
   var isEscape = false
   if ("key" in evt) {
     isEscape = (evt.key === "Escape" || evt.key === "Esc")
   } else {
     isEscape = (evt.keyCode === 27)
   }
   if (isEscape && document.body.classList.contains('searchmodal-active')) {
     toggleModal()
   }
 };
 
 
 function toggleModal () {
   const body = document.querySelector('body')
   const searchmodal = document.querySelector('.searchmodal')
   searchmodal.classList.toggle('opacity-0')
   searchmodal.classList.toggle('pointer-events-none')
   body.classList.toggle('searchmodal-active')
 }

 
})
