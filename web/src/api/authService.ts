import axiosClient from "./axiosClient.ts";
import Cookies from "js-cookie";

export interface AuthPayload {
    email: string;
    password: string;
}

export interface AuthResponse {
    access_token: string;
    token_type: string;
    user?: {
        email: string;
    };
}

export async function register(payload: AuthPayload): Promise<AuthResponse> {
    const response = await axiosClient.post<AuthResponse>("/auth/register", payload);
    Cookies.set("access_token", response.data.access_token, {expires: 7}); // Set cookie for 7 days
    return response.data;
}

export async function login(payload: AuthPayload): Promise<AuthResponse> {
    const response = await axiosClient.post<AuthResponse>("/auth/login", payload);
    Cookies.set("access_token", response.data.access_token, {expires: 7});
    return response.data;
}

export function logout(): void {
    Cookies.remove("access_token");
}