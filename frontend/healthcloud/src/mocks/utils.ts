export const chooseRandomKeypoints = (arrays: string[][], length: number) => {
    const allElements = arrays.flat();
    const result = [];

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * allElements.length);
        result.push(allElements[randomIndex]);
    }

    return result;
};
