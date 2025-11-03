import {useNavigate} from "react-router-dom";
import {useState} from "react";
import {goalsService} from "../api/goalsService.ts";

export default function GoalCreate() {
    const nav = useNavigate();
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [deadline, setDeadline] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        if (!title.trim() || !description.trim() || !deadline) {
            setError("Please fill in all fields");
            return;
        }

        setLoading(true);

        try {
            const iso = new Date(deadline).toISOString();
            await goalsService.create({title, description, deadline: iso});
            nav("/goals");
        } catch {
            setError("Failed to create goal, please try again later");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={"max-w-2xl mx-auto px-4 py-8"}>
            <h1 className={"text-2xl font-bold mb-6 text-center"}>Say it loud, Make it real!</h1>
            <form onSubmit={onSubmit} className={"space-y-5 rounded-2xl border border-gray-700 bg-gray-900/70 p-6"}>
                <div>
                    <label className="block text-sm text-gray-300 mb-1">Title</label>
                    <input
                        value={title} onChange={(e) => setTitle(e.target.value)}
                        placeholder="e.g., Run 5k every day"
                        className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"
                    />
                </div>
                <div>
                    <label className="block text-sm text-gray-300 mb-1">
                        Description <span className="text-xs text-gray-500">(what the goal is about and how completion is measured)</span>
                    </label>
                    <textarea
                        value={description} onChange={(e) => setDescription(e.target.value)}
                        placeholder="Describe your goal, acceptance criteria, and proof…"
                        className="min-h-[140px] w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"
                    />
                </div>
                <div>
                    <label className="block text-sm text-gray-300 mb-1">Deadline</label>
                    <input
                        type="datetime-local"
                        value={deadline} onChange={(e) => setDeadline(e.target.value)}
                        className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"
                    />
                </div>
                {error && <div
                    className="text-sm text-red-400 bg-red-900/20 border border-red-700/40 rounded-lg px-3 py-2">{error}</div>}
                <button
                    type="submit" disabled={loading}
                    className="w-full rounded-xl bg-yellow-500 text-black font-semibold py-2.5 hover:bg-yellow-600 disabled:opacity-60"
                >
                    {loading ? "Creating…" : "Create Goal"}
                </button>
            </form>
        </div>
    )
}