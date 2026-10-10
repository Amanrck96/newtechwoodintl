const fs = require('fs');

function testHtmlScripts(filePath) {
    console.log(`Testing scripts in ${filePath}...`);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Extract script tags (ignoring external scripts with src=)
    const scriptRegex = /<script(?![^>]*\bsrc\b)[^>]*>([\s\S]*?)<\/script>/gi;
    let match;
    let count = 0;
    
    while ((match = scriptRegex.exec(content)) !== null) {
        count++;
        const code = match[1];
        try {
            // Use Function constructor or new vm.Script to validate syntax
            new Function(code);
            console.log(`  ✓ Script block #${count} syntax valid (${code.length} chars)`);
        } catch (err) {
            console.error(`  ✗ Syntax error in script block #${count}:`, err.message);
            process.exit(1);
        }
    }
}

testHtmlScripts('admin/index.html');
testHtmlScripts('admin.html');
testHtmlScripts('admin/vendor.html');
console.log('All admin HTML scripts passed syntax validation!');
