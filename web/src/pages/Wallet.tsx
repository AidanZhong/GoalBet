import {useEffect, useState} from "react";
import {type WalletDTO, walletService} from "../api/walletService.ts";
import {useNavigate} from "react-router-dom";
import Cookies from "js-cookie";

export default function Wallet() {
    const nav = useNavigate();

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [balance, setBalance] = useState<number>(0);

    useEffect(() => {
        let mounted = true;
        (async () => {
            try {
                setLoading(true);
                setError(null);

                // first verify if user is logged in
                const hasToken = !!Cookies.get("access_token");
                if (!hasToken) {
                    nav("/auth?mode=login");
                    return;
                }

                const [balanceRes] = await Promise.all([
                    walletService.getBalance()
                ]);

                if (!mounted) return;

                setBalance((balanceRes.data as WalletDTO).balance ?? 0);
            } catch (_e) {
                if (!mounted) return;
                setError("Failed to load wallet");
            } finally {
                if (mounted) setLoading(false);
            }
        })();

        return () => {
            mounted = false;
        };
    }, [nav]);

    return (
        <div className={"max-w-3xl mx-auto px-4 py-6 space-y-6"}>
            <div className={"flex items-center justify-between"}>
                <h1 className={"text-2xl font-bold"}>
                    Wallet
                </h1>
            </div>

            {error && (
                <div className={"rounded-xl border border-red-500/40 bg-red-900/20 text-red-300 px-4 py-3"}>
                    {error}
                </div>
            )}

            <section className={"rounded-2xl border border-gray-700 bg-gray-900/70 p-6"}>
                <div className={"text-gray-300"}>Current balance</div>
                <div className={"mt-2 text-5xl font-extrabold"}>
                    {loading ? "-" : balance}
                    <span className={"ml-2 text-xl font-semibold text-gray-400"}>coins</span>
                </div>
            </section>
        </div>
    )
}