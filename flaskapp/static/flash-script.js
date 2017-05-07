$(document).ready(function(){
    setTimeout(function(){$('.flash').fadeOut();}, 5000);
    $(window).click(function(){$('.flash').fadeOut();});
})