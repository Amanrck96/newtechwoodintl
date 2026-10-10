import re

with open('admin/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Title
content = content.replace(
    '<title>NewTechWood CRM &amp; Sales Dashboard — Admin Portal</title>',
    '<title>NewTechWood CRM &amp; Commercial Operations — Partner &amp; Vendor Portal</title>'
)

# 2. Route guard
idx_start = content.find('<!-- IMMEDIATE HEAD ROUTE GUARD: PROTECT ALL ADMIN ROUTES -->')
idx_end = content.find('<!-- Fonts -->')
if idx_start != -1 and idx_end != -1:
    vendor_guard = '''<!-- ROUTE GUARD: PROTECT VENDOR PORTAL (ALLOWS ALL AUTHENTICATED PARTNERS & ADMINS) -->
\t<script>
\t\t(function() {
\t\t\ttry {
\t\t\t\tconst sessionStr = localStorage.getItem('ntw_session') || sessionStorage.getItem('ntw_session');
\t\t\t\tif (!sessionStr) {
\t\t\t\t\twindow.location.replace('/login/');
\t\t\t\t\treturn;
\t\t\t\t}
\t\t\t\tconst sess = JSON.parse(sessionStr);
\t\t\t\tif (!sess || !sess.role) {
\t\t\t\t\twindow.location.replace('/login/');
\t\t\t\t\treturn;
\t\t\t\t}
\t\t\t} catch (e) {
\t\t\t\twindow.location.replace('/login/');
\t\t\t}
\t\t})();
\t</script>

\t'''
    content = content[:idx_start] + vendor_guard + content[idx_end:]

# 3. Topbar Badge
content = content.replace(
    '<span class="crm-badge">CRM &amp; Sales Operations</span>',
    '<span class="crm-badge" style="background:rgba(201,168,76,0.18);color:#8c6d1d;border-color:rgba(201,168,76,0.4);">Partner &amp; Vendor Portal</span>'
)

# 4. Topbar Button
old_btn = '''\t\t<div class="topbar-right">
\t\t\t<a href="/admin/vendor.html" class="btn-topbar-link btn-vendor-portal" title="Open Vendor Partner Portal">
\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
\t\t\t\t\t<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
\t\t\t\t\t<circle cx="8.5" cy="7" r="4"></circle>
\t\t\t\t\t<line x1="20" y1="8" x2="20" y2="14"></line>
\t\t\t\t\t<line x1="23" y1="11" x2="17" y2="11"></line>
\t\t\t\t</svg>
\t\t\t\t<span>Vendor Portal</span>
\t\t\t</a>'''

new_btn = '''\t\t<div class="topbar-right">
\t\t\t<a href="/admin/" class="btn-topbar-link btn-vendor-portal" id="btnAdminReturn" style="display:none;" title="Return to Super Admin CMS">
\t\t\t\t<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
\t\t\t\t\t<line x1="19" y1="12" x2="5" y2="12"></line>
\t\t\t\t\t<polyline points="12 19 5 12 12 5"></polyline>
\t\t\t\t</svg>
\t\t\t\t<span>Return to Admin CMS</span>
\t\t\t</a>'''

content = content.replace(old_btn, new_btn)

# 5. initSession greeting sub and RBAC
old_init = '''\t\t\tconst dashSub = document.getElementById('dashboardGreetingSub');
\t\t\tif (dashSub) {
\t\t\t\tdashSub.innerText = `Welcome back, ${displayName}. Real-time CRM intelligence and sales monitoring.`;
\t\t\t}'''

new_init = '''\t\t\tconst dashSub = document.getElementById('dashboardGreetingSub');
\t\t\tif (dashSub) {
\t\t\t\tdashSub.innerText = `Welcome back, ${displayName}. Partner commercial dashboard, material orders, and technical CAD assets.`;
\t\t\t}

\t\t\t// Show Return to Admin CMS button if current user is admin/superadmin
\t\t\tconst returnBtn = document.getElementById('btnAdminReturn');
\t\t\tif (returnBtn && (role.toLowerCase() === 'admin' || role.toLowerCase() === 'superadmin')) {
\t\t\t\treturnBtn.style.display = 'inline-flex';
\t\t\t}

\t\t\t// RBAC Enforcement for Partner Portal
\t\t\tif (role.toLowerCase() !== 'admin' && role.toLowerCase() !== 'superadmin') {
\t\t\t\tconst pagesNav = document.getElementById('nav-pages');
\t\t\t\tif (pagesNav) {
\t\t\t\t\tconst li = pagesNav.closest('.sidebar-item');
\t\t\t\t\tif (li) li.style.display = 'none';
\t\t\t\t}
\t\t\t}'''

content = content.replace(old_init, new_init)

with open('admin/vendor.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated admin/vendor.html successfully!')
