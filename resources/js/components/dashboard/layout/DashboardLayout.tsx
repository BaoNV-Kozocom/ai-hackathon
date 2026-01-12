import { useState } from "react";
import { LayoutList, PanelLeft } from "lucide-react";
import { useThreads } from "@/hooks/useThreads";
import ThreadList from "../sidebar/ThreadList";
import ChatInterface from "../chat/ChatInterface";

export default function DashboardLayout() {
    const [selectedThreadId, setSelectedThreadId] = useState<number | null>(
        null
    );
    const [filter, setFilter] = useState("open"); // open, resolved, all
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const { data: threads, isLoading } = useThreads(filter);

    return (
        <div className="flex h-screen bg-neutral-950 text-neutral-100 overflow-hidden font-sans">
            {/* Sidebar */}
            <div
                className={`${selectedThreadId ? "hidden md:flex" : "flex"} ${
                    isSidebarOpen ? "w-full md:w-80" : "w-0 md:w-0"
                } flex-col border-r border-white/10 bg-neutral-900/50 backdrop-blur-xl transition-all duration-300 ease-in-out overflow-hidden shrink-0`}
            >
                <div
                    className={`${
                        isSidebarOpen ? "opacity-100" : "opacity-0"
                    } transition-opacity duration-300 h-full flex flex-col min-w-[320px] md:min-w-[20rem]`}
                >
                    <ThreadList
                        threads={threads}
                        isLoading={isLoading}
                        filter={filter}
                        setFilter={setFilter}
                        selectedThreadId={selectedThreadId}
                        setSelectedThreadId={setSelectedThreadId}
                    />
                </div>
            </div>

            {/* Main Content */}
            <div
                className={`${
                    !selectedThreadId ? "hidden md:flex" : "flex"
                } flex-1 bg-neutral-900 relative flex-col min-w-0`}
            >
                {/* Sidebar Toggle Button (Desktop) */}
                <div className="hidden md:flex absolute top-4 left-4 z-20">
                    <button
                        onClick={() => setIsSidebarOpen(!isSidebarOpen)}
                        className="p-2 rounded-lg bg-neutral-800/50 text-neutral-400 hover:text-white hover:bg-neutral-800 border border-white/5 transition-colors"
                    >
                        <PanelLeft className="w-5 h-5" />
                    </button>
                </div>

                <div className="absolute inset-0 overflow-hidden flex flex-col">
                    {selectedThreadId ? (
                        <ChatInterface
                            threadId={selectedThreadId}
                            onBack={() => setSelectedThreadId(null)}
                        />
                    ) : (
                        <div className="h-full flex flex-col items-center justify-center text-neutral-500 select-none">
                            <div className="w-24 h-24 bg-neutral-900 rounded-2xl border border-white/5 flex items-center justify-center mb-6 shadow-2xl shadow-black/50">
                                <LayoutList className="w-10 h-10 opacity-20" />
                            </div>
                            <h3 className="text-lg font-medium text-neutral-300">
                                No thread selected
                            </h3>
                            <p className="max-w-sm text-center mt-2 text-neutral-600 px-6">
                                Select an issue from the sidebar to view the
                                debugging session and AI insights.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
