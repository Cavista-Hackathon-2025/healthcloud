import clsx from "clsx";
import { FaTriangleExclamation } from "react-icons/fa6";

interface ErrorNotificationProps {
    className?: string;
    title?: string;
    message?: string;
    hideIcon?: boolean;
}

export const ErrorNotification = ({
    className,
    title,
    message,
    hideIcon = false,
}: ErrorNotificationProps) => {
    const defaultMessage =
        "We encountered an error. Please try reloading the page, or reaching out to HealthCloud developers. Thank you for your understanding!";
    const defaultTitle = "Something went wrong";

    const titleToDisplay = title || defaultTitle;
    const messageToDisplay = message || defaultMessage;
    return (
        <div
            className={clsx(
                "flex flex-col w-full h-full p-4 rounded-md border border-rose-300 bg-rose-50 shadow-sm shadow-rose-100 justify-center items-center",
                className
            )}>
            {!hideIcon && (
                <FaTriangleExclamation className="text-rose-600 text-3xl" />
            )}
            <h1 className="text-lg font-semibold text-rose-600 mb-0">
                {titleToDisplay}
            </h1>
            <p className="text-rose-400 max-w-1/2 text-center text-sm">
                {messageToDisplay}
            </p>
        </div>
    );
};
