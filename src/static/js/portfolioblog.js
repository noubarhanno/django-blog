$(document).ready(function(){

    var searchForm = $('.search-form')
      var searchInput = searchForm.find("[name='q']")
      // var authorLink = $('.post__list--span')
      var typingTimer;
      var typingInterval = 1000
      var searchBtn = searchForm.find("[type='submit']")

      searchInput.keyup(function(event){
        // released
        clearTimeout(typingTimer);
        typingTimer = setTimeout(performSearch, typingInterval);
      })

      searchInput.keydown(function(event){
        // pressed
        clearTimeout(typingTimer);
      })

      searchBtn.click(function(event){
        event.preventDefault();
        performSearch();
      })

      function displaySearch(){
        searchBtn.addClass="disabled"
        searchBtn.html("<i class= 'fa fa-spin fa-spinner'></i> Searching ...")
      }

      function performSearch(){
        displaySearch()
        var query = searchInput.val()
        setTimeout(function(){
          window.location.href='/posts/list?q=' + query
        },100)
      }

      // authorLink.click(function(event){
      //   event.preventDefault();
      //   var query = $(this).children('span').text();
      //   window.location.href='/posts/list?q=' + query
      // })
})

function readURL(input,event) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function (e) {
      $('.image-upload-wrap').hide();

      // $('.file-upload-image').attr('src', e.target.result);
      $('.file-upload-content').css({
        'background-image':'url('+e.target.result+')',
        'background-size':'cover',
        'height':'200px',
        'background-position':'50% 20%',
        'transition':'all .4s ease',
        'background-repeat':'no-repeat'
      });
      $('.file-upload-content').show();

      $('.image-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function removeUpload() {
  input = $('.file-upload-input')
  input.replaceWith(input.val('').clone(true));
  // input.replaceWith(input.clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}
$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});

$('.file-upload-content').click(function(){
  removeUpload();
})

$('.file-upload-content').mouseenter(function(){
  $('.image-title').css('display','block');
  $('.fa-trash-alt').css('display','block');
  $('.file-upload-content').css('opacity','0.6');
})

$('.file-upload-content').mouseleave(function(){
  $('.image-title').css('display','none');
  $('.fa-trash-alt').css('display','none');
  $('.file-upload-content').css('opacity','1');
})