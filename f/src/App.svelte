<script>import "./app.css";
  import { readToken, readGroup, clearUser, clearGroup } from "./utils_session";
  import { onMount } from'svelte';
  import Login from './components/Login.svelte';
  import SelectGroup from "./components/SelectGroup.svelte";
  import Viajes from './components/Viajes.svelte';
  import TestFecha from "./components/Test_Fecha.svelte";
  
  const apiUrl = import.meta.env.VITE_API_URL;
  console.log('API URL', apiUrl);
  let name = '';
  let token = false
  $: showLogin = true;
  $: showSelectGrupo = false;
  $: grupo = 0;
  $: console.log ('grupo', grupo);

  // Recuperar el token almacenado cuando el componente se carga
  onMount(() => {
    console.log('Componente cargado, recuperando token...');
    token = readToken();
    
    if (token) {
      showLogin = false;
      showSelectGrupo = true;
    } else {
      clearUser();
      clearGroup();
    }
    
    grupo = readGroup();

    if (grupo > 0) {
      showLogin = false;
      showSelectGrupo = false;
    }
  
  });
</script>

<main>


{#if showLogin}
<div>
  <Login bind:name bind:showLogin bind:showSelectGrupo></Login>
</div>
{/if}

{#if showSelectGrupo}
<div>
  <SelectGroup bind:grupo bind:showSelectGrupo></SelectGroup> 
</div>
{/if}

{#if grupo > 0 }
<div class="text-red-500">
  <Viajes bind:grupo bind:showSelectGrupo></Viajes>
</div>
{/if}
</main>



<style>

</style>
