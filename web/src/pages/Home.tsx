import {motion} from "framer-motion";

export default function Home() {
    return (
        <motion.div
            className="h-[80vh] flex flex-col justify-center items-center text-center relative"
            initial={{opacity: 0, y: 40}}
            animate={{opacity: 1, y: 0}}
            transition={{duration: 1}}
        >
            <div className="absolute inset-0 bg-black/40 -z-10"/>

            <h1 className="text-5xl font-extrabold text-yellow-400 drop-shadow-lg">
                Set Goals, Bet Accountability.
            </h1>

            <p className="mt-4 text-lg text-gray-300 max-w-2xl">
                Where goals meet motivation - powered by the crowd.
            </p>
        </motion.div>
    )
}
import {register} from "../api/authService";

async function handleRegister() {
    await register({email: "test@goalbet.com", password: "1234"});
    console.log("✅ Logged in successfully!");
}

handleRegister();