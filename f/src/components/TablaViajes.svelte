<script>
    import { onMount } from 'svelte';
    import { readToken } from '../utils_session.js';
    
    const apiUrl = import.meta.env.VITE_API_URL;
    export let grupo = 0;
  
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    let datos_viajes = [];  // Variable reactiva para guardar los viajes

    onMount (async function viajes() {
        console.log('Onmount...');
        try {
            console.log (({ 'grupo_id' : grupo, 'num_entradas': "3" })            )
            const response = await fetch(apiUrl + '/api/viajes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": token.token_type + " " + token.access_token
                },
                body: JSON.stringify({ 
                                "id_grupo": grupo,
                                "num_entradas": "4"
                                })
            });
            console.log ('Response', response);
            
            if (response.ok) {
                datos_viajes = await response.json();
                console.log('Datos viaje', datos_viajes);
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            cargando = false;
        }
    });
  
</script>

        <table class="border border-gray-500 table-auto w-full text-blue-500 text-xl">
          <thead>
            <tr>
              <th class="border border-gray-500 px-4 py-2">Fecha</th>
              <th class="border border-gray-500 px-4 py-2">Conductor</th>
              <th class="border border-gray-500 px-4 py-2">Mini</th>
            </tr>
          </thead>
          <tbody>
            {#each datos_viajes as viaje}
            <tr>
              <td class="border border-gray-500 px-4 py-2">{viaje.fecha}</td>
              <td class="border border-gray-500 px-4 py-2">{viaje.nombre_conductor}</td>
              <td class="border border-gray-500 px-4 py-2">{viaje.nombre_conductor_mini}</td>
            </tr>
            {/each}
          </tbody>
        </table>
  
  <style>
    
  </style>