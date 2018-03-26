$(".tag-add").click(function(){
	$(".tags").html($(".tags").html() + $(".tag-new").html());	
});

$(".tag-remove").click(function() {
    $(this).parent().parent().remove();
});

