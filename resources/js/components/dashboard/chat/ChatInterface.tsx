import { useEffect, useRef, useState } from "react";
import {
    CheckCircle2,
    MoreHorizontal,
    Send,
    Code2,
    GitCommit,
    ListTodo,
    ArrowLeft,
} from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import MessageBubble from "./MessageBubble";
import { threadService } from "@/services/threadService";
import { Message } from "@/types/dashboard";
import { useThreadMessages } from "@/hooks/useThreadMessages";

interface ChatInterfaceProps {
    threadId: number;
    onBack: () => void;
}

export default function ChatInterface({
    threadId,
    onBack,
}: ChatInterfaceProps) {
    const { data: messages, isLoading } = useThreadMessages(threadId);
    const bottomRef = useRef<HTMLDivElement>(null);
    const queryClient = useQueryClient();
    const [inputValue, setInputValue] = useState("");

    // Mark Resolved Mutation
    const resolveMutation = useMutation({
        mutationFn: () => threadService.markResolved(threadId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["threads"] });
            // Optionally refetch specific filter queries if needed, but generic invalidation works if using same base key
        },
    });

    // Commit Code Mutation
    const commitMutation = useMutation({
        mutationFn: () =>
            threadService.commitCode(
                `thread-${threadId}`,
                `Fix issue from thread #${threadId} via AI debugger`
            ),
        onSuccess: (data) => {
            if (data.status === "success") {
                alert(
                    `✅ Code committed successfully!\nBranch: ${data.branch}`
                );
            } else {
                alert(`❌ Commit failed: ${data.message}`);
            }
        },
        onError: (error: any) => {
            alert(`❌ Commit failed: ${error.message || "Unknown error"}`);
        },
    });

    // Send Message Mutation
    const sendMessageMutation = useMutation({
        mutationFn: (content: string) =>
            threadService.sendMessage(threadId, content),
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["threadMessages", threadId],
            });
            setInputValue("");
        },
    });

    const handleSendMessage = () => {
        if (!inputValue.trim()) return;
        sendMessageMutation.mutate(inputValue);
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    // Smart Scroll: Scroll to bottom when new messages appear
    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages, threadId]);

    if (isLoading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-8 h-8 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin" />
                    <p className="text-neutral-500 font-mono text-xs animate-pulse">
                        ANALYZING LOGS...
                    </p>
                </div>
            </div>
        );
    }

    return (
        <div className="flex flex-col h-full">
            {/* Header */}
            <div className="h-16 border-b border-white/10 bg-neutral-900/50 backdrop-blur flex items-center justify-between px-4 md:px-6 md:pl-16 z-10 shrink-0">
                <div className="flex items-center gap-3">
                    <button
                        onClick={onBack}
                        className="md:hidden p-2 -ml-2 text-neutral-400 hover:text-white transition-colors"
                    >
                        <ArrowLeft className="w-5 h-5" />
                    </button>
                    <div>
                        <h1 className="text-white font-semibold flex items-center gap-2">
                            Thread #{threadId}
                        </h1>
                        <p className="text-xs text-neutral-500">
                            Live Debugging Session
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-3">
                    <button
                        onClick={() => resolveMutation.mutate()}
                        disabled={resolveMutation.isPending}
                        className="group relative flex items-center gap-2 text-xs font-bold text-white bg-linear-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 px-4 py-1.5 rounded-full shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden"
                    >
                        <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                        {resolveMutation.isPending ? (
                            <div className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                        ) : (
                            <CheckCircle2 className="w-3.5 h-3.5" />
                        )}
                        <span className="relative z-10">Mark Resolved</span>
                    </button>
                    <button className="p-1.5 hover:bg-white/5 rounded text-neutral-500 hover:text-white transition-colors">
                        <MoreHorizontal className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6">
                <div className="max-w-full mx-auto flex flex-col justify-end min-h-full">
                    <div className="flex-1" />
                    {messages?.map((msg: Message) => (
                        <MessageBubble
                            key={msg.id}
                            message={msg}
                            threadId={threadId}
                        />
                    ))}
                    <div ref={bottomRef} className="h-1" />
                </div>
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-white/10 bg-neutral-900 shrink-0">
                <div className="max-w-4xl mx-auto relative group">
                    <div className="absolute inset-0 bg-linear-to-r from-indigo-500/20 to-purple-500/20 rounded-xl blur opacity-0 group-focus-within:opacity-100 transition-opacity duration-500" />
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask AI to investigate further..."
                        disabled={sendMessageMutation.isPending}
                        className="w-full bg-neutral-950/80 border border-white/10 rounded-xl py-3.5 pl-4 pr-12 text-sm text-neutral-200 focus:outline-none focus:border-indigo-500/50 transition-all relative z-10 placeholder:text-neutral-600 disabled:opacity-50"
                    />
                    <button
                        onClick={handleSendMessage}
                        disabled={
                            !inputValue.trim() || sendMessageMutation.isPending
                        }
                        className="absolute right-2 top-2 p-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg transition-colors z-20 shadow-lg shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>

                {/* Action Shortcuts */}
                <div className="flex gap-2 mt-3 overflow-x-auto pb-1 items-center justify-center">
                    <button className="px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-xs font-medium border border-emerald-500/20 transition-colors flex items-center gap-1.5 whitespace-nowrap">
                        <Code2 className="w-3.5 h-3.5" /> Fix Bug
                    </button>
                    <button
                        onClick={() => commitMutation.mutate()}
                        disabled={commitMutation.isPending}
                        className="px-3 py-1.5 rounded-lg bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 text-xs font-medium border border-indigo-500/20 transition-colors flex items-center gap-1.5 whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {commitMutation.isPending ? (
                            <div className="w-3.5 h-3.5 border-2 border-indigo-400/30 border-t-indigo-400 rounded-full animate-spin" />
                        ) : (
                            <GitCommit className="w-3.5 h-3.5" />
                        )}
                        {commitMutation.isPending
                            ? "Committing..."
                            : "Commit Code"}
                    </button>
                    <button className="px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 text-xs font-medium border border-amber-500/20 transition-colors flex items-center gap-1.5 whitespace-nowrap">
                        <ListTodo className="w-3.5 h-3.5" /> Do Task
                    </button>
                </div>

                <div className="max-w-4xl mx-auto mt-2 text-center text-[10px] text-neutral-600 font-mono">
                    AI Debugger v1.0 • Connected to Local Environment
                </div>
            </div>
        </div>
    );
}
