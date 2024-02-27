var thRender = null ;
var thPromises = null ;
// var audioObjectURL = null ;
var blob_current = null ;
var blob_next = null ;
var blob_prev = null ;

var fetched_capture = false ;
var fetched_analysis = false ;

function recomputeAudioUrl(program_offset=0) {
    let pattern = document.getElementById("midiPattern")
    let audio = document.getElementById('soundtone_audio')
    let audio_wav_mimes = ['audio/vnd.wav','audio/vnd.wave','audio/wave','audio/x-pn-wav','audio/x-wav']
    for(let i=0 ; i<audio_wav_mimes.length ; i++) {
        if(audio.canPlayType(audio_wav_mimes[i]))
            return AUDIO_URL_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program+program_offset}&ptn=${pattern.value}&f=wav&mt=${audio_wav_mimes[i]}`
    }
    if(audio.CanPlayType('audio/pcm'))
        return AUDIO_URL_BASE + `bm=${bank_msb}&bl=${bank_lsb}&p=${program+program_offset}&ptn=${pattern.value}&f=pcm`
    else
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
    //audioEle.load()
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
    if(fetched_analysis===true)
        return Promise.resolve();
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
        fetched_analysis = true
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });    
}

function captureSoundtoneGUI() {
    if(fetched_capture===true)
        return Promise.resolve() ;
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
            fetched_capture = true 
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

function fetchSound(timeout,with_extras) {
    _clearThRender()
    thRender = setTimeout( ()=>_fetchAll(with_extras) , timeout )
}

function promiseState(p) {
    const t = {};
    return Promise.race([p, t])
      .then(v => (v === t)? "pending" : "fulfilled", () => "rejected");
}

function _closeModalPromise() {
    return new Promise((resolve, reject) => {
        modalClose();
        resolve();
    }) ;
}

async function _fetchAll(with_extras=true){
    // mark existing promises as aborted
    if(thPromises!==null) {
        for(let i=0 ; i<thPromises.length ; i++) {
            thPromises[i].aborted = true // soft abort
        }
        let printed=false
        for(let i=0 ; i<thPromises.length ; i++) {
            let state = await promiseState(thPromises[i].promise)
            while( state==="pending" ) {
                if(!printed){
                    console.log("Waiting for existing request to terminate")
                    printed=true
                }
                await new Promise(r => setTimeout(r, 100));
                state = await promiseState(thPromises[i].promise)
            }
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
        { func : _closeModalPromise , aborted: false } ,
        ...extras ,
        { func : _renderAudio , aborted: false , args: [ +1 ]} ,
        { func : _renderAudio , aborted: false , args: [ -1 ]} ,
    ]
    thPromises = funcs
    let current_promise = Promise.resolve()
    for(let i=0 ; i<funcs.length ; i++) {
        current_promise = current_promise.then( (result) => {
            if(funcs[i].aborted === true) {
                console.log('request has been aborted')
                return null ;
            } if(typeof  funcs[i].args !== "undefined")
                return funcs[i].func(...funcs[i].args)
            else
                return funcs[i].func()
        })
        funcs[i].promise = current_promise 
    }
    // current_promise.then( ()=>{
    //     thPromises = null ;
    // })
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
    fetched_capture = false ;
    fetched_analysis = false ;
    
    const {
        host, hostname, href, origin, pathname, port, protocol, search
    } = window.location
    let form = document.querySelector('#soundtone_form');
    let data = new FormData(form);
    let pattern = document.getElementById("midiPattern")

    let tagsData = serializeTokenfield(tokenfieldTags)
    data.append('tags',JSON.stringify(tagsData))

    let data_get = { 
        'p' : program ,
        'bm' : bank_msb ,
        'bl' : bank_lsb ,
        'c' : document.getElementById('id_category').value ,
        'ptn' : pattern.value
    }
    let queryString = new URLSearchParams(data_get).toString();
    let form_url = pathname + '?' + queryString ;

    if(method==='GET') {
        return fetch(form_url,{
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
    } else {
        return fetch(form_url,{
            method: method ,
            body: data ,
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
            if(json.error === null)
                nextSound()
            else
                console.error('There was a problem with the fetch operation:', json.error);
        })
        .catch(error => {
            // Handle any errors here
            console.error('There was a problem with the fetch operation:', error);
        });        
    }

}

function onFormSubmit(event) {
    event.preventDefault();
    event.stopPropagation();
    submitForm(method='POST')
    reloadTags();
    return false ;
}

function onSoundToneLoaded(){
    if(category!==null)
        selectCategory(category) ;

    fetchSound(400,true)

    document.addEventListener("keydown",onKeyPress);

    document.querySelectorAll('.midi_editable_input').forEach( (ele) => {
        ele.addEventListener('click',autoSelectInput)
        
    }) ;
    document.getElementById('bank_msb').addEventListener('change', ()=> {bank_msb=parseInt(document.getElementById('bank_msb').value);resetBlobs();submitForm()})
    if(document.getElementById('bank_lsb')) document.getElementById('bank_lsb').addEventListener('change', ()=> {bank_lsb=parseInt(document.getElementById('bank_lsb').value);resetBlobs();submitForm()})
    document.getElementById('program').addEventListener('change', ()=> {program=parseInt(document.getElementById('program').value);resetBlobs();submitForm()})

    document.getElementById('soundtone_capture').src = "";
    hideSoundtoneCapture() ;

    document.querySelector('#soundtone_form').addEventListener('submit',onFormSubmit)

    modalOpen(false);
    addTokenfieldToTagsInput()
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

var tokenfieldTags 

function addTokenfieldToTagsInput() {
    tokenfieldTags = new Tokenfield({
        el: document.querySelector('#div_id_tags textarea'), // Attach Tokenfield to the input element with class "text-input"
//        items: [{id: 1, name: 'JavaScript'}, {id: 2, name:'HTML'}, {id: 3, name: 'CSS'}, {id: 4, name: 'Angular'}, {id: 5, name: 'React'}, {id: 6, name: 'Vue'}],
        addItemOnBlur: true,
        addItemsOnPaste: true,
        minChars: 0,
        maxSuggestWindow: 5,
        singleInput: true,
        singleInputValue: 'name',
        remote: {
            url: TAG_SEARCH_URL
        }
    });

    let tagsEle = document.getElementById('soundtone_form').tags
    if(tagsEle.innerText) {
        let tagsArr = JSON.parse(tagsEle.innerText )
        let itemsArr = []
        for(let i=0 ; i<tagsArr.length ; i++)
            itemsArr.push({name:tagsArr[i].name,id:tagsArr[i].id})
        tokenfieldTags.addItems( itemsArr  )
    }
}

function selectTag(tagId,tagName) {
    let item = {
        id:tagId ,
        name:tagName
    }
    tokenfieldTags.addItems(item)
}

function serializeTokenfield(tokenfield) {
    var items = tokenfield.getItems();
    console.log(items);
    var prop;
    var data=[];
    // items.forEach(function(item) {
    //     data.push(item.name)
    // })
    var data = {};
    items.forEach(function(item) {
      if (item.isNew) {
        prop = 'items';//tokenfield._options.newItemName;
      } else {
        prop = 'items';//tokenfield._options.itemName;
      }
      if (typeof data[prop] === 'undefined') {
        data[prop] = [];
      }
      if (item.isNew) {
        //data[prop].push(item.name);
        data[prop].push({name:item.name});
      } else {
        //data[prop].push(item[tokenfield._options.itemValue]);
        data[prop].push({id:item[tokenfield._options.itemValue],name:item.name});
      }
    });
    return data;
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


function reloadTags() {
    return fetch(TAGS_URL,{
        method: 'GET' ,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
    }).then( (response) =>{
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response.text(); // Parse the response body as TEXT
    })
    .then(data => {
        let div = document.getElementById('tags')
        div.innerHTML = data 
    })
    .catch(error => {
        // Handle any errors here
        console.error('There was a problem with the fetch operation:', error);
    });    
}