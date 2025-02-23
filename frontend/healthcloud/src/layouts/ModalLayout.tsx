import { PropsWithChildren } from "react";
import { createPortal } from "react-dom";

export const ModalLayout = ({ children }: PropsWithChildren) => {
    return createPortal(
        <div className="fixed top-0 left-0 bg-[#181818b9] z-20 backdrop-blur-[3px] flex items-center justify-center w-screen h-screen">
            {children}
        </div>,
        document.getElementById("modal-root") as HTMLElement
    );
};
