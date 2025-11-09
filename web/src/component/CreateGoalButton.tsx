import {Link} from "react-router-dom";
import Cookies from "js-cookie";

export default function CreateGoalButton({className = ""}: { className?: string }) {
    const hasToken = !!Cookies.get("access_token");
    const next = "/goals/create";
    const to = hasToken ? next : "/login?mode=login";

    return (
        <div className={`w-full flex justify-end ${className}`}>
            <Link
                to={to}
                className={`rounded-xl border border-yellow-400 bg-yellow-500/10 text-yellow-200 hover:bg-yellow-500/20 px-3 py-1 text-sm ${className ?? ""}`}>
                Create Goal
            </Link>
        </div>
    );
}