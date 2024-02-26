var thRender = null ;
var thPromises = null ;
// var audioObjectURL = null ;
var blob_current = null ;
var blob_next = null ;
var blob_prev = null ;

function recomputeAudioUrl(program_offset=0) {
    let pattern = document.getElementById("midiPattern")
    return AUDIO_URL_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program+program_offset}&ptn=${pattern.value}`
}
function recomputeAudioAnalyzeUrl() {
    let pattern = document.getElementById("midiPattern")
    return AUDIO_ANALYZE_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program}&ptn=${pattern.value}`
}
function recomputeAudioImageCaptureUrl() {
    return AUDIO_CAPTURE_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program}`
}
function _renderAudio(program_offset=0) {
    let audio_url = recomputeAudioUrl(program_offset)
    //let audioSrc = document.getElementById("audioSource")
    //audioSrc.src = audio_url 
    //let audioEle = document.getElementById('soundtone_audio')
    //audioEle.load()
    // if(audioObjectURL!==null) {
    //     URL.revokeObjectURL(audioObjectURL)
    //     audioObjectURL = null ;
    // }
    if(program_offset===0 && blob_current!==null) {
        _renderToAudioElement(blob_current) ;
        return Promise.resolve()
    }
    else if(program_offset===1 && blob_next!==null) {
        return Promise.resolve()
    }
    else if(program_offset===-1 && blob_prev!==null) {
        return Promise.resolve()
    }
    return fetch(audio_url,{
        method: 'GET' ,
    }).then( (response) =>{
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob(); // Parse the response body as JSON
    })
    .then(blob => {
        if(program_offset===0) {
            blob_current = blob ;
            _renderToAudioElement(blob) ;
            // will be obsolete
            // audioObjectURL = URL.createObjectURL(blob); // HAVE TO RESIVE THIS 
            // audioEle.src = audioObjectURL
            // audioEle.play();
        } 
        else if(program_offset===+1) {
            blob_next = blob ;
        }
        else if(program_offset===-1) {
            blob_prev = blob ;
        }
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });       
}
function _renderToAudioElement(blob) {
    let audioEle = document.getElementById('soundtone_audio')
    const reader = new FileReader();
    reader.onloadend = () => {
    audioEle.src = reader.result;
    // autoplay should do its job
    // audioEle.play()
    //     .catch(e => console.error('Error playing the audio:', e));
    };
    reader.readAsDataURL(blob);
}
function setSoundName(name){
    document.getElementById('sound_name').innerHTML = name;
    document.getElementById('id_name').value = name ;
}

function analyzeAudio() {
    let audio_analyze_url = recomputeAudioAnalyzeUrl()    
    return fetch(audio_analyze_url,{
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
        let div = document.getElementById('id_description_tech')
        div.innerHTML = json.description_tech
        setSoundName(json.program_name)
        // now time to also get the UI of the instrument
        //captureSoundtoneGUI()
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });    
}

function captureSoundtoneGUI() {
    let audio_capture_url = recomputeAudioImageCaptureUrl()    
    //document.getElementById('soundtone_capture').src = audio_capture_url ;
    return fetch(audio_capture_url,{
        method: 'GET' ,
    }).then( (response) =>{
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob(); // Parse the response body as JSON
    })
    .then(blob => {
        let img_capture = document.getElementById('soundtone_capture')
        const reader = new FileReader();
        reader.onloadend = () => {
            img_capture.src = reader.result;
        };
        reader.readAsDataURL(blob);    
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });          
}

function onAudioLoaded(event){
    //analyzeAudio();
}

function _clearThRender() {
    if(thRender!==null)
        clearTimeout(thRender)
}

function resetBlobs() {
    blob_current = null ;
    blob_next = null ;
    blob_prev = null ;    
}

function fetchSound(timeout=400,with_extras=true) {
    _clearThRender()
    thRender = setTimeout( ()=>_fetchAll(with_extras) , timeout )
}

function _fetchAll(with_extras=true){
    // mark existing promises as aborted
    if(thPromises!==null) {
        for(let i=0 ; i<thPromises.length ; i++) {
            thPromises[i].aborted = true // soft abort
        }
        thPromises = null ;
    }
    if(with_extras) {
        extras = [
            { func : analyzeAudio , aborted: false } ,
            { func : captureSoundtoneGUI , aborted: false } ,
        ]
    } else {
        extras = []
    }
    funcs = [
        { func : _renderAudio , aborted: false } ,
        ...extras ,
        { func : _renderAudio , aborted: false , args: [ +1 ]} ,
        { func : _renderAudio , aborted: false , args: [ -1 ]} ,
    ]
    thPromises = funcs
    let current_promise = Promise.resolve()
    for(let i=0 ; i<funcs.length ; i++) {
        current_promise = current_promise.then( (result) => {
            if(funcs[i].aborted === true)
                return null ;
            if(typeof  funcs[i].args !== "undefined")
                return funcs[i].func(...funcs[i].args)
            else
                return funcs[i].func()
        })
    }
}

function nextSound() {
    _clearThRender()
    blob_prev = blob_current ;
    blob_current = blob_next ;
    blob_next = null ;
    program++;
    submitForm();
}

function prevSound() {
    _clearThRender()
    blob_next = blob_current ;
    blob_current = blob_prev ;
    blob_prev = null ;
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
        let div = document.getElementById('soundtone_content')
        div.innerHTML = data 
        var scripts = div.getElementsByTagName('script');
        for (var ix = 0; ix < scripts.length; ix++) {
            eval(scripts[ix].text);
        }        
        onSoundToneLoaded()
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });

}

function onSoundToneLoaded(){
    if(category!==null)
        selectCategory(category) ;

    fetchSound(200,true)

    document.addEventListener("keydown",onKeyPress);

    document.querySelectorAll('.midi_editable_input').forEach( (ele) => {
        ele.addEventListener('click',autoSelectInput)
        
    }) ;
    document.getElementById('bank_msb').addEventListener('change', ()=> {bank_msb=parseInt(this.value);resetBlobs();submitForm()})
    if(document.getElementById('bank_lsb')) document.getElementById('bank_lsb').addEventListener('change', ()=> {bank_lsb=parseInt(this.value);resetBlobs();submitForm()})
    document.getElementById('program').addEventListener('change', ()=> {program=parseInt(this.value);resetBlobs();submitForm()})

    document.getElementById('soundtone_capture').src = "";
    hideSoundtoneCapture() ;

}

function hideSoundtoneCapture() {
    document.getElementById('soundtone_interface').classList.add('hidden-dyn') ;
}
function showSoundtoneCapture() {
    document.getElementById('soundtone_interface').classList.remove('hidden-dyn') ;
}
function toggleSoundtoneCapture() {
    document.getElementById('soundtone_interface').classList.toggle('hidden-dyn') ;
}


function onSoundControlLoaded() {
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

    document.getElementById('capture_view_icon').addEventListener("click", toggleSoundtoneCapture) ;

    document.getElementById('soundtone_interface').addEventListener("click", hideSoundtoneCapture) ;
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