import { Search, BrainCircuit, LogOut } from "lucide-react";
import ThreadCard from "./ThreadCard";
import { Thread } from "@/types/dashboard";
import { useAuth } from "@/hooks/useAuth";

interface ThreadListProps {
    threads: Thread[] | undefined;
    isLoading: boolean;
    filter: string;
    setFilter: (filter: string) => void;
    selectedThreadId: number | null;
    setSelectedThreadId: (id: number) => void;
}

export default function ThreadList({
    threads,
    isLoading,
    filter,
    setFilter,
    selectedThreadId,
    setSelectedThreadId,
}: ThreadListProps) {
    const { user, logout } = useAuth();
    return (
        <div className="flex flex-col h-full">
            {/* Header */}
            <div className="p-4 border-b border-white/10">
                <div className="flex items-center gap-3 mb-6">
                    <div className="w-10 h-10 rounded-xl bg-linear-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                        <BrainCircuit className="w-6 h-6 text-white" />
                    </div>
                    <div>
                        <h1 className="text-lg font-bold bg-linear-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent tracking-tight">
                            MyMind
                        </h1>
                        <p className="text-[10px] text-neutral-500 font-medium tracking-wider uppercase">
                            AI Debugger System
                        </p>
                    </div>
                </div>

                <div className="relative">
                    <Search className="absolute left-3 top-2.5 w-4 h-4 text-neutral-500" />
                    <input
                        type="text"
                        placeholder="Search threads..."
                        className="w-full bg-neutral-900 border border-white/10 rounded-lg py-2 pl-9 pr-4 text-sm focus:outline-none focus:border-neutral-700 transition-colors placeholder:text-neutral-600"
                    />
                </div>

                <div className="flex gap-2 mt-3 overflow-x-auto pb-1">
                    {["open", "resolved", "all"].map((f) => (
                        <button
                            key={f}
                            onClick={() => setFilter(f)}
                            className={`px-3 py-1 rounded-full text-xs font-medium capitalize transition-colors cursor-pointer ${
                                filter === f
                                    ? "bg-neutral-100 text-neutral-900"
                                    : "bg-neutral-800 text-neutral-400 hover:text-neutral-200 hover:bg-neutral-700"
                            }`}
                        >
                            {f}
                        </button>
                    ))}
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-2">
                {isLoading ? (
                    <div className="space-y-3 p-2">
                        {[1, 2, 3].map((i) => (
                            <div
                                key={i}
                                className="h-20 bg-neutral-800/50 rounded-lg animate-pulse"
                            />
                        ))}
                    </div>
                ) : (
                    <div className="space-y-1">
                        {threads?.map((thread: Thread) => (
                            <ThreadCard
                                key={thread.id}
                                thread={thread}
                                isActive={selectedThreadId === thread.id}
                                onClick={() => setSelectedThreadId(thread.id)}
                            />
                        ))}
                    </div>
                )}
            </div>

            {/* User Profile / Settings (Bottom) */}
            <div className="p-4 border-t border-white/10 bg-neutral-950">
                <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3 min-w-0">
                        <div className="w-9 h-9 rounded-full bg-linear-to-br from-indigo-500 to-purple-600 p-px">
                            <div className="w-full h-full rounded-full bg-neutral-900 flex items-center justify-center">
                                <span className="text-sm font-bold text-white">
                                    {user?.name?.charAt(0) || "U"}
                                </span>
                            </div>
                        </div>
                        <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium truncate text-neutral-200">
                                {user?.name || "Guest User"}
                            </p>
                            <p className="text-xs text-neutral-500 truncate">
                                {user?.email || "guest@example.com"}
                            </p>
                        </div>
                    </div>

                    <button
                        onClick={logout}
                        className="p-2 rounded-lg text-neutral-500 hover:text-red-400 hover:bg-neutral-800 transition-colors cursor-pointer"
                        title="Logout"
                    >
                        <LogOut className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
}
