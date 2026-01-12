import React, { useState } from "react";
import axios from "axios";
import { AlertCircle, CheckCircle, Loader2 } from "lucide-react";

const DemoLogin = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);
    const [email, setEmail] = useState("demo@example.com");
    const [password, setPassword] = useState("password");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(null);

        try {
            // Intentionally triggering the error endpoint
            await axios.post("/api/demo/login-error", { email, password });
            setSuccess("Login Successful (Unexpected!)");
        } catch (err: any) {
            console.error("Login Error:", err);
            // Verify if the error response confirms the system caught it
            if (err.response && err.response.data) {
                setError(
                    `Server Error: ${
                        err.response.data.message || err.message
                    }. check the Agent logs!`
                );
            } else {
                setError(
                    "Network Error or System Crash! The Agent should allow you to debug this."
                );
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
            <div className="max-w-md w-full bg-gray-800 rounded-2xl shadow-xl overflow-hidden border border-gray-700">
                <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-8 text-center">
                    <h1 className="text-3xl font-bold text-white mb-2">
                        MyMind Demo
                    </h1>
                    <p className="text-purple-200">
                        System Error Demonstration
                    </p>
                </div>

                <div className="p-8">
                    <form onSubmit={handleLogin} className="space-y-6">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">
                                Email Address
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors"
                            />
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">
                                Password
                            </label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition-colors"
                            />
                        </div>

                        {error && (
                            <div className="bg-red-900/50 border border-red-500/50 rounded-lg p-4 flex items-start gap-3">
                                <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                                <p className="text-red-200 text-sm">{error}</p>
                            </div>
                        )}

                        {success && (
                            <div className="bg-green-900/50 border border-green-500/50 rounded-lg p-4 flex items-start gap-3">
                                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                                <p className="text-green-200 text-sm">
                                    {success}
                                </p>
                            </div>
                        )}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-4 rounded-lg transition-all transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    Authenticating...
                                </>
                            ) : (
                                "Sign In"
                            )}
                        </button>
                    </form>

                    <div className="mt-6 text-center text-xs text-gray-500">
                        <p>
                            Clicking "Sign In" will trigger a backend exception.
                        </p>
                        <p>The Python Agent should catch and analyze this.</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DemoLogin;
