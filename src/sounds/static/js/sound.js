var thRender = null ;
var AUDIO_URL ;
var AUDIO_ANALYZE ;

function recomputeAudioUrl() {
    let pattern = document.getElementById("midiPattern")
    AUDIO_URL = AUDIO_URL_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program}&ptn=${pattern.value}`
}
function recomputeAudioAnalyzeUrl() {
    let pattern = document.getElementById("midiPattern")
    AUDIO_ANALYZE = AUDIO_ANALYZE_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program}&ptn=${pattern.value}`
}
function _renderAudio() {
    recomputeAudioUrl()
    let audioSrc = document.getElementById("audioSource")
    audioSrc.src = AUDIO_URL 
    let audioEle = document.getElementById('soundtone_audio')
    audioEle.load()
}

function analyzeAudio() {
    recomputeAudioAnalyzeUrl()    
    fetch(AUDIO_ANALYZE,{
        method: 'GET' ,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        // signal: controller.signal
    }).then( (response) =>{
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the response body as JSON
    })
    .then(json => {
        let div = document.getElementById('id_autogen')
        div.innerHTML = json.autogen
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });    
}

function onAudioLoaded(event){
    analyzeAudio();
}

function _clearThRender() {
    if(thRender!==null)
        clearTimeout(thRender)
}

function renderAudio() {
    _clearThRender()
    thRender = setTimeout( _renderAudio , 200 )
}

function nextSound() {
    _clearThRender()
    program++;
    submitForm();
}

function prevSound() {
    _clearThRender()
    program--;
    submitForm();
}

function selectCategory(catval) {
    document.getElementById('id_category').value = catval;
}

var controller = null ;

function submitForm( method='GET' ) {

    // if(controller!==null) 
    //     controller.abort();
    // controller = new AbortController();
    
    const {
        host, hostname, href, origin, pathname, port, protocol, search
    } = window.location
    let form = document.querySelector('#soundtone_form');
    let data = new FormData(form);
    let pattern = document.getElementById("midiPattern")

    let data_get = { 
        'p' : program ,
        'bm' : bank_msb ,
        'bl' : bank_lsb ,
        'c' : document.getElementById('id_category').value ,
        'ptn' : pattern.value
    }
    let queryString = new URLSearchParams(data_get).toString();
    let form_url = pathname + '?' + queryString ;

    fetch(form_url,{
        method: method ,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        // signal: controller.signal
    }).then( (response) =>{
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text(); // Parse the response body as JSON
    })
    .then(data => {
        // Handle the parsed data here
        //console.log(data);
        let div = document.getElementById('soundtone_content')
        div.innerHTML = data 
        var scripts = div.getElementsByTagName('script');
        for (var ix = 0; ix < scripts.length; ix++) {
            eval(scripts[ix].text);
        }        
        onSoundToneLoaded(true)
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });

}

function onSoundToneLoaded(with_render=false){
    if(category!==null)
        selectCategory(category) ;

    if(with_render===true)
        renderAudio()

    document.addEventListener("keydown",onKeyPress);

    document.querySelectorAll('.midi_editable_input').forEach( (ele) => {
        ele.addEventListener('click',autoSelectInput)
    }) ;

}

function onSoundControlLoaded(with_render=false) {
        // let audio = document.querySelector('audio')
    // let source = document.getElementById('audioSource');
    // source.src = "{% url 'sounds:render_sound' srcid=source.id %}?b={{bank}}&p={{program}}&r={% random_uuid %}"
    // audio.load(); //call this to just preload the audio without playing
    // audio.play(); //call this to play the song right away});    
    document.querySelectorAll('.prevsound').forEach( (ele) => {
        ele.addEventListener('click',prevSound)
    }) ;
    document.querySelectorAll('.nextsound').forEach( (ele) => {
        ele.addEventListener('click',nextSound)
    }) ;
    document.querySelectorAll('.soundcontrol').forEach( (ele) => {
        ele.addEventListener('click',animateBeat)
    }) ;
    document.getElementById('soundtone_audio').addEventListener("loadeddata", onAudioLoaded );

    if(with_render===true)
        renderAudio()    
} 

function onKeyPress(event) {
    switch(event.key) {
        case 'ArrowRight':
            document.querySelector('.nextsound').dispatchEvent(new CustomEvent('click',{}))
        break
        case 'ArrowLeft':
            document.querySelector('.prevsound').dispatchEvent(new CustomEvent('click',{}))
        break 
    }
}


// The party that performs a cancelable operation
// gets the "signal" object
// and sets the listener to trigger when controller.abort() is called
//signal.addEventListener('abort', () => alert("abort!"));

// The other party, that cancels (at any point later):
//controller.abort(); // abort!
// The event triggers and signal.aborted becomes true
//alert(signal.aborted); // true


function animateBeat(event){
    event.target.classList.add('beat');
    setTimeout( ()=>{event.target.classList.remove('beat')} , 2000);
}

function autoSelectInput(event){
    event.target.select()
}