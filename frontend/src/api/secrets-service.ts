import { thinksoft } from "./thinksoft-axios";
import {
  CustomSecret,
  GetSecretsResponse,
  POSTProviderTokens,
} from "./secrets-service.types";
import { Provider, ProviderToken } from "#/types/settings";

export class SecretsService {
  static async getSecrets() {
    const { data } = await thinksoft.get<GetSecretsResponse>("/api/secrets");
    return data.custom_secrets;
  }

  static async createSecret(name: string, value: string, description?: string) {
    const secret: CustomSecret = {
      name,
      value,
      description,
    };

    const { status } = await thinksoft.post("/api/secrets", secret);
    return status === 201;
  }

  static async updateSecret(id: string, name: string, description?: string) {
    const secret: Omit<CustomSecret, "value"> = {
      name,
      description,
    };

    const { status } = await thinksoft.put(`/api/secrets/${id}`, secret);
    return status === 200;
  }

  static async deleteSecret(id: string) {
    const { status } = await thinksoft.delete<boolean>(`/api/secrets/${id}`);
    return status === 200;
  }

  static async addGitProvider(providers: Record<Provider, ProviderToken>) {
    const tokens: POSTProviderTokens = {
      provider_tokens: providers,
    };
    const { data } = await thinksoft.post<boolean>(
      "/api/add-git-providers",
      tokens,
    );
    return data;
  }
}
