import Cookies from "js-cookie";
import {Link, useLocation} from "react-router-dom";
import {motion, useScroll} from "framer-motion";
import {useEffect, useState} from "react";

export default function Navbar() {
    const {scrollY} = useScroll();
    const [isScrolled, setIsScrolled] = useState(false);
    const [menuOpen, setMenuOpen] = useState(false);
    const location = useLocation();
    const accessToken = Cookies.get("access_token");
    const isLoggedIn = !!accessToken && accessToken !== "undefined" && accessToken !== "null";

    useEffect(() => {
        return scrollY.onChange((latest) => setIsScrolled(latest > 20));
    }, [scrollY]);

    useEffect(() => {
        setMenuOpen(false);
    }, [location.pathname]);

    const links = isLoggedIn ? [
        {to: "/", text: "Home"},
        {to: "/about", text: "About"},
        {to: "/goals", text: "Goals"},
        {to: "/leaderboard", text: "Leaderboard"},
        {to: "/wallet", text: "Wallet"},
    ] : [
        {to: "/about", text: "About"},
        {to: "/goals", text: "Goals"},
        {to: "/leaderboard", text: "Leaderboard"},
        {to: "/login", text: "Login"},
    ];

    const isActive = (to: string) =>
        location.pathname === to || (to !== "/" && location.pathname.startsWith(to));

    return (
        <motion.nav className="sticky top-3 z-50 px-4" initial={{y: -40}} animate={{y: 0}}>
            <div className="mx-auto max-w-7xl">
                {/* pill bar */}
                <div className={[
                    "flex items-center gap-3",
                    "rounded-[26px] border border-gray-700",
                    "px-3 sm:px-4 py-2",
                    isScrolled ? "bg-gray-900/80 backdrop-blur shadow-lg" : "bg-gray-900/60",
                ].join(" ")}>

                    <Link to="/" aria-label="GoalBet Home" className="shrink-0">
                        <img src="/images/logo.png" alt="logo" className="h-10 w-10 sm:h-12 sm:w-12"/>
                    </Link>

                    <Link to="/" className="shrink-0 text-lg sm:text-xl font-semibold text-white">
                        GoalBet
                    </Link>

                    {/* desktop links */}
                    <nav className="flex-1 hidden md:flex items-center gap-1">
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

                    <div className="flex-1 md:hidden"/>

                    {/* hamburger button */}
                    <button
                        className="md:hidden p-2 rounded-xl text-gray-300 hover:text-white hover:bg-gray-800/70"
                        onClick={() => setMenuOpen((o) => !o)}
                        aria-label="Toggle menu"
                    >
                        {menuOpen ? (
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12"/>
                            </svg>
                        ) : (
                            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16"/>
                            </svg>
                        )}
                    </button>
                </div>

                {/* mobile dropdown */}
                {menuOpen && (
                    <div className="md:hidden mt-2 rounded-2xl border border-gray-700 bg-gray-900/95 backdrop-blur p-3 shadow-xl">
                        {links.map((l) => (
                            <Link
                                key={l.to}
                                to={l.to}
                                className={[
                                    "block px-4 py-3 rounded-xl text-sm transition-colors",
                                    isActive(l.to)
                                        ? "bg-gray-800/70 text-white font-medium"
                                        : "text-gray-300 hover:text-white hover:bg-gray-800/70",
                                ].join(" ")}
                            >
                                {l.text}
                            </Link>
                        ))}
                    </div>
                )}
            </div>
        </motion.nav>
    );
}
