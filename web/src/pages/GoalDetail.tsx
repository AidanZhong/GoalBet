import {useNavigate, useParams} from "react-router-dom";
import {useEffect, useMemo, useState} from "react";
import {type GoalDTO, goalsService} from "../api/goalsService.ts";
import Cookies from "js-cookie";
import {betsService} from "../api/betsService.ts";
import {normalizeMarkets} from "../utils/markets.ts";
import {getCurrentUser} from "../api/userService.ts";
import ResolveGoalButton from "../component/ResolveGoalButton.tsx";

type BetSide = "success" | "fail"

const toPrettyDate = (iso?: string) => (
    iso ? new Date(iso).toLocaleDateString() : ""
);

export default function GoalDetail() {
    const {id} = useParams<{ id: string }>();
    const nav = useNavigate();

    const [goal, setGoal] = useState<GoalDTO | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [betSide, setBetSide] = useState<BetSide | null>(null);
    const [amount, setAmount] = useState<string>("");
    const [placing, setPlacing] = useState(false);

    const [me, setMe] = useState<{ email?: string }>({email: ""});

    useEffect(() => {
        let mounted = true;
        (async () => {
            const user = await getCurrentUser();
            if (mounted) setMe(user);
        })();
        return () => {
            mounted = false;
        }
    }, []);

    const isOwner = !!me?.email && goal?.owner_email === me.email;

    const isLoggedIn = !!Cookies.get("access_token");

    const reloadGoal = async () => {
        try {
            const response = await goalsService.getById(id!);
            setGoal(response.data);
        } catch {
            // ignore error
        }
    }

    // fetch goal
    useEffect(() => {
        let mounted = true;
        (async () => {
            try {
                setLoading(true);
                setError(null);

                try {
                    const response = await goalsService.getById(id!);
                    if (!mounted) return;
                    setGoal(response.data);
                } catch {
                    const response = await goalsService.list();
                    if (!mounted) return;
                    const g = (response.data ?? []).find((x) => String(x.id) === id);
                    if (!g) throw new Error("Goal not found");
                    setGoal(g);
                }
            } catch (_e) {
                if (!mounted) return;
                setError("Failed to load goal");
            } finally {
                if (mounted) setLoading(false);
            }
        })();

        return () => {
            mounted = false
        };
    }, [id]);

    const pools = useMemo(() => {
        const {support, against, total} = normalizeMarkets(goal?.markets);
        const sp = total > 0 ? Math.round((support / total) * 100) : 50;
        const ap = total > 0 ? Math.round((against / total) * 100) : 50;
        return {support, against, total, sp, ap};
    }, [goal]);

    const isActive = goal?.status === "active";

    const startBet = (side: BetSide) => {
        setBetSide(side);
        setAmount("");
    };

    const cancelBet = () => {
        setBetSide(null);
        setAmount("");
    };

    const submitBet = async () => {
        if (!goal || !betSide) return;

        const num = Number(amount);
        if (!isFinite(num) || num <= 0) {
            setError("Please enter a valid amount");
            return;
        }

        if (!isLoggedIn) {
            nav("/auth?mode=login");
            return;
        }

        setPlacing(true);
        setError(null);

        try {
            const sideForApi = betSide;
            await betsService.placeBet(goal.id, {side: sideForApi, amount: num});

            try {
                const response = await goalsService.getById(goal.id);
                setGoal(response.data);
            } catch {

            }
            cancelBet();
        } catch (_e) {
            setError("Failed to place bet");
        } finally {
            setPlacing(false);
        }
    };

    if (loading) {
        return (
            <div className={"max-w-3xl mx-auto px-4 py-6"}>
                <div className={"h-36 rounded-2xl bg-gray-800/60 border border-gray-700 animate-pulse"}/>
            </div>
        );
    }

    if (error && !goal) {
        return (
            <div className="max-w-3xl mx-auto px-4 py-6">
                <div className="rounded-xl border border-red-500/40 bg-red-900/20 text-red-300 px-4 py-3">{error}</div>
            </div>
        );
    }

    if (!goal) {
        return null;
    }

    return (
        <div className={"max-w-3xl mx-auto px-4 py-6"}>
            {/*header*/}
            <div className={"rounded-2xl border border-gray-700 bg-gray-900/70 p-5 relative"}>
                <h1 className="text-2xl font-bold text-white">{goal.title}</h1>
                <p className="text-sm text-gray-400 mt-1">by {goal.owner_email}</p>

                {/* resolve button */}
                {isOwner && isActive && (
                    <ResolveGoalButton goalId={goal.id}
                                       onResolved={() => reloadGoal()}
                                       className={"absolute right-5 top-5"}
                    />
                )}

                <div className={"mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm"}>
                    <div className={"space-y-1"}>
                        <div>
                            <span
                                className={"text-gray-400"}>Deadline:
                            </span>
                            <span
                                className="text-gray-100">{toPrettyDate(goal.deadline)}
                            </span>
                        </div>
                        <div>
                            <span
                                className={"text-gray-400"}>Status:
                            </span>
                            <span
                                className={"text-gray-100"}>{goal.status}
                            </span>
                        </div>
                        <div>
                            <span
                                className={"text-gray-400"}>Updates:
                            </span>
                            <span
                                className={"text-gray-100"}>{Array.isArray(goal.updates) ? goal.updates.length : 0}
                            </span>
                        </div>
                    </div>
                    <div className={"space-y-1"}>
                        <div>
                            <span
                                className={"text-gray-400"}>Supports:
                            </span>
                            <span
                                className={"text-gray-100"}>{pools.support}
                            </span>
                        </div>
                        <div>
                            <span
                                className={"text-gray-400"}>Against:
                            </span>
                            <span
                                className={"text-gray-100"}>{pools.against}
                            </span>
                        </div>
                        <div>
                            <span
                                className={"text-gray-400"}>Total pool:
                            </span>
                            <span
                                className={"text-gray-100"}>{pools.total}
                            </span>
                        </div>
                    </div>
                </div>

                {/*description*/}
                <div className={"mt-4"}>
                    <div className={"text-sm text-gray-400 mb-1"}>Description</div>
                    <div
                        className={"rounded-lg border border-gray-700 bg-gray-800/60 p-3 text-gray-100 whitespace-pre-wrap"}>
                        {goal.description || "—"}
                    </div>
                </div>

                {/*split bar*/}
                <div className={"mt-4"}>
                    <div className="h-2 w-full rounded bg-gray-800 overflow-hidden border border-gray-700">
                        <div
                            className="h-full bg-green-600"
                            style={{width: `${pools.sp}%`}}
                            title={`Support ${pools.sp}%`}
                        />
                    </div>
                    <div className="mt-1 text-[11px] text-gray-400 flex justify-between">
                        <span>Support {pools.sp}%</span>
                        <span>Against {pools.ap}%</span>
                    </div>
                </div>

                {/* error banner */}
                {error && (
                    <div className="mt-3 rounded-lg border border-red-500/40 bg-red-900/20 text-red-300 px-3 py-2">
                        {error}
                    </div>
                )}

                {/* bet buttons*/}
                {isActive ? (
                    <div className={"mt-5"}>
                        {!betSide ? (<div className={"flex flex-wrap gap-3"}>
                                <button
                                    onClick={() => startBet("success")}
                                    className={"rounded-xl border border-gray-600 bg-gray-800/60 px-4 py-2 text-white hover:bg-gray-700"}
                                >
                                    Bet on success
                                </button>
                                <button
                                    onClick={() => startBet("fail")}
                                    className={"rounded-xl border border-gray-600 bg-gray-800/60 px-4 py-2 text-white hover:bg-gray-700"}
                                >
                                    Bet on failure
                                </button>
                            </div>

                        ) : (
                            <div className={"rounded-xl border border-gray-700 bg-gray-800/60 p-4"}>
                                <div className={"text-sm text-gray-300 mb-2"}>
                                    You’re betting on <span className="font-semibold">{betSide}</span>.
                                </div>
                                <div className={"flex items-center gap-3"}>
                                    <input
                                        type={"number"}
                                        min={1}
                                        step="1"
                                        value={amount}
                                        onChange={(e) => setAmount(e.target.value)}
                                        placeholder={"Amount"}
                                        className={"w-44 rounded-lg bg-gray-900 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"}
                                    />
                                    <button
                                        disabled={placing}
                                        onClick={submitBet}
                                        className={"rounded-xl bg-yellow-500 hover:bg-yellow-600 text-black font-semibold px-4 py-2 disabled:opacity-60"}
                                    >
                                        {placing ? "Placing..." : "Place bet"}
                                    </button>
                                    <button
                                        disabled={placing}
                                        onClick={cancelBet}
                                        className={"rounded-xl border border-gray-600 bg-transparent px-4 py-2 text-white hover:bg-gray-700 disabled:opacity-60"}
                                    >
                                        Cancel
                                    </button>
                                </div>

                                {!isLoggedIn && (
                                    <div className={"mt-2 text-xs text-yellow-200"}>
                                        You need to be logged in to place a bet.{" "} <a href={"/auth?mode=login"}
                                                                                         className={"underline"}>Login</a>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ) : (
                    <div className="mt-5 text-sm text-gray-400">Betting is closed for this goal.</div>
                )}
            </div>
        </div>
    );

}