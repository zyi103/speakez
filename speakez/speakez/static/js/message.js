let recorder;
let context;
let audio = document.querySelector('audio');
let startBtn = document.querySelector('.js-start');
let stopBtn = document.querySelector('.js-stop');
let audioBlob;

// audio recorder

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


// form submition
$(document).ready(function () {

    // getting csrftoken
    var csrftoken = Cookies.get('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

$('form').submit(function (e) {
    e.preventDefault()

    var xhr = new XMLHttpRequest()
    xhr.open('GET', document.getElementById("audio").src, true)
    xhr.responseType = 'blob'
    xhr.onload = function (e) {
        if (this.status == 200) {
            audioBlob = this.response
            console.log(audioBlob)

            var formData = new FormData();
            formData.append("audio", audioBlob, document.getElementById("id_title").value + '.wav');
            formData.append("title", document.getElementById("id_title").value);
            formData.append("content", document.getElementById("id_content").value);
            formData.append("duration", audio.duration);


            console.log(formData)
            $.ajax({
                url: '/admin/messages',
                data: formData,
                processData: false,
                contentType: false,
                type: 'POST',
                success: function (data) {

                },
                error: function (e) {
                    alert(e.toString())
                }
            });
        } else {
            alert("failed to get audio message")
        }
    };
    xhr.send()
})