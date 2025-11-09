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

    return (
        <motion.nav
            className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${isScrolled ? "bg-gray-900/90 backdrop-blur shadow-lg" : "bg-transparent"}`}
            initial={{y: -40}}
            animate={{y: 0}}
        >
            <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between text-white">
                <h1 className="font-bold text-xl tracking-wide text-yellow-400">GoalBet</h1>
            </div>

            <div className="flex gap-6">
                {links.map((link) => (
                    <Link
                        key={link.to}
                        to={link.to}
                        className={`hover:text-yellow-400 transition-colors duration-300 ${location.pathname === link.to ? "text-yellow-300" : ""}`}
                    >
                        {link.text}
                    </Link>
                ))}
            </div>
        </motion.nav>
    )
}