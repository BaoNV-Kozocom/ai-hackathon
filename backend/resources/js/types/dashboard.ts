export interface Thread {
    id: number;
    title: string;
    service: string;
    status: "open" | "resolved" | "ignored";
    severity: "critical" | "high" | "medium" | "low";
    created_at: string;
}

export interface FixMetaData {
    suggested_code?: string;
    file_path?: string;
    diff?: string;
    description?: string;
    confidence?: number;
}

export interface Message {
    id: number;
    sender_type: "system_log" | "human_user" | "ai_bot";
    content: string;
    meta_data: FixMetaData | null;
    created_at?: string;
}
