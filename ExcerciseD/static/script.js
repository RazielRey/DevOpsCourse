document.getElementById("form").addEventListener("submit", function(event) {
    console.log('Page is loaded!');

    const OriginalDeg = document.querySelector('input[name="original_deg"]');
   
    if (OriginalDeg.value < 0 || OriginalDeg.value > 100) {
        event.preventDefault();
        alert('Invalid Tempature');
    }

});