function change_action() {
    let a = document.getElementsByName('form');
    let id = document.getElementById('request_id').value;
    let str = `{ url_for('download_pdf', request_id='${id}') }`;
    console.log(`{${str}}`);   
    a.action = `{${str}}`;
}