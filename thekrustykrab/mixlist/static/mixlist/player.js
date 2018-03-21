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
    let timestamp = timeUpdate.target.currentTime;
    var seconds = Math.floor(timestamp);
    let minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;
    if (seconds < 10) {
        seconds = "0" + seconds;
    }
    document.getElementById("duration").innerHTML = minutes + ":" + seconds
});

