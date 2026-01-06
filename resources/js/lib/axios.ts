import axios from "axios";
import { config } from "@/config";
import useAuthStore from "@/stores/useAuthStore";

const axiosClient = axios.create({
    baseURL: config.apiBaseUrl,
    withCredentials: true, // Critical for Sanctum cookies
    headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
    },
});

// Interceptor to handle 401s
axiosClient.interceptors.response.use(
    (response) => response,
    (error) => {
        const { response } = error;
        if (response && response.status === 401) {
            // Clear auth state
            useAuthStore.getState().setUser(null);
            useAuthStore.getState().setIsAuthenticated(false);

            // Redirect to login if not already there
            if (window.location.pathname !== "/login") {
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

export default axiosClient;
