import { create } from "zustand";

interface User {
    id: number;
    name: string;
    email: string;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    isInitialized: boolean;
    setUser: (user: User | null) => void;
    setIsAuthenticated: (status: boolean) => void;
    setIsLoading: (status: boolean) => void;
    setIsInitialized: (status: boolean) => void;
}

const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    isInitialized: false,
    setUser: (user) => set({ user, isAuthenticated: !!user }),
    setIsAuthenticated: (status) => set({ isAuthenticated: status }),
    setIsLoading: (status) => set({ isLoading: status }),
    setIsInitialized: (status) => set({ isInitialized: status }),
}));

export default useAuthStore;
