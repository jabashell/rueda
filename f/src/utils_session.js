  // Comprobar token 
  export async function checkToken() {
    const token = readToken();
    const apiUrl = import.meta.env.VITE_API_URL;
    if (!token) {
      return false;
    }
    // comprobar el token contra el backend

      let response = await fetch(apiUrl + '/api/token_status', {
              method: 'GET',
              headers: {
                  'Content-Type': 'application/json',
                  "Authorization": token.token_type + " " + token.access_token
              },
          })
          
      if (response.ok) {
          return true;
        } else {
          clearToken();
          clearUser ();
          return false;  // El token es inválido, volver a la pantalla de login
      }
  }
  
  
  // Guardar el token en sessionStorage
  export function saveToken(token) {
    sessionStorage.setItem('authToken', JSON.stringify(token));
  }

  // Limpiar el token del sessionStorage
  export function clearToken() {
    sessionStorage.removeItem('authToken');
  }

  // Leer el token del sessionStorage
  export function readToken() {
    let token = ''
    token = sessionStorage.getItem('authToken');
    return JSON.parse(token)
  }

  // Guardar el usuario en sessionStorage
  export function saveUser(user) {
    sessionStorage.setItem('user', JSON.stringify(user));
  }

  // Limpiar el usuario del sessionStorage
  export function clearUser() {
    sessionStorage.removeItem('user');
  }
  
  // Leer el usuario del sessionStorage
  export function readUser() {
    let user = ''
    user = sessionStorage.getItem('user');
    return JSON.parse(user)
  }

  // Guardar el grupo en sessionStorage
  export function saveGroup(group) {
    sessionStorage.setItem('group', JSON.stringify(group));
  }

  // Leer el grupo del sessionStorage
  export function readGroup() {
    let group = ''
    group = sessionStorage.getItem('group');
    return JSON.parse(group)
  }

  // Limpiar el grupo del sessionStorage
  export function clearGroup() {
    sessionStorage.removeItem('group');
  }
