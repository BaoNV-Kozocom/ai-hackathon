import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useAuth } from "@/hooks/useAuth";
import { BrainCircuit, Mail, Lock, ArrowRight, Loader2 } from "lucide-react";

const schema = z.object({
    email: z.string().email("Please enter a valid email address"),
    password: z.string().min(1, "Password is required"),
});

type LoginForm = z.infer<typeof schema>;

export default function Login() {
    const { login, errors, isLoading } = useAuth();
    const {
        register,
        handleSubmit,
        formState: { errors: formErrors },
    } = useForm<LoginForm>({
        resolver: zodResolver(schema),
    });

    const onSubmit = (data: LoginForm) => {
        login(data);
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-neutral-950 relative overflow-hidden">
            {/* Ambient Background Effects */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-3xl h-[500px] bg-indigo-600/20 blur-[120px] rounded-full pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-purple-600/10 blur-[100px] rounded-full pointer-events-none" />

            <div className="w-full max-w-md relative z-10 px-6">
                {/* Logo Section */}
                <div className="flex flex-col items-center mb-8">
                    <div className="w-16 h-16 rounded-2xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-xl shadow-indigo-500/20 mb-6 p-px">
                        <div className="w-full h-full rounded-2xl bg-neutral-900/30 backdrop-blur-sm flex items-center justify-center">
                            <BrainCircuit className="w-9 h-9 text-white" />
                        </div>
                    </div>
                    <h1 className="text-3xl font-bold bg-linear-to-r from-white to-neutral-400 bg-clip-text text-transparent tracking-tight">
                        Welcome Back
                    </h1>
                    <p className="mt-2 text-neutral-500 font-medium">
                        Sign in to MyMind Debugger
                    </p>
                </div>

                {/* Login Card */}
                <div className="bg-neutral-900/50 backdrop-blur-xl border border-white/10 p-8 rounded-2xl shadow-2xl">
                    <form
                        className="space-y-5"
                        onSubmit={handleSubmit(onSubmit)}
                    >
                        {/* Email Input */}
                        <div className="space-y-1.5">
                            <label className="text-xs font-medium text-neutral-400 ml-1">
                                Email Address
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Mail className="h-4 w-4 text-neutral-500 group-focus-within:text-indigo-400 transition-colors" />
                                </div>
                                <input
                                    {...register("email")}
                                    type="email"
                                    placeholder="admin@admin.com"
                                    className="block w-full pl-10 pr-3 py-2.5 bg-neutral-950/50 border border-white/10 rounded-xl text-neutral-200 placeholder:text-neutral-600 focus:outline-none focus:border-indigo-500/50 focus:bg-neutral-900 transition-all sm:text-sm"
                                />
                            </div>
                            {(formErrors.email || errors.email) && (
                                <p className="text-xs text-red-500 ml-1">
                                    {formErrors.email?.message ||
                                        errors.email?.[0]}
                                </p>
                            )}
                        </div>

                        {/* Password Input */}
                        <div className="space-y-1.5">
                            <label className="text-xs font-medium text-neutral-400 ml-1">
                                Password
                            </label>
                            <div className="relative group">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-4 w-4 text-neutral-500 group-focus-within:text-indigo-400 transition-colors" />
                                </div>
                                <input
                                    {...register("password")}
                                    type="password"
                                    placeholder="••••••••"
                                    className="block w-full pl-10 pr-3 py-2.5 bg-neutral-950/50 border border-white/10 rounded-xl text-neutral-200 placeholder:text-neutral-600 focus:outline-none focus:border-indigo-500/50 focus:bg-neutral-900 transition-all sm:text-sm"
                                />
                            </div>
                            {(formErrors.password || errors.password) && (
                                <p className="text-xs text-red-500 ml-1">
                                    {formErrors.password?.message ||
                                        errors.password?.[0]}
                                </p>
                            )}
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            disabled={isLoading}
                            className="w-full flex items-center justify-center gap-2 py-2.5 px-4 bg-linear-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-medium rounded-xl transition-all shadow-lg shadow-indigo-500/25 hover:shadow-indigo-500/40 active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed mt-2"
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-4 h-4 animate-spin" />
                                    Signing in...
                                </>
                            ) : (
                                <>
                                    Sign In <ArrowRight className="w-4 h-4" />
                                </>
                            )}
                        </button>
                    </form>
                </div>

                <div className="mt-8 text-center text-xs text-neutral-600 font-mono">
                    AI Debugger System v1.0
                </div>
            </div>
        </div>
    );
}
