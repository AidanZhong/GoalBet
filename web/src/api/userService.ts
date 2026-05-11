import axiosClient from "./axiosClient";
import Cookies from "js-cookie";

export async function getCurrentUser() {
    try{
        const response = await axiosClient.get("/auth/me");
        return response.data;
    } catch (error) {
        console.error("Error fetching current user:", error);
        Cookies.remove("access_token");
        return null;
    }
}

export type LeaderboardEntry = {
    rank: number;
    email: string;
    balance: number;
};

export function getLeaderboard() {
    return axiosClient.get<LeaderboardEntry[]>("/users/leaderboard");
}