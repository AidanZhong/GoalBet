import axiosClient from "./axiosClient";

export async function getCurrentUser() {
    const response = await axiosClient.get("/auth/me");
    return response.data;
}