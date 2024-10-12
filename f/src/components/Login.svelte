<script>
    import { Field } from 'svelte-ux';
    import { Button  } from 'svelte-ux';
    import { saveToken, saveUser, checkToken } from '../utils_session';
    import { onMount } from 'svelte';
    export let name = '';
    export let showLogin = true;
    export let showSelectGrupo = false;
    const apiUrl = import.meta.env.VITE_API_URL;
    let user = '';
    let password = '';
    let showMessageLogin = true;

    onMount(() => {
        // Comprobar el token de sesión
        let estado_token = false;
        // Comprobar el token de sesión actual y actualizar el estado del token en la variable estado_token
        checkToken().then(resultado => {
            estado_token = resultado;
        });
        console.log('Login: Comprobando token de sesión...', estado_token);
        if (estado_token) {
            console.log('Login: Token válido');

        } else {
            console.log('Login: Token inválido');
        }
    });

    async function login() {
        const f_username = user;
        const f_password = password;

        showMessageLogin = false;
        console.log('LOGIN - username: ', f_username, 'password: ', f_password, 'showMessageLogin', showMessageLogin);

        // Crear el cuerpo codificado con URLSearchParams
        const formBody = new FormData();
        formBody.append("username", f_username);
        formBody.append("password", f_password);
        const response = await fetch(apiUrl + '/api/token', {
            method: 'POST',

            credentials: 'include',  // Permite incluir cookies en la solicitud
            body: formBody  // Pasar el cuerpo codificado
        });

        const data = await response.json();
        saveToken (data);
        saveUser (f_username);
        console.log('data: ', data);

        showMessageLogin = false;
        if (response.ok) {
            showLogin = false;
            showSelectGrupo = true;
            name = f_username;
        } else {
            alert(data.detail);
            showLogin = true;
            showMessageLogin = true;
            
        }
    }
</script>
<div class="m-5">
    <img src="favicon512.png" alt="Logo" class="w-16 h-16 m-auto">
</div>
{#if showMessageLogin}
<form on:submit|preventDefault={login}>
    <div>
        <div class="grid grid-flow-cols gap-2 text-lg">
            <Field id="usuario" label="Usuario" value={null}>
                <input id="username" autocomplete="additional-name" class="font-bold w-full" type="user" bind:value={user} placeholder="Username" required />
            </Field>
            <Field id="contraseña" label="Contraseña" value={null}>
                <input id="contraseña" class="w-full" type="password" bind:value={password} placeholder="Password" required />
            </Field>
            <button id="submit" class="bg-blue-500 hover:bg-blue-600 text-gray-900 font-bold py-2 px-4 rounded" type="submit">
                Login
            </button>
        </div>
    </div>
</form>
{:else}
<div class="text-center text-blue-600 text-3xl">
    Iniciando Sesion ...
</div>
{/if}

<style>

</style>