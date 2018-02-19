add_tag_btn = document.getElementById('add-tag');

function addTag(){
	var tags = document.getElementById("upload-tags");
	var new_tag = document.createElement('div');	
	new_tag.setAttribute('class', 'form-group row upload-tag');
	new_tag.innerHTML = document.getElementById("new-tag").innerHTML;
	tags.appendChild(new_tag);
}

function removeTag(){
	
}

