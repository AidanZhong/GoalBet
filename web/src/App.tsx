import './App.css'
import {Route, BrowserRouter as Router, Routes} from "react-router-dom";
import MainLayout from "./layouts/MainLayout"
import Home from "./pages/Home";
import About from "./pages/About";
import Goals from "./pages/Goals";
import Wallet from "./pages/Wallet";
import Login from "./pages/Login";
import GoalCreate from "./pages/GoalCreate.tsx";
import GoalDetail from "./pages/GoalDetail.tsx";

function App() {
    return (
        <Router>
            <MainLayout>
                <Routes>
                    <Route path="/" element={<Home/>}/>
                    <Route path="/about" element={<About/>}/>
                    <Route path="/goals" element={<Goals/>}/>
                    <Route path="/wallet" element={<Wallet/>}/>
                    <Route path="/login" element={<Login/>}/>
                    <Route path="/goals/create" element={<GoalCreate/>}/>
                    <Route path="/goals/:id" element={<GoalDetail/>}/>
                </Routes>
            </MainLayout>
        </Router>
    )
}

export default App
