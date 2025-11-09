import {Link} from "react-router-dom";

function SectionCard({
                         title,
                         emoji,
                         children,
                         className = "",
                     }: {
    title: string,
    emoji?: string,
    children: React.ReactNode,
    className?: string,
}) {
    const BASE_SECTION_CLASS = "rounded-2xl border border-gray-700 bg-gray-900/70 p-6 md:p-8";
    return (
        <section className={`${BASE_SECTION_CLASS} ${className}`}>
            <h2 className={"text-xl md:text-2xl font-bold text-white flex items-center gap-2"}>
                {emoji ? <span className={"text-2xl"}>{emoji}</span> : null}
                {title}
            </h2>
            <div className={"mt-4 text-gray-200 leading-relaxed"}>{children}</div>
        </section>
    );
}

export default function About() {
    return (
        <div className={"max-w-4xl mx-auto px-4 py-10 space-y-8"}>
            {/* Header */}
            <header className={"text-center space-y-6"}>
                <blockquote className={"text-2xl md:text-3xl font-extrabold text-white"}>
                    "Everybody dies, but few really live. Start with a goal - and let the world watch you win."
                </blockquote>

                <div className={"mx-auto max-w-3xl text-gray-300 leading-relaxed"}>
                    <p>
                        GoalBet is a platform that allows users to create and track their goals.
                        It turns your personal goals into a public game, where people can bet for or against you.
                        Post your goal, stake coins, let others bet, and prove you can make it happen!!!
                    </p>
                    <p className={"mt-2"}>
                        When you succeed, you win - not only just rewards, but also respect.
                    </p>
                </div>

                <div>
                    <Link to={'/goals'}
                          className={"inline-flex items-center gap-2 rounded-xl bg-yellow-500 hover:bg-yellow-600 text-black font-semibold px-5 py-3 shadow-md"}
                    >
                        <span>🎯</span> Explore Goals
                    </Link>
                </div>
            </header>

            {/* Section 1: Why we exist */}
            <SectionCard title={"Why We Exist"} emoji="💡">
                <h3 className={"font-semibold text-white mb-2"}>
                    Why most people fail their goals?
                </h3>
                <p>
                    Most people fail not because they're lazy, but because the goal lacks of accountability.
                    When you're alone, motivation fades away. You can quit without any cost.
                </p>
                <p className={"mt-2"}>
                    But when others are watching, cheering, or even doubting -- you push harder.
                    GoalBet exists to make that pressure fun, rewarding, and social.
                </p>
            </SectionCard>

            {/* Section 2: How it works */}
            <SectionCard title={"How it works"} emoji={"⚙️"}>
                <div className={"grid grid-cols-1 gap-4"}>
                    {[
                        {
                            step: 1,
                            action: "Set your goal",
                            description: "Create a goal that you want to achieve. It can be anything from a simple task to a complex project. -- fitness, study, career, etc.",
                        },
                        {
                            step: 2,
                            action: "Stake coins",
                            description: "This is your commitment to the goal.",
                        },
                        {
                            step: 3,
                            action: "Let the community bet",
                            description: "People can bet for or against you -- supporters and doubters make it exciting.",
                        },
                        {
                            step: 4,
                            action: "Upload proof and win",
                            description: "Complete your goal, submit your proof, and claim your victory.",
                        },
                    ].map((row) => (
                        <div
                            key={row.step}
                            className={"rounded-xl border border-gray-700 bg-gray-800/60 p-4 md:p-5 flex items-start gap-4"}>
                            <div className={"shrink-0"}>
                                <span
                                    className={"h-8 w-8 grid place-items-center justify-center rounded-lg bg-gray-900 border border-gray-700 text-sm font-bold text-gray-200"}>
                                    {row.step}
                                </span>
                            </div>
                            <div className={"text-left flex-1 space-y-1"}>
                                <div className={"font-semibold text-white"}>{row.action}</div>
                                <div className={"text-gray-300 text-sm mt-1"}>{row.description}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </SectionCard>

            {/* Section 3: The coin economy */}
            {/* Section 4: Join the movement */}
        </div>
    )
}