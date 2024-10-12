<script>
    import { onMount } from 'svelte';
    import { readToken, readUser } from '../utils_session.js';
    import { DatePickerField } from 'svelte-ux';
    import { Datefield } from 'svelte-mui';
    import MostrarModal from './MostrarModal.svelte';
    
    export let grupo;
    export let cargando_ext = false;
    export let dateValue = new Date();
    
    let format = 'DD/MM/YYYY';
    let date = new Date(); // Date
    const onchange = ({ detail }) => {
        dateValue = detail
        console.log('onchange', detail);
    };
    let data;
    
    let showButtons = true;

    import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function handleRender() {
        dispatch('renderEvent', { message: 'Renderiza' });
    }


    const apiUrl = import.meta.env.VITE_API_URL;
  
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    let datos_conductor;

    let open = false
  
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


    let isDialogOpen = false;  // Estado del diálogo
    let dialogTitle = "Día ya asignado";
    let dialogContent = "";
    function btn_asignar_conductor() {
        cargando = true;
        /* 
        1.- Comprobar que en ese día no hay ningun conductor asignado
        */
        const datos_viaje = { "fecha": dateValue.toISOString(),
                              "pk_viaje": datos_conductor.id_siguiente_conductor,
                            }
        fetch(apiUrl + '/api/comprobar_fecha/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": token.token_type + " " + token.access_token
            },
            body: JSON.stringify(datos_viaje)
            
        })
        .then(response => response.json())
        .then(data => {
            console.log('Comprobar fecha: ', data)
            /*
            2.- Si hay conductor asignado informar
            */
            if (data.existe) {
                /* Mostrar modal con los datos */
                isDialogOpen = true;
                const fecha_str = data.data.fecha.substring(0, 10);  // Convertir fecha a string
                const conductor_str = data.data.conductor;
                const grupo_str = data.data.grupo;
                dialogContent =  "El día " + fecha_str + " esta asignado a " + conductor_str + " del grupo " + grupo_str;

            } else {
                /* El día esta libre por tanto lo puedo asignar */
                console.log ('datos viaje -> ', datos_viaje)
            
                asignar_conductor (datos_viaje)
                handleRender ();

            }    
        })
        .catch(error => console.error('Error:', error));

        
        /*
        3.- Si no hay conductor asignado, entonces asignar
        */
        console.log('Asignar conductor a', dateValue, datos_conductor);
    }

    function asignar_conductor(datos_viaje) {
        cargando_ext = true;
       
        fetch(apiUrl + '/api/asignar_conductor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": token.token_type + " " + token.access_token
            },
            body: JSON.stringify(datos_viaje)
            
        })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
        cargando_ext = false;
    }
    

      // Acción cuando se confirma la eliminación
    const handleDelete = () => {
        const datos_viaje = { "fecha": dateValue.toISOString(),
                              "pk_viaje": datos_conductor.id_siguiente_conductor,
                            }
        console.log("Item deleted!");
        asignar_conductor (datos_viaje);
        isDialogOpen = false;  // Cerrar el diálogo después de la acción
    };

    // Cerrar el diálogo
    const closeDialog = () => {
        isDialogOpen = false;
        cargando = false;
    };


    function btn_borrar_dia() {
        cargando = true;
        console.log('cargando', cargando);
        /* 
        1.- Comprobar que en ese día no hay ningun conductor asignado
        */
        const datos_dia = { "fecha": dateValue.toISOString(),
                            }
        fetch(apiUrl + '/api/borrar_dia/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": token.token_type + " " + token.access_token
            },
            body: JSON.stringify(datos_dia)
            
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(handleRender, 100);

            console.log('Resultado del borrado: ', data)
        })
        .catch(error => console.error('Error:', error));
    }


  </script>
  
  
  <div class="text-blue-500 text-2xl">
      {#if cargando} 
      <div class="mt-10">
          Cargando...
      </div>
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
        <div>
            <Datefield
            value={date}
            readonly=false  
            {format}
            message={format}
            locale="es-ES"
            icon=true
            on:date-change={onchange}
        />
        </div>

    </div>
        <div class="flex flex-row mt-4 justify-center space-x-4">
            <div>
              <button on:click={btn_asignar_conductor} class="bg-blue-400 text-blue-100">Asignar Conductor</button>
            </div>
            <div>
              <button on:click={btn_borrar_dia} class="bg-red-400 text-blue-100">Borrar Día</button>
            </div>
          
          </div>
      {/if}

    <!-- Componente de diálogo con control externo -->
      <MostrarModal 
      open={isDialogOpen}     
      onClose={closeDialog}    
      onConfirm={handleDelete} 
      dialogTitle={dialogTitle}   
      dialogContent={dialogContent}
      persistent=true
      messageConfirm="Reasignar"
    />
  </div>

  
  
  
  <style>
    
  </style>