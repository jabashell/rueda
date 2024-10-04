<script>
    import { onMount } from 'svelte';
    import { readToken, readUser } from '../utils_session.js';
    import { DatePickerField } from 'svelte-ux';
    
    const apiUrl = import.meta.env.VITE_API_URL;
  
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    export let grupo;
    export let dateValue = new Date();
    let datos_conductor;
    import { es } from 'date-fns/locale'; // Importa el idioma español
  
    onMount (async function getSiguienteConductor() {
        try {
            const response = await fetch(apiUrl + '/api/siguiente_conductor/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": token.token_type + " " + token.access_token
                },
                body: JSON.stringify({ 
                                "id_grupo": grupo,
                                })
                
            });
            console.log ('Response', response);
            
            if (response.ok) {
                datos_conductor = await response.json();
                console.log('Datos conductor', datos_conductor);
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
  
  
  <div class="text-blue-500 text-2xl">
      {#if cargando} 
      Cargando...
      {:else}
      <div class="mt-8 flex flex-row space-x-reverse justify-center items-baseline">
      <div class="mr-4">
          Proximo conductor: 
      </div>
        <div class="text-3xl font-bold">
            {datos_conductor.nombre_siguiente_conductor}
        </div>
      </div>
      <div class="flex justify-center mt-4">
        <div class="w-64">
            <DatePickerField
                bind:value={dateValue}
                format="dd/MM/yyyy"
                locale={es}
                firstDayOfWeek={1}
                class="bg-white text-black p-2 rounded border border-gray-300 text-xl"
                />
        </div>
        
    </div>
        <div class="flex flex-row mt-4 justify-center space-x-4">
            <div>
              <button on:click={btn_asignar_conductor} class="bg-blue-400 text-blue-100">Asignar Conductor</button>
            </div>
            <div>
              <button class="bg-red-400 text-blue-100">Borrar Día</button>
            </div>
          
          </div>
      {/if}
  </div>
      
  
  
  
  <style>
    
  </style>