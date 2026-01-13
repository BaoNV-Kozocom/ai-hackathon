import React, { useEffect } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./components/dashboard/Dashboard";
import Login from "./pages/auth/Login";
import DemoLogin from "./pages/DemoLogin";
import { RequireAuth } from "./components/auth/ProtectedRoute";
import useAuthStore from "./stores/useAuthStore";
import { useAuth } from "./hooks/useAuth";
import "../css/app.css";

const queryClient = new QueryClient();

function App() {
    const { fetchUser } = useAuth();
    const { user } = useAuthStore();

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <Routes>
            <Route
                path="/login"
                element={!!user ? <Navigate to="/" /> : <Login />}
            />
            <Route path="/demo-login" element={<DemoLogin />} />
            <Route
                path="/"
                element={
                    <RequireAuth>
                        <Dashboard />
                    </RequireAuth>
                }
            />
        </Routes>
    );
}

const container = document.getElementById("root");
if (container) {
    const root = createRoot(container);
    root.render(
        <React.StrictMode>
            <QueryClientProvider client={queryClient}>
                <BrowserRouter>
                    <App />
                </BrowserRouter>
            </QueryClientProvider>
        </React.StrictMode>
    );
}
