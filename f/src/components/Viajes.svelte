<script>
    import { Toggle, Dialog, TextField } from 'svelte-ux';
    import { Button } from 'svelte-ux';
    import { onMount } from 'svelte';
    import { readToken, readUser, clearGroup } from '../utils_session.js';
    import SiguienteConductor from './SiguienteConductor.svelte';
    
    const apiUrl = import.meta.env.VITE_API_URL;
    export let grupo = 0;
    export let showSelectGrupo = false;
  
    let data = {};  // Variable reactiva para guardar los datos
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    let datos_viajes = [];  // Variable reactiva para guardar los viajes
    let name = readUser() ;
    let dateValue;
    let viajeSeleccionado = null; // Almacena el viaje seleccionado
    let showSiguienteConductor = true;
    let notas = ''; // Almacena las notas del viaje


    onMount (async function viajes() {
        try {
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
            
            if (response.ok) {
                datos_viajes = await response.json();
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
        } finally {
            cargando = false;
        }
    });

    function actualizar_notas(viajeSeleccionado) {
        fetch(apiUrl + '/api/actualizar_notas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": token.token_type + " " + token.access_token
            },
            body: JSON.stringify({ 
                            "fecha": viajeSeleccionado.fecha,
                            "notas_viaje": viajeSeleccionado.notas_viaje,
                            })
            
        })
        .then(response => response.json())
        .then(() => {
          datos_viajes = datos_viajes
        })
        .catch(error => console.error('Error:', error))

    };

    async function recargaViaje() {
        try {
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
            
            if (response.ok) {
                showSiguienteConductor = false;
                datos_viajes = await response.json();
                showSiguienteConductor = true;
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
        } 
    }
  
    function handleButton () {
      sessionStorage.clear(); 
      location.reload();
    }
    function btn_volver () {
      clearGroup();
      showSelectGrupo = true;
      grupo = 0;
    }
    function handleCustomEvent(event) {
      setTimeout (recargaViaje, 100);
    }

        // Función para mostrar un mensaje al hacer click en una fila
    function mostrarMensaje(viaje, toggle) {
      viajeSeleccionado = viaje;
      toggle ();
    }
    function actualizarViaje(viajeSeleccionado, toggleOff){
      actualizar_notas (viajeSeleccionado);
      toggleOff();
    }

  </script>
  
  <div class="min-h-screen flex flex-col bg-red-100 w-screen lg:max-w-[1024px]">
    <!-- Header -->
    <header class="bg-blue-500 text-white p-4 w-full">
      <h1 class="text-xl">{name}</h1>
    </header>
  
    <!-- Parte central que ocupa el máximo espacio -->
    <main class="flex-grow bg-gray-100  p-4 w-full">
      {#if cargando} 
      Cargando...
      {:else}
        <div>
          <Toggle let:toggle let:toggleOff let:on={open}>
          <table class="border border-gray-500 table-auto w-full text-blue-500 text-xl">
            <thead>
              <tr>
                <th class="border border-gray-500 px-4 py-2">Fecha</th>
                <th class="border border-gray-500 px-4 py-2">Conductor</th>
                <th class="border border-gray-500 px-4 py-2">Mini</th>
              </tr>
            </thead>
            <tbody>
              {#each datos_viajes as viaje (viaje.fecha)}
              <tr on:click={() => mostrarMensaje(viaje, toggle)} class={viaje.notas_viaje ? "bg-blue-100" : ""}>
                <td class="border border-gray-500 px-4 py-2">{viaje.fecha}</td>
                <td class="border border-gray-500 px-4 py-2">{viaje.nombre_conductor}</td>
                <td class="border border-gray-500 px-4 py-2">{viaje.nombre_conductor_mini}</td>
              </tr>
              {/each}
            </tbody>
          </table>

            <Dialog {open} on:close={toggleOff} persistent>
              <div slot="title">Notas del Viaje</div>
              <div class="p-2">
                {#if viajeSeleccionado}
                  <p><strong>Fecha:</strong> {viajeSeleccionado.fecha}</p>
                  <p><strong>Conductor:</strong> {viajeSeleccionado.nombre_conductor}</p>
                  <div class="p-2">
                    <TextField label="Notas" multiline autofocus bind:value={viajeSeleccionado.notas_viaje} />
                  </div>
                {/if}
              </div>
              <div slot="actions">
                <Button variant="fill" color="primary" on:click={() => actualizarViaje(viajeSeleccionado, toggleOff)}>OK</Button>
                <Button on:click={toggleOff}>Cancel</Button>
              </div>
            </Dialog>
          </Toggle>


        </div>
        <div>
          {#if showSiguienteConductor}
          <SiguienteConductor {grupo} bind:dateValue bind:cargando_ext={cargando} on:renderEvent={handleCustomEvent} />
          {/if}
        </div>

      {/if}
            
    </main>
  
    <!-- Footer -->
    <footer class="flex flex-row justify-evenly bg-blue-500 text-white p-4 w-full">
      <div>
        <Button label="Volver" on:click={btn_volver} className="bg-black-600">Volver</Button>
      </div>
      <div>
        <Button label="Salir" on:click={handleButton} className="bg-black-600">Logout</Button>
      </div>
    </footer>
  </div>
  
<style>

</style>