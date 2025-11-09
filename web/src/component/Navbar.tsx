import Cookies from "js-cookie";
import {Link, useLocation} from "react-router-dom";
import {motion, useScroll} from "framer-motion";
import {useEffect, useState} from "react";

export default function Navbar() {
    const {scrollY} = useScroll();
    const [isScrolled, setIsScrolled] = useState(false);
    const location = useLocation();
    const accessToken = Cookies.get("access_token");
    const isLoggedIn = !!accessToken && accessToken !== "undefined" && accessToken !== "null";

    useEffect(() => {
        return scrollY.onChange((latest) => setIsScrolled(latest > 20));
    }, [scrollY]);

    const links = isLoggedIn ? [
        {to: "/", text: "Home"},
        {to: "/about", text: "About"},
        {to: "/goals", text: "Goals"},
        {to: "/wallet", text: "Wallet"},
    ] : [
        {to: "/about", text: "About"},
        {to: "/goals", text: "Goals"},
        {to: "/login", text: "Login"},
    ];

    const isActive = (to: string) =>
        location.pathname === to || (to !== "/" && location.pathname.startsWith(to));

    return (
        <motion.nav
            className="sticky top-3 z-50 px-4"
            initial={{y: -40}}
            animate={{y: 0}}
        >
            <div className="mx-auto max-w-7xl">
                {/* pill container */}
                <div
                    className={[
                        "flex items-center gap-3 sm:gap-4",
                        "rounded-[26px] border border-gray-700",
                        "px-3 sm:px-4 py-2",
                        isScrolled ? "bg-gray-900/80 backdrop-blur shadow-lg" : "bg-gray-900/60",
                    ].join(" ")}
                >
                    {/* logo box */}
                    <Link
                        to="/"
                        aria-label="GoalBet Home"
                        className="shrink-0"
                    >
                        <img
                            src="/images/logo.png"
                            alt="logo"
                            className="h-10 w-10 sm:h-12 sm:w-12"
                        />
                    </Link>

                    {/* brand */}
                    <Link
                        to="/"
                        className="mr-1 sm:mr-3 text-lg sm:text-xl font-semibold text-white"
                    >
                        GoalBet
                    </Link>

                    {/* inline links */}
                    <nav className="flex-1 flex items-center gap-1 sm:gap-2">
                        {links.map((l) => (
                            <Link
                                key={l.to}
                                to={l.to}
                                className={[
                                    "px-3 py-2 rounded-xl text-sm transition-colors",
                                    isActive(l.to)
                                        ? "bg-gray-800/70 text-white"
                                        : "text-gray-300 hover:text-white hover:bg-gray-800/70",
                                ].join(" ")}
                            >
                                {l.text}
                            </Link>
                        ))}
                    </nav>
                </div>
            </div>
        </motion.nav>
    );
}