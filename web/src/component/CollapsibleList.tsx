import {type ReactNode, useId, useMemo, useState} from "react";
import {motion, AnimatePresence} from "framer-motion";

type CollapsibleListProps = {
    title: ReactNode;    // title of the collapsible list
    children: ReactNode; // contents of the collapsible list
    count?: number;
    defaultOpen?: boolean;
    isOpen?: boolean;
    onToggle?: (open: boolean) => void;
    className?: string;
};

export default function CollapsibleList({
                                            title,
                                            children,
                                            count,
                                            defaultOpen = false,
                                            isOpen,
                                            onToggle,
                                            className
                                        }: CollapsibleListProps) {
    const [internalOpen, setInternalOpen] = useState<boolean>(defaultOpen);
    const open = isOpen ?? internalOpen;

    const panelId = useId();
    const buttonId = useMemo(() => `${panelId}-btn`, [panelId]);

    const toggle = () => {
        const next = !open;
        if (onToggle) onToggle(next);
        if (isOpen === undefined) setInternalOpen(next);
    };

    const onKeyDown: React.KeyboardEventHandler<HTMLButtonElement> = (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            toggle();
        }
    };

    return (
        <section className={className}>
            {/* Header */}
            <button
                id={buttonId}
                type="button"
                onClick={toggle}
                onKeyDown={onKeyDown}
                aria-expanded={open}
                aria-controls={panelId}
                className="
                  w-full flex items-center justify-between
                  rounded-xl border border-gray-700 bg-gray-800/60
                  px-4 py-3 text-left text-white
                  hover:bg-gray-800 transition-colors
                "
            >
                <div className="flex items-center gap-3">
                    <span className="font-semibold">{title}</span>
                    {typeof count === "number" && ( // Render count if provided
                        <span
                            className="
                            inline-flex items-center justify-center
                            h-6 min-w-6 px-2 rounded-full text-xs
                            bg-yellow-500 text-black
                          "
                        >
                          {count}
                        </span>
                    )}
                </div>

                {/* Toggle Icon */}
                <motion.svg
                    viewBox="0 0 24 24"
                    className="h-6 w-6 text-gray-200"
                    initial={false}
                    animate={{rotate: open ? 180 : 0}}
                    transition={{duration: 0.3}}
                    aria-hidden="true"
                >
                    <path
                        d="M6 9l6 6 6-6"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap={"round"}
                        strokeLinejoin={"round"}
                    />
                </motion.svg>

            </button>

            {/* Content */}
            <AnimatePresence initial={false}>
                {open && (
                    <motion.div
                        id={panelId}
                        role="region"
                        aria-labelledby={buttonId}
                        initial={{height: 0, opacity: 0}}
                        animate={{height: "auto", opacity: 1}}
                        exit={{height: 0, opacity: 0}}
                        transition={{duration: 0.22}}
                        className={"overflow-hidden"}>
                        <div className={"px-1 py-3 space-y-3"}>
                            {children}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </section>
    );

}