import { useNavigate } from "react-router-dom";
import axiosClient from "../lib/axios";
import useAuthStore from "../stores/useAuthStore";
import { useState } from "react";

export const useAuth = () => {
    const navigate = useNavigate();
    const { setUser, setIsAuthenticated } = useAuthStore();
    const [errors, setErrors] = useState<Record<string, string[]>>({});
    const [isLoading, setIsLoading] = useState(false);

    const csrf = async () => {
        await axiosClient.get("/sanctum/csrf-cookie", {
            baseURL: window.location.origin,
        });
    };

    const login = async (data: any) => {
        setIsLoading(true);
        setErrors({});
        try {
            await csrf(); // 1. Get CSRF Cookie
            await axiosClient.post("/login", data); // 2. Login
            await fetchUser(); // 3. Get User
            navigate("/"); // 4. Redirect
        } catch (error: any) {
            if (error.response && error.response.status === 422) {
                setErrors(error.response.data.errors);
            }
        } finally {
            setIsLoading(false);
        }
    };

    const logout = async () => {
        try {
            await axiosClient.post("/logout");
            setUser(null);
            setIsAuthenticated(false);
            navigate("/login");
        } catch (error) {
            console.error(error);
        }
    };

    const fetchUser = async () => {
        try {
            const response = await axiosClient.get("/user");
            setUser(response.data);
        } catch (error) {
            setUser(null);
            setIsAuthenticated(false);
        }
    };

    const { user, isAuthenticated } = useAuthStore();

    return {
        user,
        isAuthenticated,
        login,
        logout,
        fetchUser,
        errors,
        isLoading,
    };
};
