const fs = require('fs');

const content = fs.readFileSync('admin/index.html', 'utf8');

// Extract second script block
const scriptRegex = /<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>/gi;
scriptRegex.exec(content); // first block (route guard)
const match = scriptRegex.exec(content); // second main block
const scriptCode = match[1];

// Mock minimum DOM and browser globals
const globalScope = {
    document: {
        getElementById: () => null,
        querySelectorAll: () => [],
        addEventListener: () => {}
    },
    window: {
        addEventListener: () => {},
        location: { href: '', replace: () => {} }
    },
    localStorage: {
        getItem: () => null,
        setItem: () => {}
    },
    sessionStorage: {
        getItem: () => null,
        setItem: () => {}
    },
    console: console
};

const vm = require('vm');
const ctx = vm.createContext(globalScope);
vm.runInContext(scriptCode, ctx);

console.log('Testing computeClientAnalyticsData in sandboxed environment...');

const allData = ctx.computeClientAnalyticsData('', '', 'all', 'all');
console.log('All Time Metrics:');
console.log('  Total Activities:', allData.metrics.total_activities);
console.log('  Total Won Revenue (INR):', allData.metrics.total_revenue);
console.log('  Active Pipeline Value (INR):', allData.metrics.total_pipeline);
console.log('  Won Count:', allData.metrics.won_count);
console.log('  Pipeline Count:', allData.metrics.pipeline_count);
console.log('  Lost Count:', allData.metrics.lost_count);
console.log('  Consultations/Meetings Count:', allData.metrics.meetings_count);
console.log('  Conversion / Win Rate (%):', allData.metrics.win_rate_pct);
console.log('  Average Deal Size (INR):', allData.metrics.avg_deal_size);
console.log('  Distinct Users:', allData.distinct_users);

// Assertions
if (allData.metrics.total_activities <= 0) throw new Error('total_activities should be > 0');
if (allData.metrics.total_revenue <= 0) throw new Error('total_revenue should be > 0');
if (allData.metrics.total_pipeline <= 0) throw new Error('total_pipeline should be > 0');
if (allData.metrics.win_rate_pct <= 0) throw new Error('win_rate_pct should be > 0');
if (allData.metrics.avg_deal_size <= 0) throw new Error('avg_deal_size should be > 0');

// Test Filter by status: Win
const winData = ctx.computeClientAnalyticsData('', '', 'all', 'Win');
console.log('Win Filter Activities:', winData.metrics.total_activities);
if (winData.activities.some(a => a.status !== 'Win' && a.status !== 'Completed')) {
    throw new Error('Win filter returned non-won items');
}

// Test Filter by status: Pipeline
const pipeData = ctx.computeClientAnalyticsData('', '', 'all', 'Pipeline');
console.log('Pipeline Filter Activities:', pipeData.metrics.total_activities);
if (pipeData.activities.some(a => a.status !== 'Pipeline')) {
    throw new Error('Pipeline filter returned non-pipeline items');
}

// Test Date Presets
const fyData = ctx.computeClientAnalyticsData('2025-04-01', '2026-03-31', 'all', 'all');
console.log('FY 2025-26 Activities:', fyData.metrics.total_activities);
if (fyData.metrics.total_activities <= 0) throw new Error('FY 25-26 should contain activities');

console.log('✓ All analytics calculation assertions PASSED successfully!');
