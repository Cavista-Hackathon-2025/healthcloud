import React from "react";

export const cloneComponent = (
    component: React.ReactElement = <></>,
    multiples: number
) => {
    const components: React.ReactElement[] = [];

    for (let i = 0; i < multiples; i++) {
        components.push(<React.Fragment key={i}>{component}</React.Fragment>);
    }

    return components;
};
