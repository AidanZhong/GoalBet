import {useNavigate, useSearchParams} from "react-router-dom";
import {useEffect, useMemo, useState} from "react";
import {login, register} from "../api/authService.ts";

type Mode = "login" | "register";

export default function Login() {
    const nav = useNavigate();
    const [params, setParams] = useSearchParams();
    const initialMode = (params.get("mode") as Mode) || "login";
    const [mode, setMode] = useState<Mode>(initialMode);

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const current = params.get("mode");
        if (current !== mode) {
            params.set("mode", mode);
            setParams(params, {replace: true});
            setError(null);
            setLoading(false);
            setEmail("");
            setPassword("");
        }
    }, [mode]);

    const title = useMemo(() => (
        mode === "login" ? "Welcome back" : "Create your account"
    ), [mode]);

    const cta = mode === "login" ? "Login" : "Register";

    const switchText = mode === "login"
        ? {question: "Don't have an account yet?", link: "Register", next: "register" as Mode}
        : {question: "Already have an account?", link: "Login", next: "login" as Mode};

    const onSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            if (mode === "login") {
                await login({email, password});
            } else {
                await register({email, password});
            }
            // if success, redirect to home
            nav("/");
        } catch (e: any) {
            setError(mode === "login" ? "Invalid email or password" : e.message || "Failed to register");
        } finally {
            setLoading(false);
        }
    };

    const canSubmit = email.trim() && password.trim();


    return (
        <div className={"min-h-[70vh] flex items-center justify-center px-4"}>
            <form
                onSubmit={onSubmit}
                className={"w-full max-w-md rounded-2xl border border-gray-700 bg-gray-900/70 p-6 shadow"}>
                {/* Heading + mode toggle chips */}
                <div className={"flex items-center justify-between"}>
                    <h1 className={"text-2xl font-bold text-white"}>{title}</h1>
                    <div className={"flex rounded-lg overflow-hidden border border-gray-700"}>
                        <button
                            type={"button"}
                            onClick={() => setMode("login")}
                            className={`
                                px-4 py-2 text-sm font-medium transition-colors
                                ${mode === "login" ? "bg-gray-800 text-white" : "bg-gray-700 text-gray-300 hover:bg-gray-600"}
                            `}
                        >
                            Login
                        </button>
                        <button
                            type={"button"}
                            onClick={() => setMode("register")}
                            className={`
                                px-4 py-2 text-sm font-medium transition-colors
                                ${mode === "register" ? "bg-gray-800 text-white" : "bg-gray-700 text-gray-300 hover:bg-gray-600"}
                            `}
                        >
                            Register
                        </button>
                    </div>
                </div>

                <p className={"mt-4 text-sm text-gray-400"}>
                    {mode === 'login' ? "Login to continue on GoalBet" : "Create an account to get started"}
                </p>

                <div className="mt-6 space-y-4">
                    <div>
                        <label className="block text-sm text-gray-300 mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            required
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"
                            placeholder="you@example.com"
                            autoComplete="email"
                        />
                    </div>

                    <div>
                        <label className={"block text-sm text-gray-300 mb-1"}>Password</label>
                        <input
                            type="password"
                            required
                            minLength={8}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full rounded-lg bg-gray-800 border border-gray-700 px-3 py-2 text-white outline-none focus:border-yellow-400"
                            placeholder={mode === "login" ? "••••••••" : "At least 8 characters"}
                            autoComplete={mode === "login" ? "current-password" : "new-password"}
                        />
                    </div>

                    {error && (
                        <div
                            className={"text-sm text-red-400 bg-red-900/20 border border-red-700/40 rounded-lg px-3 py-2"}>
                            {error}
                        </div>
                    )}

                    <button
                        type={"submit"}
                        disabled={loading || !canSubmit}
                        className={"w-full rounded-xl bg-yellow-500 text-black font-semibold py-2.5 hover:bg-yellow-600 disabled:opacity-60"}
                    >
                        {loading ? `${cta}...` : `${cta}`}
                    </button>
                </div>

                <div className={"mt-4 text-sm text-gray-400"}>
                    {switchText.question}{" "}
                    <button
                        type={"button"}
                        className={"text-yellow-400 hover:underline"}
                        onClick={() => setMode(switchText.next)}
                    >
                        {switchText.link}
                    </button>
                </div>
            </form>
        </div>
    );
}