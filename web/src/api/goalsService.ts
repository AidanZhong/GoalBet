import axiosClient from "./axiosClient.ts";

export type MarketsDTO = {
    support: number;
    against: number;
    total?: number;
};

export type GoalUpdateDTO = {
    id: number;
    goal_id: number;
    content: string;
    author_email: string;
    created_at: string;
    youtube_url?: string;
};

export type GoalDTO = {
    id: number;
    owner_email: string;
    title: string;
    description: string;
    deadline: string;
    status: string;
    markets: MarketsDTO | any;
    updates: GoalUpdateDTO[];
    youtube_url?: string;
};

export const goalsService = {
    list() {
        return axiosClient.get<GoalDTO[]>("/goals");
    },

    create(payload: { title: string; description: string; deadline: string; youtube_url?: string }) {
        return axiosClient.post<GoalDTO>("/goals", payload);
    },

    postUpdate(goalId: number | string, payload: { content: string; youtube_url?: string }) {
        return axiosClient.post<GoalUpdateDTO>(`/goals/${goalId}/updates`, payload);
    },

    listMine() {
        return axiosClient.get<GoalDTO[]>("/goals/mine");
    },

    getById(id: string | number) {
        return axiosClient.get<GoalDTO>(`/goals/get_goal/${id}`);
    },

    resolve(goalId: string | number, outcome: "success" | "fail") {
        return axiosClient.post(`/goals/${goalId}/resolve`, {outcome});
    },
};