<script>
    import { Button } from 'svelte-ux';
    import { onMount } from 'svelte';
    import { readToken, readUser, clearGroup } from '../utils_session.js';
    import SiguienteConductor from './SiguienteConductor.svelte';
    import TablaViajes from './TablaViajes.svelte';
    
    const apiUrl = import.meta.env.VITE_API_URL;
    export let grupo = 0;
    export let showSelectGrupo = false;
  
    let data = {};  // Variable reactiva para guardar los datos
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    let datos_viajes = [];  // Variable reactiva para guardar los viajes
    let name = readUser() ;
    let dateValue;


    onMount (async function viajes() {
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
  
    function handleButton () {
      sessionStorage.clear(); 
      location.reload();
    }
    function btn_volver () {
      clearGroup();
      showSelectGrupo = true;
      grupo = 0;
      console.log('Grupo:', grupo, 'showSelectGrupo', showSelectGrupo);
    }
    function handleCustomEvent(event) {
      console.log(event.detail.message); // 'Hola desde el hijo!'
      cargando = true;
      console.log ('Cargando:', cargando);
      setTimeout(() => {
        cargando = false;
        console.log ('ReCargando:', cargando);
      }, 10);
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
          <TablaViajes {grupo} />
        </div>
        <div>
          <SiguienteConductor {grupo} bind:dateValue bind:cargando_ext={cargando} on:renderEvent={handleCustomEvent} />
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