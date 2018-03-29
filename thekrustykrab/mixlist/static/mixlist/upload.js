$("#tag-add").click(function(){
	//$("#tags").html($("#tags").html() + "\n" + $("#tag-new").html());
	$("#tags").append($("#tag-new").html());
	$(".tag-remove").click(function() {
		$(this).parent().parent().remove();
	});
});

$(".tag-remove").click(function() {
    $(this).parent().parent().remove();
});