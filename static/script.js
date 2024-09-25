const toggle =  document.getElementById('toggleDark');
const body = document.querySelector('body');

toggle.addEventListener('click', function(){
    this.classList.toggle('bi-toggle-on');
    if(this.classList.toggle('bi-toggle-off'))
    {
        body.classList.toggle('dark');
        body.style.transition = '2s';
    }else {
        body.classList.toggle('dark');
        body.style.transition = '2s';
    }
})
