import {Link} from "react-router-dom";
import {useMemo} from "react";

export type GoalCardData = {
    id: string;
    title: string;
    author: string;
    deadline: string | Date;
    status: string;
    pool: { total: number; support: number; against: number };
};

type Props = {
    data: GoalCardData;
    to?: string;
    className?: string;
}

function clampPct(x: number) {
    if (!Number.isFinite(x)) return 0;
    return Math.max(0, Math.min(100, x));
}

function formatDate(d: string | Date) {
    const date = typeof d === "string" ? new Date(d) : d;
    return date.toLocaleDateString(undefined, {
            year: "numeric",
            month: "short",
            day: "numeric",
        }
    )
}

const statusColor: Record<GoalCardData['status'], string> = {
    OPEN: "bg-blue-500/20 text-blue-300 border-blue-400/40",
    SUCCESS: "bg-green-600/20 text-green-300 border-green-500/40",
    FAIL: "bg-red-600/20 text-red-300 border-red-500/40",
    SETTLED: "bg-gray-600/20 text-gray-300 border-gray-400/40",
}

export default function GoalCard({data, to, className}: Props) {
    const author = data.author || "Anonymous";

    const {supportPct, againstPct} = useMemo(() => {
        const denom = data.pool.support + data.pool.against;
        const s = denom > 0 ? data.pool.support / denom * 100 : 50; // if there is no bet, center it
        const sp = clampPct(s);
        return {supportPct: sp, againstPct: clampPct(100 - sp)};
    }, [data.pool.support, data.pool.against]);

    const href = to ?? `/goals/${data.id}`;

    return (
        <Link to={href} className={`block group ${className ?? ""}`} aria-label={`Open ${data.title}`}>
            <article
                className="
                          relative overflow-hidden rounded-2xl border border-gray-700 bg-gray-900/70
                          shadow-sm transition hover:shadow-lg">
                {/* Background split + divider */}
                <div className={'absolute inset-0 pointer-events-none'}>
                    {/* left (support) tint */}
                    <div className={"absolute top-0 left-0 h-full bg-green-500/10"}
                         style={{width: `${supportPct}%`}}/>
                    {/* right (against) tint */}
                    <div className={"absolute top-0 right-0 h-full bg-red-500/10"}
                         style={{width: `${againstPct}%`}}/>
                    {/* vertical divider exactly at split */}
                    <div className={"absolute top-0 left-0 h-full w-px bg-gray-700"}
                         style={{left: `${supportPct}%`, transform: "translateX(-0.5px)"}}/>
                    {/* big background percentages digits */}
                    <div className={"absolute inset-0 flex justify-between items-center px-6 select-none"}>
                        <span className={"text-6xl font-extrabold text-green-400/20"}>
                            {Math.round(supportPct)}%
                        </span>
                        <span className={"text-6xl font-extrabold text-red-400/20"}>
                            {Math.round(againstPct)}%
                        </span>
                    </div>
                </div>

                {/* Foreground content */}
                <div className={"relative p-4 sm:p-5"}>
                    <div className={"flex items-start justify-between gap-3"}>
                        <h3 className={"text-lg sm:text-xl font-semibold text-white line-clamp-2"}>
                            {data.title}
                        </h3>

                        <span className={
                            "shrink-0 border px-2 py-0.5 rounded-lg text-xs sm:text-sm " +
                            statusColor[data.status]
                        }
                              aria-label={`Status: ${data.status}`}>
                            {data.status}
                        </span>
                    </div>

                    <div className={"mt-2 text-sm text-gray-300 flex flex-wrap gap-x-4 gap-y-1"}>
                        <span>
                            Author: <span className="text-gray-100">{author}</span>
                        </span>
                        <span>
                            Deadline: <span className="text-gray-100">{formatDate(data.deadline)}</span>
                        </span>
                        <span>
                            Total pool:<span className="text-yellow-400 font-medium">{data.pool.total}</span>
                        </span>
                    </div>
                </div>
            </article>
        </Link>
    )
}