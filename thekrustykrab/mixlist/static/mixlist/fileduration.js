$('#id_audio_file').on('change', function() {
    var obj = this.files[0];
    var objectUrl = URL.createObjectURL(obj);
    var audio = new Audio(objectUrl);
    setTimeout(function(){ 
        document.getElementById('duration').value =  audio.duration; 
    }, 50);
});
