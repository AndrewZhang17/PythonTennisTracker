var video;
const frameTime = 1/30;

window.onload = () => {
    video = document.getElementById('video');
}


window.addEventListener('keypress', function (evt) {
    if (evt.key === ",") { //left arrow
        //one frame back
        video.currentTime = Math.max(0, video.currentTime - frameTime);
        console.log(video.currentTime);
    } else if (evt.key === ".") { //right arrow
        //one frame forward
        //Don't go past the end, otherwise you may get an error
        video.currentTime = Math.min(video.duration, video.currentTime + frameTime);
        console.log(video.currentTime);
    }
});