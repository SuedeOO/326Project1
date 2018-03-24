let file = document.getElementById("audioFile");
let progressBar = document.getElementById("progressBar");
let trackTimestamps = document.getElementsByClassName('track-time');

for (var i = 0; i < trackTimestamps.length; i++) {
    trackTimestamps[i].onclick = (aTag) => {
        let seconds = parseInt(aTag.target.parentNode.dataset.time);
        file.currentTime = seconds;
    }
}

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
    let pct = 100 * timestamp / file.duration;
    progressBar.style.width = pct + "%";
}
