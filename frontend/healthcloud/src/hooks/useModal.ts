import { useState } from "react";

export const useModal = (hash = "modal") => {
    const isAlreadyOpen = window.location.hash === `#${hash}`;
    const [isOpen, setIsOpen] = useState(isAlreadyOpen);

    const openModal = () => {
        window.location.hash = hash;
        setIsOpen(true);
    };
    const closeModal = () => {
        window.location.hash = "";
        setIsOpen(false);
    };

    return {
        openModal,
        closeModal,
        isOpen,
    };
};
