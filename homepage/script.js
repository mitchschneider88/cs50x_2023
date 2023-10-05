var track1 = document.getElementById('track1');

var controlBtn = document.getElementById('play-pause');

function playPause() {
    if (track1.paused) {
        track1.play();
        controlBtn.className = "pause";
    } else {
        track1.pause();
        controlBtn.className = "play";
    }
}

controlBtn.addEventListener("click", playPause);
track.addEventListener("ended", function() {
  controlBtn.className = "play";
});
