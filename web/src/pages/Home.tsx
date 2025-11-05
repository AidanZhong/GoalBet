import {type GoalDTO, goalsService} from "../api/goalsService.ts";
import GoalCard, {type GoalCardData} from "../component/GoalCard.tsx";
import {useEffect, useState} from "react";
import {getCurrentUser} from "../api/userService.ts";
import {toCard} from "./Goals.tsx";
import {type BetDTO, betsService} from "../api/betsService.ts";
import CollapsibleList from "../component/CollapsibleList.tsx";
import BetCard from "../component/BetCard.tsx";

export default function Home() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [me, setMe] = useState<{ email?: string }>({email: ""});
    const [myGoals, setMyGoals] = useState<GoalCardData[]>([]);
    const [myBets, setMyBets] = useState<BetDTO[]>([]);
    const [goalMap, setGoalMap] = useState<Map<string, GoalDTO>>(new Map());

    useEffect(() => {
        let mounted = true;
        (async () => {
            try {
                setLoading(true);
                setError(null);
                setMe(await getCurrentUser());

                const [mineGoalsRes, mineBetsRes, allGoalsRes] = await Promise.all([
                    goalsService.listMine(),
                    betsService.listMyBets(),
                    goalsService.list(),
                ]);

                if (!mounted) return;

                const myGoals = (mineGoalsRes.data ?? []).map(toCard);
                const myBets = (mineBetsRes.data ?? []) as BetDTO[];
                const allGoals = (allGoalsRes.data ?? []) as GoalDTO[];
                const goalMap = new Map(allGoals.map((g) => [String(g.id), g]));

                setMyGoals(myGoals);
                setMyBets(myBets);
                setGoalMap(goalMap);
            } catch (_e) {
                if (!mounted) return;
                setError("Failed to load goals");
            } finally {
                if (mounted) setLoading(false);
            }
        })();

        return () => {
            mounted = false;
        };
    }, []);

    return (
        <div className={"max-w-3xl mx-auto px-4 py-6 space-y-6"}>
            <h1 className={"text-2xl font-bold"}>
                Hi {me?.email ?? "there"},
            </h1>
            {error && (
                <div className={"rounded-xl border border-red-500/40 bg-red-900/20 text-red-300 px-4 py-3"}>
                    {error}
                </div>
            )}

            {/** My Goals */}
            <CollapsibleList title={"Your Goals"} defaultOpen count={myGoals.length}>
                {loading ? (
                    <div className={"h-24 rounded-2xl bg-gray-800/60 border border-gray-700 animate-pulse"}/>
                ) : myGoals.length === 0 ? (
                    <div className={"text-gray-300"}>
                        You haven't created any goals yet.{" "}
                        <a className={"underline"} href={"/goals/create"}>
                            Create one now!
                        </a>
                        .
                    </div>
                ) : (
                    <div className={"space-y-4"}>
                        {myGoals.map((g) => (
                            <GoalCard key={g.id} data={g}/>
                        ))}
                    </div>
                )}
            </CollapsibleList>

            {/** My Bets */}
            <CollapsibleList title={"Your Bets"} defaultOpen count={myBets.length}>
                {loading ? (
                    <div className={"h-24 rounded-2xl bg-gray-800/60 border border-gray-700 animate-pulse"}/>
                ) : myBets.length === 0 ? (
                    <div className={"text-gray-300"}>
                        You haven't placed any bets yet.{" "}
                        <a className={"underline"} href={"/goals"}>
                            Explore goals
                        </a>
                        to place one.
                    </div>
                ) : (
                    <div className={"space-y-4"}>
                        {myBets.map((b) => (
                            <BetCard
                                key={String(b.id)}
                                bet={{
                                    id: b.id,
                                    goal_id: b.goal_id,
                                    side: b.side,
                                    amount: b.amount,
                                    odds_snapshot: b.odds_snapshot,
                                    status: b.status,
                                    payout: b.payout,
                                }}
                                goal={goalMap.get(String(b.goal_id))}
                            />
                        ))}
                    </div>
                )
                }
            </CollapsibleList>
        </div>
    )
}