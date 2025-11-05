import axiosClient from "./axiosClient.ts";

export type BetDTO = {
    id: number | string;
    goal_id: number | string;
    user_email: string;
    side: "support" | "against";
    amount: number;
    odds_snapshot: number;
    status: string;
    payout: number | null;
}

export const betsService = {
    listForGoal(goalId: number | string) {
        return axiosClient.get<BetDTO[]>(`/markets/${goalId}/bets`);
    },

    listMyBets() {
        return axiosClient.get<BetDTO[]>("/users/bets");
    },
}