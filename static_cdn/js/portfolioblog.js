$(document).ready(function(){
    console.log('ready')
    var searchForm = $('.search-form')
    console.log(searchForm)
      var searchInput = searchForm.find("[name='q']") // input  name='q'
      var typingTimer;
      var typingInterval = 1000
      var searchBtn = searchForm.find("[type='submit']")
      console.log(searchBtn)
      searchInput.keyup(function(event){
          console.log('pressed')
        // released
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
      })
      searchInput.keydown(function(event){
        console.log('pressed')
        // pressed
        clearTimeout(typingTimer)
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
})