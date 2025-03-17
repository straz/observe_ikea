import { setCookie, getCookie, DATA_COOKIE } from './common.js';

$('#submit').on('click', ()=>{
  const dataHost = $('#data_host').val();
  setCookie(DATA_COOKIE, dataHost, 365);
  $('#response').html(`data host set to <tt>${dataHost}</tt>`)
})

const cookie = getCookie(DATA_COOKIE);
if (cookie != null){
  $('#data_host').val(cookie)
}


export function login(divId){
  console.log('cookie', cookie)
  return null
}

