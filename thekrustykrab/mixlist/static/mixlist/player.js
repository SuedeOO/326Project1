let file = document.getElementById("audioFile");
var isPlaying = false;

let togglePlay = (button) => {
    if (!isPlaying) {
        file.play();
    } else {
        file.pause();
    }
    button.classList.toggle("fa-play");
    button.classList.toggle("fa-pause");
    isPlaying = !isPlaying;
}

file.addEventListener("timeupdate", (timeUpdate) => {
    let timestamp = timeUpdate.timeStamp;
    var seconds = Math.floor(timestamp / 1000);
    let minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;
    document.getElementById("duration").innerHTML = minutes + ":" + seconds
});

