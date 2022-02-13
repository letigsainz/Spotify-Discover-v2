function load() {
    let loader = document.getElementById('loader');
    loader.className = 'ui massive loader inverted active';
    loader.textContent = '';
    document.getElementById('wrap').style.pointerEvents = 'none';
}
