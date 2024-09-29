<script>
    import { Button } from 'svelte-ux';
    import { onMount } from 'svelte';
    import { readToken, saveGroup } from '../utils_session';
    const apiUrl = import.meta.env.VITE_API_URL;

    let grupos = [];  // Variable reactiva para guardar los datos
    let cargando = true;  // Para mostrar un indicador de carga
    let token = readToken();
    export let grupo = 0;
    export let showSelectGrupo = false;
    let size = 40

    onMount (async function get_groups() {
        try {
            const response = await fetch(apiUrl + '/api/grupos', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": token.token_type + " " + token.access_token
                },
            });
            
            
            if (response.ok) {
                grupos = await response.json();
                console.log('Grupos', grupos);
            } else {
                alert('Login failed');
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
        } finally {
            cargando = false;  // Finaliza la carga
        }
    })

    function handleClick(grupoId) {
        console.log('Grupo seleccionado:', grupoId);
        grupo = grupoId;
        saveGroup (grupoId);  // Guarda el grupo seleccionado en la sesión
        showSelectGrupo = false;
        // Aquí puedes agregar la lógica para manejar el clic en el grupo
    }

</script>

<!-- Mostrar un mensaje mientras se están cargando los datos -->
{#if cargando}
  <p>Cargando...</p>
{:else}
  <!-- Renderizar los datos cuando se terminen de cargar -->
    <ul>
        {#each grupos as grupo}
          <li class="p-4"><Button on:click={() => handleClick (grupo.id)} class="w-56 text-2xl" variant="fill" color="primary" >{grupo.descripcion}</Button></li>
        {/each}
      </ul>
{/if}