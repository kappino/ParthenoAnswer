const toggle =  document.getElementById('toggleDark');
const body = document.querySelector('body');

toggle.addEventListener('click', function(){
    this.classList.toggle('bi-toggle-on');
    if(this.classList.toggle('bi-toggle-off')){
        body.style.background = "rgb(40, 67, 208)";
        body.style.color = 'black';
        body.style.transition = '1s';
    }else{
        body.style.background = '#242526';
        body.style.transition = '1s';
    }
})