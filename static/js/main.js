// SmartGastro - JS general
// Hernández Andrés

// Guarda el token JWT en sessionStorage cuando el usuario inicia sesión
function guardarToken(token) {
    sessionStorage.setItem("sg_token", token);
}

// Recupera el token para usarlo en los fetch()
function obtenerToken() {
    return sessionStorage.getItem("sg_token");
}