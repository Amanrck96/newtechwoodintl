import re

with open('admin.html', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update renderRevenueCharts with typeof Chart check
old_rev = """\t\tfunction renderRevenueCharts(chartsData) {
\t\t\tif (!chartsData) return;

\t\t\t// Chart 1: Monthly Bar Chart (Pipeline vs Win in ₹ Cr)
\t\t\tconst barCtx = document.getElementById('monthlyBarChart')?.getContext('2d');
\t\t\tif (barCtx) {"""

new_rev = """\t\tfunction renderRevenueCharts(chartsData) {
\t\t\tif (!chartsData) return;
\t\t\tif (typeof Chart === 'undefined') {
\t\t\t\tconsole.warn('Chart.js CDN unavailable; skipping canvas chart instantiation');
\t\t\t\treturn;
\t\t\t}
\t\t\ttry {

\t\t\t// Chart 1: Monthly Bar Chart (Pipeline vs Win in ₹ Cr)
\t\t\tconst barCtx = document.getElementById('monthlyBarChart')?.getContext('2d');
\t\t\tif (barCtx) {"""

assert old_rev in code, "old_rev not found in admin.html"
code = code.replace(old_rev, new_rev, 1)

# Close try block in renderRevenueCharts
old_rev_end = """\t\t\t\t\t\t\t}
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}
\t\t}"""

new_rev_end = """\t\t\t\t\t\t\t}
\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}
\t\t\t} catch (chartErr) {
\t\t\t\tconsole.warn('Error rendering revenue charts:', chartErr);
\t\t\t}
\t\t}"""

assert old_rev_end in code, "old_rev_end not found in admin.html"
code = code.replace(old_rev_end, new_rev_end, 1)

# 2. Update renderProductAmountCharts
old_amt = """\t\tfunction renderProductAmountCharts(breakdown) {
\t\t\tconst ctx = document.getElementById('productAmountChart')?.getContext('2d');
\t\t\tif (ctx) {
\t\t\t\tif (dashCharts.prodAmount) dashCharts.prodAmount.destroy();"""

new_amt = """\t\tfunction renderProductAmountCharts(breakdown) {
\t\t\tconst ctx = document.getElementById('productAmountChart')?.getContext('2d');
\t\t\tif (ctx && typeof Chart !== 'undefined') {
\t\t\t\ttry {
\t\t\t\t\tif (dashCharts.prodAmount) dashCharts.prodAmount.destroy();"""

assert old_amt in code, "old_amt not found in admin.html"
code = code.replace(old_amt, new_amt, 1)

old_amt_end = """\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}

\t\t\t// Render summary table"""

new_amt_end = """\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t\t} catch (chartErr) {
\t\t\t\t\tconsole.warn('Error rendering product amount chart:', chartErr);
\t\t\t\t}
\t\t\t}

\t\t\t// Render summary table"""

assert old_amt_end in code, "old_amt_end not found in admin.html"
code = code.replace(old_amt_end, new_amt_end, 1)

# 3. Update renderProductSqftCharts
old_sqft = """\t\tfunction renderProductSqftCharts(breakdown) {
\t\t\tconst ctx = document.getElementById('productSqftChart')?.getContext('2d');
\t\t\tif (ctx) {
\t\t\t\tif (dashCharts.prodSqft) dashCharts.prodSqft.destroy();"""

new_sqft = """\t\tfunction renderProductSqftCharts(breakdown) {
\t\t\tconst ctx = document.getElementById('productSqftChart')?.getContext('2d');
\t\t\tif (ctx && typeof Chart !== 'undefined') {
\t\t\t\ttry {
\t\t\t\t\tif (dashCharts.prodSqft) dashCharts.prodSqft.destroy();"""

assert old_sqft in code, "old_sqft not found in admin.html"
code = code.replace(old_sqft, new_sqft, 1)

old_sqft_end = """\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t}

\t\t\t// Render summary table"""

new_sqft_end = """\t\t\t\t\t\t}
\t\t\t\t\t}
\t\t\t\t});
\t\t\t\t} catch (chartErr) {
\t\t\t\t\tconsole.warn('Error rendering product sqft chart:', chartErr);
\t\t\t\t}
\t\t\t}

\t\t\t// Render summary table"""

assert old_sqft_end in code, "old_sqft_end not found in admin.html"
code = code.replace(old_sqft_end, new_sqft_end, 1)

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(code)

with open('admin/index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Safeguarded Chart.js rendering in admin.html and admin/index.html successfully!")
