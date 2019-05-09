let recorder;
let context;
let audio = document.querySelector('audio');
let startBtn = document.querySelector('.js-start');
let stopBtn = document.querySelector('.js-stop');

window.URL = window.URL || window.webkitURL;
/** 
 * Detecte the correct AudioContext for the browser 
 * */
window.AudioContext = window.AudioContext || window.webkitAudioContext;
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

let onFail = function (e) {
    alert('Error ' + e);
    console.log('Rejected!', e);
};

let onSuccess = function (s) {
    console.log('Recording...');
    let tracks = s.getTracks();
    startBtn.setAttribute('disabled', true);
    stopBtn.removeAttribute('disabled');
    context = new AudioContext();
    let mediaStreamSource = context.createMediaStreamSource(s);
    recorder = new Recorder(mediaStreamSource);
    recorder.record();

    stopBtn.addEventListener('click', () => {
        console.log('Stop Recording...');
        stopBtn.setAttribute('disabled', true);
        startBtn.removeAttribute('disabled');
        recorder.stop();
        tracks.forEach(track => track.stop());
        recorder.exportWAV(function (s) {
            audio.src = window.URL.createObjectURL(s);
        });
    });
}

startBtn.addEventListener('click', () => {
    if (navigator.getUserMedia) {
        /** 
         * ask permission of the user for use microphone or camera  
         */
        navigator.getUserMedia({ audio: true }, onSuccess, onFail);
    } else {
        console.warn('navigator.getUserMedia not present');
    }
});
