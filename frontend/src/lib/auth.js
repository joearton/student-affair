import { apiRequest } from '../api';


export const login = async (/** @type {string} */ username, /** @type {string} */ password) => {
    let errorMessage = '';
    let successMessage = '';

    if (!username || !password) {
        errorMessage = 'Username dan password harus diisi.';
        return { errorMessage, successMessage };
    }

    try {
        // @ts-ignore
        const response = await apiRequest('/token/', 'POST', { username, password });
        const { access, refresh } = response;

        // Simpan token ke sessionStorage
        sessionStorage.setItem('access_token', access);
        sessionStorage.setItem('refresh_token', refresh);

        successMessage = 'Login berhasil!';
        errorMessage = ''; // Clear previous error message
    } catch (error) {
        // @ts-ignore
        if (error.response && error.response.status === 401) {
            errorMessage = 'Login gagal. Username atau password salah.';
        } else {
            errorMessage = 'Terjadi kesalahan saat mencoba login.';
        }
        successMessage = ''; // Clear previous success message
    }

  return { errorMessage, successMessage };
};
