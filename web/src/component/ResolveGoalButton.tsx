import {useState} from "react";
import {goalsService} from "../api/goalsService.ts";

type Props = {
    goalId: string | number;
    onResolved?: (outcome: "success" | "fail") => void;
    className?: string;
};

export default function ResolveGoalButton({goalId, onResolved, className}: Props) {
    const [open, setOpen] = useState(false);
    const [choice, setChoice] = useState<"success" | "fail">('fail');
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const confirm = async () => {
        setBusy(true);
        setError(null);
        try {
            await goalsService.resolve(goalId, choice);
            setOpen(false);
            onResolved?.(choice);
        } catch {
            setError("Failed to resolve goal, please try again later");
        } finally {
            setBusy(false);
        }
    };

    return (
        <>
            <button
                onClick={() => setOpen(true)}
                className={`rounded-xl border border-emerald-600 bg-emerald-500/10 text-emerald-200 hover:bg-emerald-500/20 px-3 py-1 text-sm ${className ?? ""}`}
            >
                Resolve Goal
            </button>

            {open && (
                <div className={"fixed inset-0 z-50 flex items-center justify-center"}>
                    <div className={"absolute inset-0 bg-black/60"} onClick={() => !busy && setOpen(false)}/>
                    <div
                        className={"relative w-[92%] max-w-md rounded-2xl border border-gray-700 bg-gray-900 p-5 shadow-xl"}>
                        <h3 className={"text-lg font-semibold text-white"}>Resolve goal</h3>
                        <p className={"text-sm text-gray-400 mt-1"}>Choose the final outcome.</p>
                        <div className="mt-4 grid grid-cols-2 gap-3">
                            <button
                                onClick={() => setChoice("success")}
                                className={`rounded-xl px-3 py-2 border ${choice === "success" ? "border-emerald-500 bg-emerald-500/10 text-emerald-200" : "border-gray-600 bg-gray-800/60 text-gray-200"}`}
                            >
                                Success
                            </button>
                            <button
                                onClick={() => setChoice("fail")}
                                className={`rounded-xl px-3 py-2 border ${choice === "fail" ? "border-red-500 bg-red-500/10 text-red-200" : "border-gray-600 bg-gray-800/60 text-gray-200"}`}
                            >
                                Fail
                            </button>
                        </div>
                        {error && <div
                            className="mt-3 rounded-lg border border-red-500/40 bg-red-900/20 text-red-300 px-3 py-2">{error}</div>}

                        <div className="mt-5 flex justify-end gap-3">
                            <button
                                disabled={busy}
                                onClick={() => setOpen(false)}
                                className="rounded-xl border border-gray-600 bg-transparent px-4 py-2 text-white hover:bg-gray-700 disabled:opacity-60"
                            >
                                Cancel
                            </button>
                            <button
                                disabled={busy}
                                onClick={confirm}
                                className="rounded-xl bg-yellow-500 hover:bg-yellow-600 text-black font-semibold px-4 py-2 disabled:opacity-60"
                            >
                                {busy ? "Resolving…" : "Confirm"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </>
    )
}