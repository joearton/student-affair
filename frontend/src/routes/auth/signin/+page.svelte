<script lang="ts">
    import { login } from '$lib/auth';  
    import { preference } from '$lib/stores/preference';    

    $: site_title = $preference.site_title;
    
    let [username, password, errorMessage, successMessage] = ['', '', '', ''];

    const handleLogin = async () => {
        const { errorMessage: err, successMessage: succ } = await login(username, password);
        
        errorMessage = err;
        successMessage = succ;
    };
</script>


<svelte:head>
    <title>Login | {site_title}</title>
</svelte:head>


<div class="container-fluid d-flex justify-content-center align-items-center min-vh-100">
    <div class="row w-100">
        <div class="login-container bg-white shadow-lg border rounded px-4 py-5">
            <h2 class="text-center mb-4 text-primary">Sign In</h2>

            {#if successMessage}
                <div class="alert alert-success" role="alert">
                    {successMessage}
                </div>
            {/if}

            {#if errorMessage}
                <div class="alert alert-danger" role="alert">
                    {errorMessage}
                </div>
            {/if}

            <form on:submit|preventDefault={handleLogin}>
                <div class="form-input mb-4">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" id="username" class="form-control form-control-lg" bind:value={username} placeholder="Masukkan username" required />
                </div>

                <div class="form-input mb-4">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" id="password" class="form-control form-control-lg" bind:value={password} placeholder="Masukkan password" required />
                </div>

                <div class="d-grid gap-2 mb-4">
                    <button type="submit" class="btn btn-primary btn-lg">Sign In</button>
                </div>
            </form>

            <div class="text-center">
                <a href="/register" class="text-decoration-none text-primary">Belum punya akun? Daftar</a>
            </div>
        </div>
    </div>
</div>


<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border-radius: 12px;
    }
    
    h2 {
        font-weight: bold;
    }
</style>