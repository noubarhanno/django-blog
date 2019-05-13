$(document).ready(function(){
    var content = $('.data')
    content.mouseenter(handlerIn).mouseleave(handlerOut)
    
    function handlerIn(){
        $(this).find('.menu-content').css({'-webkit-transform': 'translateY(-55px)', 'transform': 'translateY(-55px)'});
        
    }

    function handlerOut(){
        $(this).find('.menu-content').css({'-webkit-transform': 'translateY(-0px)', 'transform': 'translateY(-0px)'});
    }
})
