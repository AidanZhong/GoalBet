import GoalCard, {type GoalCardData} from "../component/GoalCard.tsx";
import {type GoalDTO, goalsService, type MarketsDTO} from "../api/goalsService.ts";
import Cookies from "js-cookie";
import {useEffect, useMemo, useState} from "react";

type FetchState =
    | { kind: "idle" | "loading" }
    | { kind: "error"; message: string }
    | { kind: "loaded"; items: GoalCardData[] };

function toPools(market: MarketsDTO | any) {
    if (!market) return {support: 0, against: 0, total: 0};
    const support = Number(market.support ?? 0);
    const against = Number(market.against ?? 0);
    const total = Number(market.total ?? support + against);
    return {support, against, total};
}

export const toCard = (g: GoalDTO): GoalCardData => {
    return {
        id: String(g.id),
        title: g.title,
        author: g.owner_email,
        deadline: g.deadline,
        status: g.status,
        pool: toPools(g.markets),
    };
};

export default function Goals() {
    const isLoggedIn = !!Cookies.get("access_token");
    const [state, setState] = useState<FetchState>({kind: "idle"});

    useEffect(() => {
        let mounted = true;
        setState({kind: "loading"});

        goalsService
            .list()
            .then((response) => {
                if (!mounted) return;
                const items = (response.data ?? []).map(toCard);
                setState({kind: "loaded", items});
            })
            .catch(() => {
                if (!mounted) return;
                setState({kind: "error", message: "Failed to load goals"});
            });
        return () => {
            mounted = false;
        };
    }, []);

    const content = useMemo(() => {
        if (state.kind === "idle" || state.kind === "loading") {
            return (
                <div className={"space-y-4"}>
                    {Array.from({length: 4}).map((_, i) => (
                        <div key={i} className="h-32 rounded-2xl bg-gray-800/60 border border-gray-700 animate-pulse"/>
                    ))}
                </div>
            );
        }

        if (state.kind === "error") {
            return (
                <div className={"rounded-xl border border-red-500/40 bg-red-900/20 text-red-300 px-4 py-3"}>
                    {state.message}
                </div>
            );
        }

        if (state.kind !== "loaded") {
            // This should never happen, but TypeScript doesn't know that.
            return null;
        }

        if (state.items.length === 0) {
            return <div className={"text-gray-300"}>No goals yet.</div>;
        }

        return (
            <div className={"space-y-4"}>
                {state.items.map((item) => (
                    <GoalCard key={item.id} data={item} className={"hover:shadow-lg"}/>
                ))}
            </div>
        );
    }, [state]);

    return (
        <div className={"max-w-3xl mx-auto px-4 py-6"}>
            {!isLoggedIn && (
                <div className="mb-6 rounded-xl border border-yellow-500/40 bg-yellow-500/10 text-yellow-100 px-4 py-3">
                    Hi there, you haven't logged in yet. {" "}
                    <a href={"/auth?mode=login"} className="underline">Login</a> {" "} to place a bet or start your own
                    goals.
                </div>
            )}
            <h1 className={"text-2xl font-bold mb-4"}>All Goals</h1>
            {content}
        </div>
    );
}