import {motion} from "framer-motion";

export default function Background({
                                       image,
                                       color = "rgba(0,0,0,0.8)",
                                   }: {
    image?: string;
    color?: string;
}) {
    return (
        <motion.div
            key={image || color}
            initial={{opacity: 0}}
            animate={{opacity: 1}}
            exit={{opacity: 0}}
            transition={{duration: 0.5}}
            className="fixed inset-0 z-0"
            style={{
                backgroundImage: image ? `url(${image})` : undefined,
                backgroundSize: "cover",
                backgroundPosition: "center",
                backgroundColor: image ? undefined : color,
            }
            }
        />
    );
}