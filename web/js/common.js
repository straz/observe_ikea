export const DATA_COOKIE = 'data_host';

export function sensorsUrl(){
  const host = getCookie(DATA_COOKIE);
  if (host == null){
    return null
  }
  return `${host}/sensors`;
}

export function dataUrl(p){
  const host = getCookie(DATA_COOKIE);  
  if (host == null){
    return null
  }
  return `${host}/data/${p.deviceId}/day/${p.year}/${p.month}/${p.day}`;
}

export function setCookie(key, value, days) {
  let expires = new Date();
  expires.setTime(expires.getTime() + (days*24*60*60*1000));
  const expiration = "expires=" + expires.toUTCString();
  document.cookie = key + "=" + value + ";" + expiration + ";path=/";
}

export function getCookie(key) {
  var cookies = document.cookie.split('; ');
  for (var i = 0; i < cookies.length; i++) {
    var parts = cookies[i].split('=');
    if (decodeURIComponent(parts[0]) === key) {
      return decodeURIComponent(parts[1]);
    }
  }
  return null;
}
