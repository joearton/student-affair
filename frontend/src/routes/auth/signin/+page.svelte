<script>
    import { login } from '$lib/auth';  
  
    let username = '';
    let password = '';
    let errorMessage = '';
    let successMessage = '';
  
    const handleLogin = async () => {
        const { errorMessage: err, successMessage: succ } = await login(username, password);
        
        errorMessage = err;
        successMessage = succ;
    };
</script>

<svelte:head>
    <title>Login</title>
</svelte:head>

<div class="container">
    <div class="row">
        <div class="col-md-3"></div>
        <div class="col-md-6">
            <div class="login-container bg-white shadow border rounded px-4 py-3 my-5">
                <h2 class='mb-3 text-center'>Sign In</h2>
                
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
                    <div class="form-input mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" id="username" class="form-control" bind:value={username} placeholder="Masukkan username" />
                    </div>
            
                    <div class="form-input">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" id="password" class="form-control" bind:value={password} placeholder="Masukkan password" />
                    </div>
                    
                    <div class="mt-3 text-center">
                        <button type="submit" class="btn btn-primary btn-lg btn-login">Sign In</button>
                    </div>
                </form>
            
                <div class="text-center mt-3">
                    <a href="/register" class="text-decoration-none">Belum punya akun? Daftar</a>
                </div>
            </div>            
        </div>
        <div class="col-md-3"></div>
    </div>
</div>
