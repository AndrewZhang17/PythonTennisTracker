var video;
var curFrame = 0;

window.onload = () => {
    video = document.getElementById("video");
    video.addEventListener("mousedown", function (evt) {
        console.log("Mouse-X: " + (evt.offsetX));
        console.log("Mouse-Y: " + (evt.offsetY));
        evt.preventDefault();
        var pos = {
            frame: curFrame,
            x: evt.offsetX/video.offsetWidth,
            y: evt.offsetY/video.offsetHeight
        }
        $.post('/analysis', {
            "data": JSON.stringify(pos)
        }, (data) => {
            document.getElementById("result").innerHTML = data;
        });
    });
}


window.addEventListener("keypress", function (evt) {
    if (evt.key === ",") { 
        prevFrame();
    } else if (evt.key === ".") {
        nextFrame();
    }
});

function nextFrame() {
    curFrame = Math.min(video.duration * fps, curFrame + 1);
    video.currentTime = curFrame / fps;
    console.log(video.currentTime);
}

function prevFrame() {
    curFrame = Math.max(0, curFrame - 1);
    video.currentTime = curFrame / fps;
    console.log(video.currentTime);
}

function done() {
    $.post('/analysis', {
        "data": 0
    }, (data) => {
        document.getElementById("result").innerHTML = data;
    });
}

