import { useState } from "react";
import { Check, Code2, ChevronDown, ChevronUp } from "lucide-react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

interface CodeFixCardProps {
    filePath: string;
    confidence: number;
    diffContent: string; // The proposed code change
    onApply: () => void;
}

export default function CodeFixCard({
    filePath,
    confidence,
    diffContent,
    onApply,
}: CodeFixCardProps) {
    const [isApplying, setIsApplying] = useState(false);
    const [isDiffExpanded, setIsDiffExpanded] = useState(false);

    const handleApply = async () => {
        setIsApplying(true);
        await onApply();
        setIsApplying(false);
    };

    // Determine color based on confidence
    const confidenceColor =
        confidence > 90
            ? "bg-emerald-500"
            : confidence > 70
            ? "bg-amber-500"
            : "bg-red-500";

    return (
        <div className="mt-4 rounded-xl border border-white/10 bg-black/40 overflow-hidden shadow-2xl backdrop-blur-sm group">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-white/5 border-b border-white/10">
                <div className="flex items-center gap-2 text-xs font-mono text-neutral-400">
                    <Code2 className="w-4 h-4 text-neutral-500" />
                    <span className="text-neutral-300">{filePath}</span>
                </div>

                <div
                    className="flex items-center gap-2"
                    title={`${confidence}% confidence`}
                >
                    <div className="h-1.5 w-16 bg-neutral-800 rounded-full overflow-hidden">
                        <div
                            className={`h-full ${confidenceColor} transition-all duration-500`}
                            style={{ width: `${confidence}%` }}
                        />
                    </div>
                    <span
                        className={`text-[10px] font-medium ${
                            confidence > 90
                                ? "text-emerald-400"
                                : "text-amber-400"
                        }`}
                    >
                        {confidence}%
                    </span>
                </div>
            </div>

            {/* Code Diff Preview */}
            <div className="relative group/code">
                <div
                    className={`transition-all duration-300 ${
                        isDiffExpanded ? "max-h-[500px]" : "max-h-[200px]"
                    } overflow-hidden relative`}
                >
                    <SyntaxHighlighter
                        language="php"
                        style={vscDarkPlus}
                        customStyle={{
                            margin: 0,
                            padding: "1rem",
                            fontSize: "0.85rem",
                            background: "transparent",
                        }}
                        showLineNumbers={true}
                    >
                        {diffContent}
                    </SyntaxHighlighter>

                    {/* Gradient Overlay for collapsed state */}
                    {!isDiffExpanded && (
                        <div className="absolute bottom-0 left-0 right-0 h-20 bg-linear-to-t from-black/80 to-transparent pointer-events-none" />
                    )}
                </div>

                <button
                    onClick={() => setIsDiffExpanded(!isDiffExpanded)}
                    className="absolute bottom-2 right-2 p-1.5 rounded-md bg-neutral-800/80 text-neutral-400 hover:text-white hover:bg-neutral-700 backdrop-blur-md opacity-0 group-hover/code:opacity-100 transition-opacity text-xs flex items-center gap-1"
                >
                    {isDiffExpanded ? (
                        <>
                            <ChevronUp className="w-3 h-3" /> Less
                        </>
                    ) : (
                        <>
                            <ChevronDown className="w-3 h-3" /> More
                        </>
                    )}
                </button>
            </div>

            {/* Actions */}
            <div className="p-3 bg-white/5 border-t border-white/5 flex gap-3">
                <button
                    onClick={handleApply}
                    disabled={isApplying}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-medium py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(5,150,105,0.3)] hover:shadow-[0_0_20px_rgba(5,150,105,0.5)]"
                >
                    {isApplying ? (
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    ) : (
                        <Check className="w-4 h-4" />
                    )}
                    Apply Fix
                </button>
                <button className="px-4 py-2 text-sm font-medium text-neutral-400 hover:text-white hover:bg-white/5 rounded-lg transition-colors border border-transparent hover:border-white/10">
                    View Full Diff
                </button>
            </div>
        </div>
    );
}
