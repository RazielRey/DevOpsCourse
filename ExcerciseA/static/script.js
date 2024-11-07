document.addEventListener('DOMContentLoaded', function() {
    console.log('Page is loaded!');

    const Button = document.querySelector('button');
    const Time = document.getElementById('time');
    const CloseAnswer = document.querySelector('#close-answer');

    Button.addEventListener('click', async function() {
        const response = new Date();
        const data = await fetch('/');
        Time.textContent = `The time is: ${response}`;
        
        Button.style.display = 'none';
        console.log(data);
        Time.style.display = 'block';
    }
    );
});  
