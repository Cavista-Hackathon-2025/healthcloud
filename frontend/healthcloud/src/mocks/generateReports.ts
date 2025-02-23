import { Report } from "@/types/reports";
import { faker } from "@faker-js/faker";
import { mockReportTitles, mockReportSummaries } from "@/mocks/mockdata";
import { generateReportSegments } from "@/mocks/generateReportSegments";

export const generateReports = (count: number): Report[] => {
    const reports = [];

    for (let i = 0; i < count; i++) {
        const report: Report = {
            id: faker.string.nanoid(),
            title: faker.helpers.arrayElement(mockReportTitles),
            summary: faker.helpers.arrayElement(mockReportSummaries),
            dateCreated: faker.date.past(),
            patient: {
                id: faker.string.nanoid(),
                name: faker.person.fullName(),
            },
            doctor: {
                id: faker.string.nanoid(),
                name: `Dr. Julius Ekene`,
            },
            segments: generateReportSegments(
                faker.number.int({ min: 4, max: 8 })
            ),
        };

        reports.push(report);
    }

    return reports;
};
