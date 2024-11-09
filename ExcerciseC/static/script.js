document.getElementById("form").addEventListener("submit", function(event) {
    console.log('Page is loaded!');
    
    const UrlInput = document.querySelector('input[name="url"]');
    const Url = UrlInput.value;
    const ValidIds = ['.com', '.net', '.org', '.gov', '.edu'];

    if (!ValidIds.some(id => Url.includes(id))) {
        event.preventDefault();
        alert('Invalid URL');

        
    }
      
});

