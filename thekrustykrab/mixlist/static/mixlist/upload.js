$("#tag-add").click(function(){	
	addEmptyTag();
});

tags = [];

function uniqueID() {
  return Math.round(new Date().getTime() + (Math.random() * 100));
}

function addEmptyTag(){
	addTag("","","","");
}

function addTag(startTime, title, artist, links){
	newhtml = $("#tag-new").html();
	newid = uniqueID();
	newhtml = newhtml.replace("¶id", newid);
	tags.push(newid);
	newhtml = newhtml.replace("¶startTime", startTime);
	newhtml = newhtml.replace("¶title", title);
	newhtml = newhtml.replace("¶artist", artist);
	newhtml = newhtml.replace("¶links", links);
	$("#tags").append(newhtml);
	setFunctions();
}

function setFunctions(){
	/*
	for(id in tags){		
		id_select = "#" + id;
		//$(id_select + " > div > .tag-up").attr("pid", id_select);
		$(id_select + " > div > .tag-up").click(function() {			
			$(id_select).remove();//.prev().insertAfter($(id_select));			
		});
	}
	*/
	$(".tag-up").click(function(e) {
		tag = $(this).parent().parent();
		tag.prev(".tag").insertAfter(tag);
	});
	
	$(".tag-down").click(function(e) {
		tag = $(this).parent().parent();
		tag.next(".tag").insertBefore(tag);	
	});
	
	$(".tag-remove").click(function() {
		$(this).parent().parent().remove();
	});
}

