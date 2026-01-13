import { useQuery, useQueryClient } from "@tanstack/react-query";
import { threadService } from "@/services/threadService";
import { useEffect } from "react";

export const useThreads = (filter: string) => {
    const queryClient = useQueryClient();

    useEffect(() => {
        // @ts-ignore
        const channel = window.Echo.private("threads");
        // @ts-ignore
        channel.listen("ThreadCreated", (e: any) => {
            queryClient.invalidateQueries({ queryKey: ["threads"] });
        });

        // @ts-ignore
        channel.listen("ThreadUpdated", (e: any) => {
            queryClient.invalidateQueries({ queryKey: ["threads"] });
        });

        return () => {
            // @ts-ignore
            window.Echo.leave("threads");
        };
    }, [queryClient]);

    return useQuery({
        queryKey: ["threads", filter],
        queryFn: () => threadService.fetchThreads(filter),
    });
};
