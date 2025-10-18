import {Link} from 'react-router-dom'

export default function MainLayout({children}: { children: React.ReactNode }) {
    return (
        <div className="min-h-screen bg-gray-900 text-white">
            <nav className="p-4 bg-gray-800 flex gap-4">
                <Link to="/" className="hover:text-yellow-400">Home</Link>
                <Link to="/about" className="hover:text-yellow-400">About</Link>
                <Link to="/goals" className="hover:text-yellow-400">Goals</Link>
                <Link to="/wallet" className="hover:text-yellow-400">Wallet</Link>
                <Link to="/login" className="hover:text-yellow-400">Login</Link>
            </nav>
            <main className="p-6"> {children} </main>
        </div>
    )
}