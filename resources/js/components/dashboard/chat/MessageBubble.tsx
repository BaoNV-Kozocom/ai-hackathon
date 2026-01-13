import { useState } from "react";
import { User, Sparkles, Terminal, ChevronDown, ChevronUp } from "lucide-react";
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
    const [isExpanded, setIsExpanded] = useState(false);

    if (isSystem) {
        const lines = message.content.split("\n");
        const shouldTruncate = lines.length > 5;
        const displayContent =
            shouldTruncate && !isExpanded
                ? lines.slice(0, 5).join("\n")
                : message.content;

        return (
            <div className="flex justify-start w-full max-w-full mx-auto my-4 px-4">
                <div className="bg-neutral-950 border border-white/10 rounded-lg p-4 font-mono text-sm text-neutral-400 w-full shadow-lg">
                    <div className="flex items-center gap-2 mb-2 pb-2 border-b border-white/5 text-xs text-neutral-500 uppercase tracking-widest">
                        <Terminal className="w-3 h-3" /> System Log
                    </div>
                    <div className="whitespace-pre-wrap leading-relaxed overflow-x-auto">
                        {displayContent}
                        {shouldTruncate && !isExpanded && (
                            <span className="text-neutral-600">...</span>
                        )}
                    </div>
                    {shouldTruncate && (
                        <button
                            onClick={() => setIsExpanded(!isExpanded)}
                            className="mt-3 flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                        >
                            {isExpanded ? (
                                <>
                                    <ChevronUp className="w-3 h-3" />
                                    Show less
                                </>
                            ) : (
                                <>
                                    <ChevronDown className="w-3 h-3" />
                                    Read more ({lines.length - 5} more lines)
                                </>
                            )}
                        </button>
                    )}
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
                            <div className="prose prose-invert prose-sm max-w-[50vw] overflow-y-auto pr-2">
                                <ReactMarkdown>{message.content}</ReactMarkdown>
                            </div>
                        ) : (
                            message.content
                        )}
                    </div>

                    {/* AI Code Fix Attachment */}
                    {isAI && message.meta_data && message.meta_data.diff && (
                        <div className="w-full min-w-125 mt-2 animate-in fade-in slide-in-from-top-4 duration-500">
                            <CodeFixCard
                                filePath={
                                    message.meta_data.file_path || "unknown.php"
                                }
                                confidence={95}
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
