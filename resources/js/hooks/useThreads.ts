import { useQuery } from "@tanstack/react-query";
import { threadService } from "@/services/threadService";

export const useThreads = (filter: string) => {
    return useQuery({
        queryKey: ["threads", filter],
        queryFn: () => threadService.fetchThreads(filter),
    });
};
