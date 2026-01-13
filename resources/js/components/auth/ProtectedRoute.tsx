import React, { useEffect } from "react";
import { Navigate, Outlet } from "react-router-dom";
import useAuthStore from "@/stores/useAuthStore";
import { useAuth } from "@/hooks/useAuth";

export default function ProtectedRoute() {
    const { user, isAuthenticated } = useAuthStore();
    const { fetchUser } = useAuth();

    // Attempt to hydrate user on first load
    useEffect(() => {
        if (!user) {
            fetchUser();
        }
    }, []);

    // Simple check. In real app, might want a 'loading' state while fetching /user
    // For now, if no user and fetch fails (handled in hook), we redirect.
    // To prevent flicker, we could add 'isCheckingAuth' state.

    // For this demo: If we believe we are authenticated or just loaded, we render Outlet.
    // If explicit 401 happened, useAuthStore updates isAuthenticated to false.

    if (!isAuthenticated && !user) {
        // This is tricky without a loading state.
        // Let's assume initialized false means verify first.
        return <div className="p-10 text-center">Loading session...</div>;
    }

    return <Outlet />;
}

// Better approach for ProtectedRoute with Loading state:
export function RequireAuth({ children }: { children: React.ReactNode }) {
    const { user, isLoading, isInitialized } = useAuthStore();

    // Show loading while checking auth
    if (isLoading || !isInitialized) {
        return (
            <div className="min-h-screen bg-neutral-950 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
                    <p className="text-neutral-500 text-sm">Loading...</p>
                </div>
            </div>
        );
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
}
