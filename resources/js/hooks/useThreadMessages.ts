import { useQuery, useQueryClient } from "@tanstack/react-query";
import { threadService } from "@/services/threadService";
import { useEffect } from "react";

export const useThreadMessages = (threadId: number | null) => {
    const queryClient = useQueryClient();

    useEffect(() => {
        if (!threadId) return;

        // @ts-ignore
        const channel = window.Echo.private(`thread.${threadId}`);

        // @ts-ignore
        channel.listen("MessageCreated", (e: any) => {
            queryClient.invalidateQueries({
                queryKey: ["threadMessages", threadId],
            });
            queryClient.invalidateQueries({ queryKey: ["threads"] });
        });

        // @ts-ignore
        channel.listen("ThreadUpdated", (e: any) => {
            queryClient.invalidateQueries({
                queryKey: ["threadMessages", threadId],
            });
            queryClient.invalidateQueries({ queryKey: ["threads"] });
        });

        return () => {
            // @ts-ignore
            window.Echo.leave(`thread.${threadId}`);
        };
    }, [threadId, queryClient]);

    return useQuery({
        queryKey: ["threadMessages", threadId],
        queryFn: () =>
            threadId
                ? threadService.fetchMessages(threadId)
                : Promise.resolve([]),
        enabled: !!threadId,
    });
};
