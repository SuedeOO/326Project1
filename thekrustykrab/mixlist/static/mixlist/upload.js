$("#author").change(function(){    
    displayTags();    
});

$("#desc").on('input propertychange', function(){
    displayTags(); 
});

$("#tag-add").click(function(){	
	addTag();
});

$("#scrub-bar").click(function(){    
    var newTime = this.value;
    $("#tag-new-time").val(secToHMS(newTime));
    file.currentTime = newTime;
    $("#scrub-bar").select();
});

$("#id_json").hide();
$("label[for='id_json']").remove();

var tags = [];

function addTag(){
    var tag = {};
    tag.time = HMSToSec($("#tag-new-time").val());
    tag.title = $("#tag-new-title").val();
    //tag.title = tag.title.replace(/&#39;/g, "\'");
    //tag.title = tag.title.replace(/&#34;/g, "\"");
    //tag.title = tag.title.replace(/&quot;/g, "\"");
    tag.artist = $("#tag-new-artist").val();
    //tag.artist = tag.artist.replace(/&#39;/g, "\'");
    //tag.artist = tag.artist.replace(/&#34;/g, "\"");
    //tag.title = tag.title.replace(/&quot;/g, "\"");
    tag.links = $("#tag-new-links").val().split(" ").filter(function(el) {return el.length != 0});
    
    clearNewTagErrors();
    if(validate(tag)){       
        tags.push(tag);
        clearNewTagData();
        tags.sort(compareTags);
        displayTags(); 
    }
}

function addExistingTag(time, title, artist, links){
    title = title.replace(/&#39;/g, "\'");
    title = title.replace(/&#34;/g, "\"");
    title = title.replace(/&quot;/g, "\"");
    title = title.replace(/&amp;/g, "&");
    artist = artist.replace(/&#39;/g, "\'");
    artist = artist.replace(/&#34;/g, "\"");
    artist = artist.replace(/&quot;/g, "\"");
    artist = artist.replace(/&amp;/g, "&");
    
    var tag = {};
    tag.time = HMSToSec(time);
    tag.title = title;
    tag.artist = artist;
    tag.links = links;
    tags.push(tag);   
}

function validate(tag){
    var isValid = true;
    if(!/[0-9][0-9]:[0-6][0-9]:[0-6][0-9]/.test($("#tag-new-time").val()) || tag.time < 0 || tag.time > $("#scrub-bar").attr("max")){
        $("#tag-new-time").addClass("is-invalid");
        isValid = false;
    }
               
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
    /*
    if(tag.links === ""){ //TODO: validate with url patterns
        $("#tag-new-links").addClass("is-invalid");
        isValid = false;
    }
    */
    return isValid;
}

function displayTags(){
	$("#tags").html("");
        
    for(i = 0; i < tags.length; i++){  
        tag = tags[i];
        newhtml = $("#tag-new").html();
        newhtml = newhtml.replace("¶id", "tag" + i);        
        newhtml = newhtml.replace("¶startTime", secToHMS(tag.time));
        newhtml = newhtml.replace("¶title", tag.title);
        newhtml = newhtml.replace("¶artist", tag.artist);
        
        newhtml = newhtml.replace("¶links", getLinks(tag));
        $("#tags").append(newhtml);	        
	}
    
        var title = $("#title").val();
        var author = $("#author").val();
        var desc = $("#desc").val();
        var mix = {title:title, author:author, tags:tags, desc:desc};
        
        $("#id_json").val(JSON.stringify(mix));
    
	$(".tag-remove").click(function() {
		var par = $(this).parent().parent();        
        var i = parseInt(par.attr("id").substr(3,3));
        tags.splice(i,1);
        displayTags();
	});
    
    $(".tag-edit").click(function() {
        var par = $(this).parent().parent();        
        var i = parseInt(par.attr("id").substr(3,3));       
        $("#scrub-bar").val(tags[i].time);
        $("#tag-new-time").val(secToHMS($("#scrub-bar").val()));   
        $("#tag-new-title").val(tags[i].title);
        $("#tag-new-artist").val(tags[i].artist);    
        $("#tag-new-links").val(getLinks(tags[i]));
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

function getLinks(tag){
    var linksCombined = "";
        for(j = 0; j < tag.links.length; j++){ 
            linksCombined = linksCombined + " " + tag.links[j];
        }
    return linksCombined;
}

function compareTags(a, b){
    if(a.time < b.time)
        return -1;
    else
        return 1;
}


let file = document.getElementById("audioFile");
let togglePlay = (button) => {
    if (file.paused) {
        file.play();
    } else {
        file.pause();
    }
    button.classList.toggle("fa-play");
    button.classList.toggle("fa-pause");
}

file.addEventListener("timeupdate", (timeUpdate) => {
    let totalDuration = file.duration;
    let timestamp = timeUpdate.target.currentTime;
    updateTime(timestamp);
    updateProgressBar(timestamp);
});

let updateTime = (timestamp) => {
    var seconds = Math.floor(timestamp);
    let minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    document.getElementById("duration").innerHTML = minutes + ":" + seconds
}

let updateProgressBar = (timestamp) => {
    let progressBar = document.getElementById("progressBar");
    let pct = 100 * timestamp / file.duration;
    $("#scrub-bar").val(timestamp);
    $("#scrub-bar").change();
    $("#tag-new-time").val(secToHMS($("#scrub-bar").val()));
}