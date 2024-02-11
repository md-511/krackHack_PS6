window.addEventListener('DOMContentLoaded', ()=>{
    let pos = document.getElementById('pos');
    let c = document.getElementById('changeable');
    let con = document.querySelector('.container');
    let id = "c_mem";
    let flag = false;
    pos.addEventListener('change', (e)=>{
        id = e.target.value;
        if ( e.target.value == 's_fa') {
            let str = `<input type="text" id="society" required placeholder="Society">`;
            c.innerHTML += str;
            con.style.height = '600px';
            flag = true;
        } else if (flag == true) {
            con.style.height = '550px';
            c.innerHTML = c.innerHTML.slice(0, c.innerHTML.length - 63);
            flag = false;
        }
    });
});