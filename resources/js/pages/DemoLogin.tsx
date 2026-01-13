import React, { useState } from "react";
import axios from "axios";
import {
    AlertCircle,
    CheckCircle,
    Loader2,
    Zap,
    Bug,
    Sparkles,
    ArrowRight,
} from "lucide-react";

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
                    }. Check the Agent logs!`
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
        <div className="min-h-screen bg-neutral-950 flex">
            {/* Left Side - Info Panel */}
            <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 p-12 flex-col justify-between relative overflow-hidden">
                {/* Background Pattern */}
                <div className="absolute inset-0 opacity-10">
                    <div className="absolute top-20 left-20 w-72 h-72 bg-white rounded-full blur-3xl"></div>
                    <div className="absolute bottom-20 right-20 w-96 h-96 bg-white rounded-full blur-3xl"></div>
                </div>

                {/* Logo */}
                <div className="relative z-10">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                            <Zap className="w-7 h-7 text-white" />
                        </div>
                        <span className="text-2xl font-bold text-white">
                            AI Debugger
                        </span>
                    </div>
                </div>

                {/* Main Content */}
                <div className="relative z-10 space-y-8">
                    <h1 className="text-5xl font-bold text-white leading-tight">
                        Autonomous AI
                        <br />
                        <span className="text-white/80">Error Fixing</span>
                    </h1>
                    <p className="text-xl text-white/70 max-w-md">
                        Watch AI automatically detect, analyze, and fix
                        production errors in real-time.
                    </p>

                    {/* Features */}
                    <div className="space-y-4">
                        <div className="flex items-center gap-4 text-white/90">
                            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                                <Bug className="w-5 h-5" />
                            </div>
                            <span>Automatic error detection</span>
                        </div>
                        <div className="flex items-center gap-4 text-white/90">
                            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                                <Sparkles className="w-5 h-5" />
                            </div>
                            <span>AI-powered code analysis</span>
                        </div>
                        <div className="flex items-center gap-4 text-white/90">
                            <div className="w-10 h-10 bg-white/20 rounded-lg flex items-center justify-center">
                                <Zap className="w-5 h-5" />
                            </div>
                            <span>One-click fix & commit</span>
                        </div>
                    </div>
                </div>

                {/* Footer */}
                <div className="relative z-10 text-white/50 text-sm">
                    AI Hackathon 2026 • Built with GPT-4o
                </div>
            </div>

            {/* Right Side - Login Form */}
            <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
                <div className="w-full max-w-md">
                    {/* Mobile Logo */}
                    <div className="lg:hidden flex items-center gap-3 mb-8 justify-center">
                        <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                            <Zap className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-xl font-bold text-white">
                            AI Debugger
                        </span>
                    </div>

                    {/* Demo Badge */}
                    <div className="flex justify-center mb-6">
                        <div className="inline-flex items-center gap-2 px-4 py-2 bg-amber-500/10 border border-amber-500/20 rounded-full">
                            <div className="w-2 h-2 bg-amber-500 rounded-full animate-pulse"></div>
                            <span className="text-amber-400 text-sm font-medium">
                                Demo Mode
                            </span>
                        </div>
                    </div>

                    {/* Card */}
                    <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-8 shadow-2xl">
                        <div className="text-center mb-8">
                            <h2 className="text-2xl font-bold text-white mb-2">
                                Trigger an Error
                            </h2>
                            <p className="text-neutral-400">
                                Click sign in to simulate a production bug
                            </p>
                        </div>

                        <form onSubmit={handleLogin} className="space-y-5">
                            <div>
                                <label className="block text-sm font-medium text-neutral-300 mb-2">
                                    Email Address
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full px-4 py-3.5 bg-neutral-800 border border-neutral-700 rounded-xl text-white placeholder-neutral-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-neutral-300 mb-2">
                                    Password
                                </label>
                                <input
                                    type="password"
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                    className="w-full px-4 py-3.5 bg-neutral-800 border border-neutral-700 rounded-xl text-white placeholder-neutral-500 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
                                />
                            </div>

                            {error && (
                                <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 flex items-start gap-3 animate-in fade-in slide-in-from-top-2 duration-300 overflow-hidden">
                                    <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
                                    <div className="min-w-0 flex-1">
                                        <p className="text-red-300 text-sm font-medium">
                                            Error Triggered!
                                        </p>
                                        <p className="text-red-400/80 text-sm mt-1 break-words whitespace-pre-wrap">
                                            {error}
                                        </p>
                                    </div>
                                </div>
                            )}

                            {success && (
                                <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-4 flex items-start gap-3 animate-in fade-in slide-in-from-top-2 duration-300 overflow-hidden">
                                    <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                                    <p className="text-emerald-300 text-sm break-words min-w-0 flex-1">
                                        {success}
                                    </p>
                                </div>
                            )}

                            <button
                                type="submit"
                                disabled={loading}
                                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold py-3.5 px-4 rounded-xl transition-all transform active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/25"
                            >
                                {loading ? (
                                    <>
                                        <Loader2 className="w-5 h-5 animate-spin" />
                                        Triggering Error...
                                    </>
                                ) : (
                                    <>
                                        Sign In
                                        <ArrowRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>
                        </form>

                        {/* Info Box */}
                        <div className="mt-6 p-4 bg-neutral-800/50 border border-neutral-700/50 rounded-xl">
                            <div className="flex items-start gap-3">
                                <div className="w-8 h-8 bg-indigo-500/20 rounded-lg flex items-center justify-center flex-shrink-0">
                                    <Sparkles className="w-4 h-4 text-indigo-400" />
                                </div>
                                <div>
                                    <p className="text-sm text-neutral-300 font-medium">
                                        What happens next?
                                    </p>
                                    <p className="text-xs text-neutral-500 mt-1">
                                        The error will be sent to the AI Agent,
                                        which will analyze and automatically fix
                                        the code.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Dashboard Link */}
                    <div className="mt-6 text-center">
                        <a
                            href="/dashboard"
                            className="text-indigo-400 hover:text-indigo-300 text-sm font-medium inline-flex items-center gap-1 transition-colors"
                        >
                            Go to Dashboard
                            <ArrowRight className="w-4 h-4" />
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DemoLogin;
