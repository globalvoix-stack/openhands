import { SuggestedTask } from "#/utils/types";
import { thinksoft } from "../thinksoft-axios";

export class SuggestionsService {
  static async getSuggestedTasks(): Promise<SuggestedTask[]> {
    const { data } = await thinksoft.get("/api/user/suggested-tasks");
    return data;
  }
}
