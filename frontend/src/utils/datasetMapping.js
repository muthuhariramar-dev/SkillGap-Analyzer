/**
 * Utility to map human-readable role titles to kebab-case dataset filenames.
 */

export const ROLE_DATASET_MAP = {
    "WordPress Developer": "wordpress-developer",
    "Software Engineer[AGILE]": "software-engineer-agile",
    "Mobile Developer": "mobile-developer",
    "Game Developer": "game-developer",
    "Big Data Developer": "big-data-developer",
    "Developmental Operations Engineer": "devops-engineer",
    "Data Scientist": "data-scientist",
    "Security Developer": "security-developer",
    "Graphics Developer": "graphics-developer",
    "Frontend Developer": "frontend-developer",
    "Backend Developer": "backend-developer",
    "Full Stack Developer": "fullstack-developer",
    "Product Manager": "product-manager",
    "Team Lead": "team-lead",
    "UI/UX Designer": "ui-ux-designer",
};

/**
 * Converts a role title to a safe kebab-case filename slug.
 * 1. lowercase
 * 2. remove special characters like []
 * 3. spaces -> hyphens
 * 4. remove multiple hyphens
 * 
 * @param {string} roleName 
 * @returns {string} kebab-case slug
 */
export const formatRoleToKebab = (roleName) => {
    // Check explicit map first for consistency
    if (ROLE_DATASET_MAP[roleName]) {
        return ROLE_DATASET_MAP[roleName];
    }

    return roleName
        .toLowerCase()
        .replace(/\[|\]/g, '')       // Remove [ and ]
        .replace(/[^a-z0-9\s-]/g, '') // Remove other special chars
        .trim()
        .replace(/\s+/g, '-')         // Spaces to hyphens
        .replace(/-+/g, '-');         // Collapse multiple hyphens
};

/**
 * Gets the dataset filename for a given role.
 * @param {string} roleName 
 * @returns {string} filename with .json extension
 */
export const getDatasetFilename = (roleName) => {
    return `${formatRoleToKebab(roleName)}.json`;
};
