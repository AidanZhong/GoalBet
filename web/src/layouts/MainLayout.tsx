import Navbar from "../component/Navbar.tsx";
import Background from "../component/Background.tsx";
import {useLocation} from "react-router-dom";

export default function MainLayout({children}: { children: React.ReactNode }) {
    const location = useLocation();

    const backgrounds: Record<string, string> = {
        "/": "/images/goalbet_logo_black_bg.png",
        "/about": "/images/goalbet_logo_black_bg.png",
        "/goals": "/images/goalbet_logo_black_bg.png",
        "/wallet": "/images/goalbet_logo_black_bg.png",
        "/login": "/images/goalbet_logo_black_bg.png",
    };

    const currentBg = backgrounds[location.pathname] || "/images/goalbet_logo_black_bg.png";

    return (
        <div className="min-h-screen text-white relative overflow-hidden">
            <Background image={currentBg}/>
            <header className={"relative z-10"}>
                <Navbar/>
            </header>
            <main className="pt-20"> {children} </main>
        </div>
    )
}