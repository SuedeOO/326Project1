let file = document.getElementById("audioFile");
let trackTimestamps = document.getElementsByClassName('track-time');
let reversePlaylist = playlist.slice().reverse(); // useful for current track
var currentSong = null;
var hasClickedPlay = false;

for (var i = 0; i < trackTimestamps.length; i++) {
    trackTimestamps[i].onclick = (aTag) => {
        let seconds = parseInt(aTag.target.dataset.time);
        file.currentTime = seconds;
    }
}

let recordListen = () => {
    fetch('/mix/'+ mixId +'/addrecentPlayed', {
        method:'POST',
        credentials: "same-origin",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
        }
    });
}

let togglePlay = (button) => {
    if (file.paused) {
        file.play();
        if(!hasClickedPlay){
            hasClickedPlay = true;
            recordListen();
        }
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
    updateNowPlaying(timestamp);
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
    progressBar.style.width = pct + "%";
}

let linkToButtonMapper = (link) => {
    let elem = document.createElement('a');
    elem.href = link.url;
    elem.target = "_blank";
    elem.className = "btn btn-sm mx-1 ";
    switch (link.provider) {
        case "SOUNDCLOUD":
            elem.className += "btn-soundcloud";
            elem.innerHTML = "SoundCloud";
            break;
        case "SPOTIFY":
            elem.className += "btn-spotify";
            elem.innerHTML = "Spotify";
            break;
        case "APPLEMUSIC":
            elem.className += "btn-apple-music";
            elem.innerHTML = "Apple Music";
            break;
        case "YOUTUBE":
            elem.className += "btn-youtube";
            elem.innerHTML = "YouTube";
            break;
        default:
            break;
    }
    return elem;
}

let updateNowPlaying = (timestamp) => {
    let newSong = reversePlaylist.find((track) => timestamp >= track.time);
    if (newSong != currentSong) {
        if (currentSong != null) {
            document.querySelector("[data-id='" + currentSong.id + "']").classList.remove('border-success', 'text-success', 'box-shadow');
        }
        currentSong = newSong;
        document.getElementById('now-playing-title').innerHTML = currentSong.title;
        document.getElementById('now-playing-artist').innerHTML = currentSong.artist;
        let linksDiv = document.getElementById('now-playing-links');
        linksDiv.innerHTML = '';
        currentSong.links.map(linkToButtonMapper).forEach((e) => linksDiv.appendChild(e));
        document.querySelector("[data-id='" + currentSong.id + "']").classList.add('border-success', 'text-success', 'box-shadow');
    }
}
