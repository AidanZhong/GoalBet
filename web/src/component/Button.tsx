import {Link, type LinkProps} from "react-router-dom";
import type {ButtonHTMLAttributes, ReactNode} from "react";

type Variant = "primary" | "secondary" | "ghost" | "success" | "danger" | "warning";
type Size = "sm" | "md" | "lg";

type BaseProps = {
    children: ReactNode;
    variant?: Variant;
    size?: Size;
    fullWidth?: boolean;
    loading?: boolean;
    leftIcon?: ReactNode;
    rightIcon?: ReactNode;
    className?: string;
};

type ButtonAsButton = BaseProps &
    ButtonHTMLAttributes<HTMLButtonElement> & {
    as?: "button";
};

type ButtonAsLink = BaseProps &
    Omit<LinkProps, "to"> & {
    as: "link";
    to: string;
};

type Props = ButtonAsButton | ButtonAsLink;

function cn(...classes: Array<string | false | undefined>) {
    return classes.filter(Boolean).join(" ");
}

const base =
    "inline-flex items-center justify-center gap-2 rounded-xl font-medium transition-colors " +
    "focus:outline-none focus:ring-2 focus:ring-yellow-400 disabled:opacity-60 disabled:cursor-not-allowed";

const variantClasses: Record<Variant, string> = {
    primary: "bg-yellow-500 text-black hover:bg-yellow-600",
    secondary: "bg-gray-800 text-white hover:bg-gray-700 border border-gray-700",
    ghost: "bg-transparent text-white hover:bg-white/10",
    success: "bg-green-600 text-white hover:bg-green-700",
    danger: "bg-red-600 text-white hover:bg-red-700",
    warning: "bg-orange-500 text-white hover:bg-orange-600",
};

const sizeClasses: Record<Size, string> = {
    sm: "h-9 px-3 text-sm",
    md: "h-10 px-4",
    lg: "h-12 px-6 text-lg",
};

const Spinner = () => (
    <svg
        className="h-4 w-4 animate-spin"
        viewBox="0 0 24 24"
        aria-hidden="true"
    >
        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
        <path
            className="opacity-75"
            d="M4 12a8 8 0 018-8v4A4 4 0 004 12z"
            fill="currentColor"
        />
    </svg>
);

export function Button(props: Props) {
    const {
        children,
        variant = "primary",
        size = "md",
        fullWidth,
        loading,
        leftIcon,
        rightIcon,
        className,
        ...rest
    } = props;

    const classes = cn(
        base,
        variantClasses[variant],
        sizeClasses[size],
        fullWidth && "w-full",
        className
    );

    const content = (
        <>
            {loading && <Spinner/>}
            {!loading && leftIcon}
            <span>{children}</span>
            {!loading && rightIcon}
        </>
    );

    if ("as" in props && props.as === "link") {
        const {to, ...linkRest} = rest as ButtonAsLink;
        return (
            <Link
                to={to}
                role="button"
                aria-busy={loading || undefined}
                className={classes}
                {...linkRest}
            >
                {content}
            </Link>
        );
    }

    const buttonRest = rest as ButtonAsButton;
    return (
        <button
            type={buttonRest.type ?? "button"}
            disabled={buttonRest.disabled || loading}
            aria-busy={loading || undefined}
            className={classes}
            {...buttonRest}
        >
            {content}
        </button>
    );
}
