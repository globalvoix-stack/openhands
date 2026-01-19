import { useMutation, useQueryClient } from "@tanstack/react-query";
import { thinksoft } from "#/api/thinksoft-axios";
import {
  LLM_API_KEY_QUERY_KEY,
  LlmApiKeyResponse,
} from "#/hooks/query/use-llm-api-key";

export function useRefreshLlmApiKey() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const { data } = await thinksoft.post<LlmApiKeyResponse>(
        "/api/keys/llm/byor/refresh",
      );
      return data;
    },
    onSuccess: () => {
      // Invalidate the LLM API key query to trigger a refetch
      queryClient.invalidateQueries({ queryKey: [LLM_API_KEY_QUERY_KEY] });
    },
  });
}
