import {normalizeMarkets} from "../utils/markets.ts";

export type BetCardProps = {
    bet: {
        id: string | number;
        goal_id: string | number;
        side: string;
        amount: number;
        odds_snapshot?: number | null;
        status: string;
        payout?: number | null;
    };
    goal?: {
        id: string | number;
        title?: string;
        owner_email?: string;
        deadline?: string;
        status?: string;
        markets?: { support?: number; against?: number; total?: number };
    };
    className?: string;
};

const pillFromStatus = (s?: string) => {
    const base = "text-xs px-2 py-0.5 rounded-lg border";
    if (!s) return `${base} border-gray-600 text-gray-300`;
    const k = s.toLowerCase();
    if (k === "won" || k === "success" || k === "settled")
        return `${base} border-green-600 text-green-300`;
    if (k === "lost" || k === "fail")
        return `${base} border-red-600 text-red-300`;
    return `${base} border-gray-600 text-gray-300`;
};

const prettySide = (side: string) => {
    const k = side?.toLowerCase();
    if (k === "success" || k === "support") return "Support";
    if (k === "failure" || k === "against") return "Against";
    return side || "—";
};


const prettyDate = (iso?: string) =>
    iso ? new Date(iso).toLocaleString() : "—";

export default function BetCard({bet, goal, className = ""}: BetCardProps) {
    const {support, against, total} = normalizeMarkets(goal?.markets)
    const supportPct = total > 0 ? Math.round((support / total) * 100) : 50;
    const againstPct = total > 0 ? Math.round((against / total) * 100) : 50;

    return (
        <article className={`rounded-2xl border border-gray-700 bg-gray-900/70 p-4 ${className}`}>
            <div className={"flex items-start justify-between"}>
                <div>
                    <h3 className={"text-lg font-semibold text-white"}>
                        {goal?.title || `Goal #${bet.goal_id}`}
                    </h3>
                    <p className={"text-xs text-gray-400"}>
                        {goal?.owner_email ? <>by {goal.owner_email} • </> : null}
                        Deadline: {prettyDate(goal?.deadline)}
                    </p>
                </div>
                <span className={pillFromStatus(bet.status)}>
                    {bet.status}
                </span>
            </div>
            {/* Market split visual */}/
            <div className={"mt-3"}>
                <div className={"h-2 w-full rounded bg-gray-800 overflow-hidden border border-gray-700"}>
                    <div
                        className={"h-full bg-green-600"}
                        style={{width: `${supportPct}%`}}
                        aria-label={`Support share`}
                        title={`Support: ${supportPct}%`}/>
                </div>
                <div className={"mt-1 text-[11px] text-gray-400 flex justify-between"}>
                    <span>Support {supportPct}%</span>
                    <span>Against {againstPct}%</span>
                </div>
            </div>
            {/* Bet details */}
            <div className="mt-3 text-sm text-gray-200 flex flex-wrap gap-x-4 gap-y-1">
                <span>
                    Side:<span className="font-medium">{prettySide(bet.side)}</span>
                </span>
                <span>
                    Amount:<span className={"text-yellow-400 font-semibold"}>{bet.amount}</span>
                </span>
                {bet.odds_snapshot != null && (
                    <span>
                        Odds:<span className={"font-medium"}>{bet.odds_snapshot}</span>
                    </span>
                )}
                {bet.payout != null && (
                    <span>
                        Payout:<span className={"text-green-400 font-semibold"}>{bet.payout}</span>
                    </span>
                )}
            </div>
            <a
                href={`/goals/${bet.goal_id}`}
                className={"mt-3 inline-block text-xs text-gray-300 hover:text-white hover:underline"}
            >
                View goal details
            </a>
        </article>
    );
}