$("#tag-add").click(function(){	
	addTag();
});

$("#scrub-bar").change(function(){    
    $("#tag-new-time").val(secToHMS(this.value));    
});

$("#finish").click(function(){    
    console.log(JSON.stringify(tags));  
});

var tags = [];

function addTag(){
    var tag = {};
    tag.time = parseInt($("#scrub-bar").val());
    tag.title = $("#tag-new-title").val();
    tag.artist = $("#tag-new-artist").val();
    tag.links = $("#tag-new-links").val();
    clearNewTagErrors();
    if(validate(tag)){       
        tags.push(tag);
        clearNewTagData();
        tags.sort(compareTags);
        displayTags(); 
    }
}

function validate(tag){
    var isValid = true;
   
    for(i = 0; i < tags.length; i++) {  
        if(tag.time === tags[i].time){
            $("#tag-new-time").addClass("is-invalid");
            isValid = false;
        }
    }
    
    if(tag.title === ""){
        $("#tag-new-title").addClass("is-invalid");
        isValid = false;
    }
    
    if(tag.artist === ""){
        $("#tag-new-artist").addClass("is-invalid");
        isValid = false;
    }
    
    if(tag.links === ""){ //TODO: validate with url patterns
        $("#tag-new-links").addClass("is-invalid");
        isValid = false;
    }
    
    return isValid;
}

function displayTags(){
	$("#tags").html("");
        
    for(i = 0; i < tags.length; i++) {  
        tag = tags[i];
        newhtml = $("#tag-new").html();
        //newid = uniqueID();
        //newhtml = newhtml.replace("¶id", newid);
        newhtml = newhtml.replace("¶id", "tag" + i);        
        newhtml = newhtml.replace("¶startTime", secToHMS(tag.time));
        newhtml = newhtml.replace("¶title", tag.title);
        newhtml = newhtml.replace("¶artist", tag.artist);
        newhtml = newhtml.replace("¶links", tag.links);
        $("#tags").append(newhtml);	
	}
    
	$(".tag-remove").click(function() {
		var par = $(this).parent().parent();        
        var i = parseInt(par.attr("id").substr(3,3));
        tags.splice(i,1);
        displayTags();
        //par.remove();
	});
    
    $(".tag-edit").click(function() {
        var par = $(this).parent().parent();        
        var i = parseInt(par.attr("id").substr(3,3));       
        $("#scrub-bar").val(tags[i].time);
        $("#scrub-bar").change();    
        $("#tag-new-title").val(tags[i].title);    
        $("#tag-new-artist").val(tags[i].artist);    
        $("#tag-new-links").val(tags[i].links);
        tags.splice(i,1);
        displayTags();
	});
}

function clearNewTagErrors(){
    $("#tag-new-time").removeClass("is-invalid");
    $("#tag-new-title").removeClass("is-invalid");
    $("#tag-new-artist").removeClass("is-invalid");
    $("#tag-new-links").removeClass("is-invalid");
}

function clearNewTagData(){
    $("#scrub-bar").val(parseInt($("#scrub-bar").val()) + 1);
    $("#scrub-bar").change();    
    $("#tag-new-title").val("");    
    $("#tag-new-artist").val("");    
    $("#tag-new-links").val("");    
}

function secToHMS(seconds){
    var time = new Date(null);
    time.setSeconds(seconds);
    return time.toISOString().substr(11, 8);
}

function HMSToSec(HMS){ 
    var split = HMS.split(':');
    return (+split[0])*3600 + (+split[1])*60 + (+split[2]);  
}

function compareTags(a, b){
    if(a.time < b.time)
        return -1;
    else
        return 1;
}

