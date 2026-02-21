const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

/**
 * Safe filename formatter utility
 */
const formatRoleToKebab = (roleName) => {
    return roleName
        .toLowerCase()
        .replace(/[\[\]]/g, '')
        .replace(/[^a-z0-9\s-]/g, '')
        .trim()
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-');
};

/**
 * GET /api/questions/:role
 * Dynamically load dataset based on selected role.
 */
router.get('/:role', (req, res) => {
    const roleName = req.params.role;
    const filename = `${formatRoleToKebab(roleName)}.json`;
    const datasetPath = path.join(__dirname, '..', '..', 'datasets', filename);

    // Error handling if dataset not found
    if (!fs.existsSync(datasetPath)) {
        return res.status(404).json({
            success: false,
            message: `Dataset not found for role: ${roleName}`,
            path: datasetPath
        });
    }

    try {
        const rawData = fs.readFileSync(datasetPath, 'utf8');
        const questions = JSON.parse(rawData);

        res.json({
            success: true,
            role: roleName,
            filename: filename,
            questions: questions.questions || questions // Handle both wrapped and unwrapped JSON
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            message: 'Error loading dataset',
            error: error.message
        });
    }
});

module.exports = router;
