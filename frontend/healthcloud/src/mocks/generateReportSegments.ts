import {
    alleviatingWorriesSummaries,
    diagnosisSummaries,
    generalDiscussionsSummaries,
    informationExchangeSummaries,
    prescriptionsSummaries,
    warningsSummaries,
} from "@/mocks/mockdata";
import { chooseRandomKeypoints } from "@/mocks/utils";
import { ReportSegment, SegmentType } from "@/types/reports";
import { faker } from "@faker-js/faker";

const keypoints = [
    diagnosisSummaries,
    alleviatingWorriesSummaries,
    warningsSummaries,
    generalDiscussionsSummaries,
    informationExchangeSummaries,
    prescriptionsSummaries,
];

const segmentTypes: SegmentType[] = [
    "ALLEVIATING_WORRIES",
    "DIAGNOSIS",
    "GENERAL_DISCUSSIONS",
    "INFORMATION_EXCHANGE",
    "PRESCRIPTIONS",
    "WARNINGS",
];

export const generateReportSegments = (count: number): ReportSegment[] => {
    const segments: ReportSegment[] = [];

    for (let i = 0; i < count; i++) {
        const index = faker.number.int({
            min: 0,
            max: segmentTypes.length - 1,
        });

        const segment = {
            id: faker.string.nanoid(),
            title: faker.lorem.sentence(),
            type: segmentTypes[index],
            content: faker.lorem.paragraph(),
            keypoints: chooseRandomKeypoints(
                [keypoints[index]],
                faker.number.int({ min: 1, max: 3 })
            ),
        };

        segments.push(segment);
    }

    return segments;
};
