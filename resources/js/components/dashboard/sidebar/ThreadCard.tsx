import { formatDistanceToNow } from "date-fns";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { Thread } from "@/types/dashboard";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface ThreadCardProps {
    thread: Thread;
    isActive: boolean;
    onClick: () => void;
}

export default function ThreadCard({
    thread,
    isActive,
    onClick,
}: ThreadCardProps) {
    const isCritical = thread.severity === "critical";
    const isHigh = thread.severity === "high";

    return (
        <button
            onClick={onClick}
            className={cn(
                "w-full text-left p-3 rounded-lg border transition-all duration-200 group relative overflow-hidden",
                isActive
                    ? "bg-white/5 border-white/10 shadow-lg"
                    : "bg-transparent border-transparent hover:bg-white/5 hover:border-white/5"
            )}
        >
            {/* Active Indicator Line */}
            {isActive && (
                <div className="absolute left-0 top-3 bottom-3 w-1 bg-indigo-500 rounded-r-full shadow-[0_0_10px_rgba(99,102,241,0.5)]" />
            )}

            <div className={cn("flex flex-col gap-1", isActive && "pl-3")}>
                <div className="flex justify-between items-start gap-2">
                    <h3
                        className={cn(
                            "font-medium text-sm line-clamp-2 leading-snug",
                            isActive
                                ? "text-white"
                                : "text-neutral-300 group-hover:text-white"
                        )}
                    >
                        {thread.title}
                    </h3>

                    {/* Severity Dot */}
                    <div className="mt-1 shrink-0">
                        {isCritical ? (
                            <div className="w-2 h-2 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)] animate-pulse" />
                        ) : isHigh ? (
                            <div className="w-2 h-2 rounded-full bg-orange-500 shadow-[0_0_8px_rgba(249,115,22,0.6)]" />
                        ) : (
                            <div className="w-2 h-2 rounded-full bg-blue-500" />
                        )}
                    </div>
                </div>

                <div className="flex items-center justify-between mt-2">
                    <span className="text-[10px] uppercase tracking-wider font-mono text-neutral-500 bg-neutral-900/50 px-1.5 py-0.5 rounded border border-white/5">
                        {thread.service}
                    </span>
                    <span className="text-xs text-neutral-500 font-medium">
                        {formatDistanceToNow(new Date(thread.created_at), {
                            addSuffix: true,
                        }).replace("about ", "")}
                    </span>
                </div>
            </div>
        </button>
    );
}
