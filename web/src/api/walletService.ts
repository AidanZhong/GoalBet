import axiosClient from "./axiosClient.ts";

export type WalletDTO = {
    balance: number;
}

export const walletService = {
    getBalance() {
        return axiosClient.get<WalletDTO>("/wallet");
    }
}