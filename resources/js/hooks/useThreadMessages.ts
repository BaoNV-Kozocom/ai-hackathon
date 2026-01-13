import { useQuery } from "@tanstack/react-query";
import { threadService } from "@/services/threadService";

export const useThreadMessages = (threadId: number | null) => {
    return useQuery({
        queryKey: ["threadMessages", threadId],
        queryFn: () =>
            threadId
                ? threadService.fetchMessages(threadId)
                : Promise.resolve([]),
        enabled: !!threadId,
    });
};
