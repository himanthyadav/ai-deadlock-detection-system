var detectBtn = document.getElementById('detectBtn');
if(detectBtn){
    detectBtn.addEventListener('click', async ()=>{
        var graphTextEl = document.getElementById('graph');
        var outputEl = document.getElementById('output');
        var graphText = graphTextEl ? graphTextEl.value : '';
        let graph = {};
        try{ graph = JSON.parse(graphText); }catch(e){ alert('Invalid JSON'); return; }
        const res = await fetch('/detect', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({graph})});
        const data = await res.json();
        if(outputEl) outputEl.innerText = 'Deadlock: ' + data.deadlock;
    });
}

var predictBtn = document.getElementById('predictBtn');
if(predictBtn){
    predictBtn.addEventListener('click', async ()=>{
        var f1El = document.getElementById('f1');
        var f2El = document.getElementById('f2');
        var f3El = document.getElementById('f3');
        var outputEl = document.getElementById('output');
        const f1 = parseInt((f1El && f1El.value) || 0);
        const f2 = parseInt((f2El && f2El.value) || 0);
        const f3 = parseInt((f3El && f3El.value) || 0);
        const res = await fetch('/predict', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({features:[f1,f2,f3]})});
        const data = await res.json();
        if(outputEl) outputEl.innerText = 'Prediction: ' + data.prediction + ' (Prob: ' + data.probability.toFixed(2) + ')';
    });
}
