var thRender = null ;

function _renderAudio() {
    let audioSrc = document.getElementById("audioSource")
    audioSrc.src = audioSrc.getAttribute('data-src') ;
    let audioEle = document.getElementById('soundtone_audio')
    audioEle.load()
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

    let data_get = { 
        'p' : program ,
        'bm' : bank_msb ,
        'bl' : bank_lsb ,
        'c' : category 
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
        document.getElementById('soundtone_content').innerHTML = data ;
        onSoundToneLoaded()
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });

}

function onSoundToneLoaded(){
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

    if(category!==null)
        selectCategory(category) ;

    //renderAudio()
}


// The party that performs a cancelable operation
// gets the "signal" object
// and sets the listener to trigger when controller.abort() is called
//signal.addEventListener('abort', () => alert("abort!"));

// The other party, that cancels (at any point later):
//controller.abort(); // abort!
// The event triggers and signal.aborted becomes true
//alert(signal.aborted); // true