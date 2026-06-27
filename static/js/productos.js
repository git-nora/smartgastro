// SmartGastro - JS Productos
// Operación asíncrona con fetch() para alta de productos sin recargar la página
// Hernández Andrés

function mostrarFormulario() {
    document.getElementById("formulario-nuevo").style.display = "block";
}

function ocultarFormulario() {
    document.getElementById("formulario-nuevo").style.display = "none";
    document.getElementById("mensaje-resultado").textContent = "";
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("stock").value = "";
}

async function guardarProducto() {
    const nombre = document.getElementById("nombre").value.trim();
    const precio = document.getElementById("precio").value;
    const stock = document.getElementById("stock").value;
    const categoria = document.getElementById("categoria").value;
    const mensaje = document.getElementById("mensaje-resultado");

    // Validaciones en el frontend
    if (!nombre) {
        mensaje.textContent = "El nombre es obligatorio.";
        mensaje.style.color = "red";
        return;
    }

    if (!precio || parseFloat(precio) < 0) {
        mensaje.textContent = "El precio debe ser mayor o igual a 0.";
        mensaje.style.color = "red";
        return;
    }

    // Obtener el token de la sesión
    const token = obtenerToken();

    try {
        const respuesta = await fetch("/api/productos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                nombre: nombre,
                precio: parseFloat(precio),
                stock: parseInt(stock) || 0,
                categoria: categoria
            })
        });

        const datos = await respuesta.json();

        if (respuesta.ok) {
            mensaje.textContent = "✓ Producto guardado correctamente.";
            mensaje.style.color = "green";

            // Agregar la fila a la tabla sin recargar la página
            const tbody = document.querySelector(".tabla tbody");
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${nombre}</td>
                <td>$${parseFloat(precio).toFixed(2)}</td>
                <td>${parseInt(stock) || 0}</td>
                <td>${categoria}</td>
                <td><span class="badge badge-ok">OK</span></td>
            `;
            tbody.appendChild(fila);

            // Limpiar el formulario después de 2 segundos
            setTimeout(() => {
                ocultarFormulario();
            }, 2000);

        } else {
            mensaje.textContent = "Error: " + (datos.error || "No se pudo guardar el producto.");
            mensaje.style.color = "red";
        }

    } catch (error) {
        mensaje.textContent = "Error de conexión con el servidor.";
        mensaje.style.color = "red";
    }
}