import axiosClient from "./axiosClient.ts";

export type MarketsDTO = {
    support: number;
    against: number;
    total?: number;
};

export type GoalDTO = {
    id: number;
    owner_email: string;
    title: string;
    description: string;
    deadline: string;
    status: string;
    markets: MarketsDTO | any;
    updates: any[];
};

export const goalsService = {
    list() {
        return axiosClient.get<GoalDTO[]>("/goals");
    },

    create(payload: {title:string, description:string, deadline:string}) {
        return axiosClient.post<GoalDTO>("/goals", payload);
    },

    listMine() {
        return axiosClient.get<GoalDTO[]>("/goals/mine");
    },

    getById(id: string | number) {
        return axiosClient.get<GoalDTO>(`/goals/get_goal/${id}`);
    }
};