let session_user_id = null
let session_user_login = null
let session_user_access_level = 0

export function getVariables() {
  return [session_user_id, session_user_login, session_user_access_level];
}

export function exitVariables() {
  session_user_id = null
  session_user_login = null
  session_user_access_level = 0
}

export function setVariavle(variableName, value) {
  console.log(`variableName = ${variableName}`)
  //
  if (variableName == 'session_user_id') {
    session_user_id = value;
  }
  //
  if (variableName == 'session_user_login') {
    session_user_login = value;
    //
    console.log('Изменено активное имя пользователя');
  }
  //
  if (variableName == 'session_user_access_level') {
    session_user_access_level = value;
  }
}