$("#tag-add").click(function(){	
	addEmptyTag();
});

function addEmptyTag(){
	addTag("","","","");
}

function addTag(startTime, title, artist, links){
	newhtml = $("#tag-new").html();
	newhtml = newhtml.replace("¶startTime", startTime);
	newhtml = newhtml.replace("¶title", title);
	newhtml = newhtml.replace("¶artist", artist);
	newhtml = newhtml.replace("¶links", links);
	$("#tags").append(newhtml);
	setFunctions();
}

function setFunctions(){
	$(".tag-up").click(function() {
		$(this).parent().parent().prev().insertAfter($(this).parent().parent());			
	});
	
	$(".tag-down").click(function() {
		$(this).parent().parent().next().insertBefore($(this).parent().parent());		
	});
	
	$(".tag-remove").click(function() {
		$(this).parent().parent().remove();
	});
}

