import {useEffect, useState} from "react";
import {type LeaderboardEntry, getLeaderboard} from "../api/userService.ts";
import Cookies from "js-cookie";
import {getCurrentUser} from "../api/userService.ts";

const MEDALS = ["🥇", "🥈", "🥉"];

export default function Leaderboard() {
    const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [myEmail, setMyEmail] = useState<string | null>(null);

    const isLoggedIn = !!Cookies.get("access_token");

    useEffect(() => {
        if (isLoggedIn) {
            getCurrentUser().then((u) => setMyEmail(u?.email ?? null));
        }
    }, [isLoggedIn]);

    useEffect(() => {
        (async () => {
            try {
                const res = await getLeaderboard();
                setEntries(res.data);
            } catch {
                setError("Failed to load leaderboard");
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    return (
        <div className="max-w-2xl mx-auto px-4 py-8">
            <h1 className="text-2xl font-bold mb-2 text-center">Leaderboard</h1>
            <p className="text-sm text-gray-400 text-center mb-6">Top 50 players ranked by coins</p>

            {loading && (
                <div className="space-y-2">
                    {Array.from({length: 8}).map((_, i) => (
                        <div key={i} className="h-12 rounded-xl bg-gray-800/60 animate-pulse"/>
                    ))}
                </div>
            )}

            {error && (
                <div className="rounded-xl border border-red-500/40 bg-red-900/20 text-red-300 px-4 py-3">{error}</div>
            )}

            {!loading && !error && (
                <div className="rounded-2xl border border-gray-700 bg-gray-900/70 overflow-hidden">
                    <table className="w-full text-sm">
                        <thead>
                        <tr className="border-b border-gray-700 text-gray-400 text-left">
                            <th className="px-4 py-3 w-12">Rank</th>
                            <th className="px-4 py-3">Player</th>
                            <th className="px-4 py-3 text-right">Coins</th>
                        </tr>
                        </thead>
                        <tbody>
                        {entries.map((e) => {
                            const isMe = e.email === myEmail;
                            return (
                                <tr
                                    key={e.rank}
                                    className={[
                                        "border-b border-gray-800 last:border-0 transition-colors",
                                        isMe ? "bg-yellow-500/10" : "hover:bg-gray-800/40",
                                    ].join(" ")}
                                >
                                    <td className="px-4 py-3 text-center font-semibold">
                                        {e.rank <= 3 ? MEDALS[e.rank - 1] : e.rank}
                                    </td>
                                    <td className="px-4 py-3 text-gray-100">
                                        {e.email}
                                        {isMe && (
                                            <span className="ml-2 text-xs text-yellow-400 font-medium">you</span>
                                        )}
                                    </td>
                                    <td className="px-4 py-3 text-right font-semibold text-yellow-400">
                                        {e.balance.toLocaleString()}
                                    </td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>

                    {entries.length === 0 && (
                        <p className="text-center text-gray-500 py-8">No players yet.</p>
                    )}
                </div>
            )}
        </div>
    );
}
