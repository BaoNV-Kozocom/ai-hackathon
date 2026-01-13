import axios from "axios";
import { Thread, Message } from "../types/dashboard";

const API_BASE = "/api";
const PYTHON_API_BASE = "http://localhost:5001";

export const threadService = {
    async fetchThreads(filter: string = "all"): Promise<Thread[]> {
        const response = await axios.get(`${API_BASE}/threads`, {
            params: { filter },
        });
        // Handle Laravel Resource wrapper (response.data.data) or direct array (response.data)
        const data = response.data;
        if (Array.isArray(data)) {
            return data;
        }
        if (data && Array.isArray(data.data)) {
            return data.data;
        }
        console.warn("Unexpected API response format for threads:", data);
        return [];
    },

    async fetchMessages(threadId: number): Promise<Message[]> {
        const response = await axios.get(
            `${API_BASE}/threads/${threadId}/messages`
        );
        const data = response.data;
        if (Array.isArray(data)) {
            return data;
        }
        if (data && Array.isArray(data.data)) {
            return data.data;
        }
        console.warn("Unexpected API response format for messages:", data);
        return [];
    },

    async applyFix(threadId: number, fixData: any): Promise<void> {
        await axios.post(`${API_BASE}/threads/${threadId}/apply-fix`, fixData);
    },

    async markResolved(threadId: number): Promise<void> {
        await axios.patch(`${API_BASE}/threads/${threadId}/status`, {
            status: "resolved",
        });
    },

    async sendMessage(threadId: number, content: string): Promise<Message> {
        const response = await axios.post(
            `${API_BASE}/threads/${threadId}/messages`,
            { content }
        );
        return response.data;
    },

    async commitCode(
        issueName: string,
        commitMessage: string,
        files?: string[]
    ): Promise<{
        status: string;
        branch?: string;
        message: string;
        push_output?: string;
    }> {
        const response = await axios.post(`${PYTHON_API_BASE}/commit-code`, {
            issue_name: issueName,
            commit_message: commitMessage,
            files: files,
        });
        return response.data;
    },
};
