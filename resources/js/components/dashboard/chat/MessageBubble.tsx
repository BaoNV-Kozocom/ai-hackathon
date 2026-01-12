import { User, Sparkles, Terminal } from "lucide-react";
import CodeFixCard from "./CodeFixCard";
import ReactMarkdown from "react-markdown";
import { Message } from "@/types/dashboard";
import { threadService } from "@/services/threadService";

interface MessageBubbleProps {
    message: Message;
    threadId: number;
}

export default function MessageBubble({
    message,
    threadId,
}: MessageBubbleProps) {
    const isUser = message.sender_type === "human_user";
    const isSystem = message.sender_type === "system_log";
    const isAI = message.sender_type === "ai_bot";

    if (isSystem) {
        return (
            <div className="flex justify-start w-full max-w-full mx-auto my-4 px-4">
                <div className="bg-neutral-950 border border-white/10 rounded-lg p-4 font-mono text-sm text-neutral-400 w-full shadow-lg">
                    <div className="flex items-center gap-2 mb-2 pb-2 border-b border-white/5 text-xs text-neutral-500 uppercase tracking-widest">
                        <Terminal className="w-3 h-3" /> System Log
                    </div>
                    <div className="whitespace-pre-wrap leading-relaxed overflow-x-auto">
                        {message.content}
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div
            className={`flex w-full mb-6 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >
            <div
                className={`flex max-w-[80%] ${
                    isUser ? "flex-row-reverse" : "flex-row"
                } gap-3`}
            >
                {/* Avatar */}
                <div
                    className={`shrink-0 w-8 h-8 rounded-full flex items-center justify-center shadow-lg ${
                        isUser ? "bg-indigo-600" : "bg-emerald-600"
                    }`}
                >
                    {isUser ? (
                        <User className="w-4 h-4 text-white" />
                    ) : (
                        <Sparkles className="w-4 h-4 text-white" />
                    )}
                </div>

                {/* Bubble Content */}
                <div
                    className={`flex flex-col ${
                        isUser ? "items-end" : "items-start"
                    }`}
                >
                    <div
                        className={`px-5 py-3 rounded-2xl shadow-md text-sm leading-relaxed ${
                            isUser
                                ? "bg-indigo-600 text-white rounded-tr-sm"
                                : "bg-neutral-800 text-neutral-200 border border-white/5 rounded-tl-sm"
                        }`}
                    >
                        {isAI ? (
                            <div className="prose prose-invert prose-sm max-w-none">
                                <ReactMarkdown>{message.content}</ReactMarkdown>
                            </div>
                        ) : (
                            message.content
                        )}
                    </div>

                    {/* AI Code Fix Attachment */}
                    {isAI &&
                        message.meta_data &&
                        message.meta_data.diff && ( // Check for 'diff' instead of 'has_fix' or 'diff_content' based on seeder
                            <div className="w-full min-w-[500px] mt-2 animate-in fade-in slide-in-from-top-4 duration-500">
                                <CodeFixCard
                                    filePath={
                                        message.meta_data.file_path ||
                                        "unknown.php"
                                    }
                                    confidence={
                                        95 // Hardcoded for now as seeder doesn't provide confidence
                                    }
                                    diffContent={message.meta_data.diff}
                                    onApply={() =>
                                        threadService.applyFix(
                                            threadId,
                                            message.meta_data
                                        )
                                    }
                                />
                            </div>
                        )}
                </div>
            </div>
        </div>
    );
}
