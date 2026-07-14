import os
import re

file_path = r'c:\Users\amanr\OneDrive\Documents\newtechwoodintl\locations\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Title and Meta Tags
content = content.replace('<title>Find a Distributor - NewTechWood</title>', '<title>Experience Centre - NewTechWood</title>')
content = content.replace('content="Locate authorized NewTechWood distributors worldwide! Easily find local suppliers for our products—simply select your location."', 'content="Explore NewTechWood\'s Experience Centres across India. Visit our partner locations in Nagpur, Bengaluru, Delhi, Mumbai, Pune, and Chennai."')
content = content.replace('content="Find a Distributor - NewTechWood"', 'content="Experience Centre - NewTechWood"')

# 2. Add Premium Styles
style_block = """@font-face {
	font-family: 'Butler';
	font-style: normal;
	font-weight: 900;
	src: url('../wp-content/uploads/2025/08/Butler-Black-8.otf') format('OpenType');
}
</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
<style id="ll-premium-styles">
  :root {
    --ll-green: #2d6a2d;
    --ll-green-light: #4a9e4a;
    --ll-gold: #c9a84c;
    --ll-dark: #1a1a1a;
    --ll-bg: #f8f6f1;
    --ll-white: #ffffff;
    --ll-shadow: 0 8px 32px rgba(0,0,0,0.10);
    --ll-radius: 16px;
    --ll-transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* --- Experience Centre Section --- */
  .ll-experience-centre {
    background: linear-gradient(135deg, #0d2b0d 0%, #1a4a1a 50%, #0d2b0d 100%);
    padding: 100px 20px;
    font-family: 'Inter', sans-serif;
    position: relative;
    overflow: hidden;
    min-height: 80vh;
    display: flex;
    align-items: center;
  }
  .ll-experience-centre::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 320px; height: 320px;
    background: radial-gradient(circle, rgba(201,168,76,0.15) 0%, transparent 70%);
    pointer-events: none;
  }
  .ll-experience-centre::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(74,158,74,0.12) 0%, transparent 70%);
    pointer-events: none;
  }
  .ll-ec-inner {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    position: relative;
    z-index: 1;
  }
  .ll-ec-header {
    text-align: center;
    margin-bottom: 60px;
  }
  .ll-ec-eyebrow {
    display: inline-block;
    background: rgba(201,168,76,0.18);
    color: var(--ll-gold);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    border: 1px solid rgba(201,168,76,0.3);
    margin-bottom: 20px;
  }
  .ll-ec-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(36px, 5vw, 56px);
    font-weight: 700;
    color: var(--ll-white);
    line-height: 1.15;
    margin: 0 0 16px;
  }
  .ll-ec-title span {
    color: var(--ll-gold);
  }
  .ll-ec-subtitle {
    font-size: 16px;
    color: rgba(255,255,255,0.65);
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.6;
  }
  .ll-ec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 30px;
  }
  .ll-ec-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: var(--ll-radius);
    padding: 40px 32px;
    position: relative;
    overflow: hidden;
    transition: var(--ll-transition);
    backdrop-filter: blur(8px);
  }
  .ll-ec-card:hover {
    transform: translateY(-6px);
    background: rgba(255,255,255,0.10);
    border-color: rgba(201,168,76,0.40);
    box-shadow: 0 20px 48px rgba(0,0,0,0.25);
  }
  .ll-ec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--ll-gold), var(--ll-green-light));
    opacity: 0;
    transition: opacity 0.35s;
  }
  .ll-ec-card:hover::before {
    opacity: 1;
  }
  .ll-ec-card.coming-soon {
    opacity: 0.60;
  }
  .ll-ec-card.coming-soon:hover {
    opacity: 0.75;
    transform: none;
  }
  .ll-ec-city-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--ll-gold);
    margin-bottom: 20px;
  }
  .ll-ec-city-badge svg {
    width: 12px;
    height: 12px;
    fill: currentColor;
  }
  .ll-ec-card-city {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 700;
    color: var(--ll-white);
    margin: 0 0 6px;
  }
  .ll-ec-card-partner {
    font-size: 14px;
    font-weight: 600;
    color: var(--ll-green-light);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 20px;
  }
  .ll-ec-card-address {
    font-size: 15px;
    color: rgba(255,255,255,0.70);
    line-height: 1.7;
    min-height: 60px;
  }
  .ll-ec-coming-tag {
    display: inline-block;
    background: rgba(255,255,255,0.10);
    color: rgba(255,255,255,0.50);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 100px;
    margin-top: 16px;
  }
  .ll-ec-divider {
    width: 50px;
    height: 2px;
    background: linear-gradient(90deg, var(--ll-gold), transparent);
    margin: 18px 0 20px;
  }

  /* --- Footer Lumber Life Block --- */
  .ll-footer-brand {
    background: linear-gradient(135deg, #0a1f0a 0%, #142814 100%);
    padding: 40px 40px 32px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    display: flex;
    flex-direction: column;
    gap: 20px;
    font-family: 'Inter', sans-serif;
  }
  .ll-footer-brand img {
    width: 160px;
    height: auto;
    object-fit: contain;
  }
  .ll-footer-brand-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .ll-footer-brand-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--ll-gold);
    opacity: 0.85;
  }
  .ll-footer-brand-address {
    font-size: 13px;
    color: rgba(255,255,255,0.70);
    line-height: 1.6;
  }
  .ll-footer-brand-contact {
    font-size: 13px;
    color: rgba(255,255,255,0.70);
    line-height: 1.6;
  }
  .ll-footer-brand-divider {
    width: 100%;
    height: 1px;
    background: rgba(255,255,255,0.08);
  }

  @media (max-width: 768px) {
    .ll-experience-centre { padding: 60px 16px; }
    .ll-ec-grid { grid-template-columns: 1fr; }
    .ll-footer-brand { padding: 28px 24px; }
  }
</style>"""

content = content.replace("""@font-face {
	font-family: 'Butler';
	font-style: normal;
	font-weight: 900;
	src: url('../wp-content/uploads/2025/08/Butler-Black-8.otf') format('OpenType');
}
</style>""", style_block)

# 3. Remove Exhibitions Link
exhib_str = """				<div class="elementor-element elementor-element-41abd95 elementor-widget elementor-widget-text-editor" data-id="41abd95" data-element_type="widget" data-widget_type="text-editor.default">
									<p><a href="../blog/category/exhibitions/index.html">Exhibitions</a></p>								</div>"""
content = content.replace(exhib_str, "")

# 4. Change Nav text
content = content.replace("FIND A DISTRIBUTOR", "EXPERIENCE CENTRE")

# 5. Replace Grid
start_marker = '<div class="elementor-element elementor-element-1a54c74 elementor-widget elementor-widget-Logic_Widget_Distributor"'
end_marker = '<!-- ======================================================'

footer_marker = '<footer data-elementor-type="footer" data-elementor-id="272" class="elementor elementor-272 elementor-location-footer" data-elementor-post-type="elementor_library">'

start_idx = content.find(start_marker)
end_idx = content.find(footer_marker)

grid_html = """	<!-- ======================================================
	     EXPERIENCE CENTRE SECTION
	     ====================================================== -->
	<section class="ll-experience-centre" id="experience-centre" aria-label="Experience Centres across India">
	  <div class="ll-ec-inner">
	    <div class="ll-ec-header">
	      <div class="ll-ec-eyebrow">&#x2706; Visit Us In Person</div>
	      <h2 class="ll-ec-title">Our <span>Experience Centres</span></h2>
	      <p class="ll-ec-subtitle">Touch, feel, and explore NewTechWood's premium composite products at our experience centres across India.</p>
	    </div>
	    <div class="ll-ec-grid">

	      <!-- Nagpur -->
	      <div class="ll-ec-card">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Nagpur
	        </div>
	        <h3 class="ll-ec-card-city">Nagpur</h3>
	        <div class="ll-ec-card-partner">Lumber Life</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">[Lumber Life Address &amp; Contact — to be filled]</p>
	      </div>

	      <!-- Bengaluru -->
	      <div class="ll-ec-card">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Bengaluru
	        </div>
	        <h3 class="ll-ec-card-city">Bengaluru</h3>
	        <div class="ll-ec-card-partner">Aaren Intpro</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">[Aaren Intpro Address &amp; Contact — to be filled]</p>
	      </div>

	      <!-- Delhi -->
	      <div class="ll-ec-card coming-soon">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Delhi
	        </div>
	        <h3 class="ll-ec-card-city">Delhi</h3>
	        <div class="ll-ec-card-partner">&nbsp;</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">Details coming soon. Stay tuned for our upcoming Experience Centre in the capital.</p>
	        <span class="ll-ec-coming-tag">Coming Soon</span>
	      </div>

	      <!-- Mumbai -->
	      <div class="ll-ec-card coming-soon">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Mumbai
	        </div>
	        <h3 class="ll-ec-card-city">Mumbai</h3>
	        <div class="ll-ec-card-partner">&nbsp;</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">Our Mumbai Experience Centre is coming. We look forward to welcoming you soon.</p>
	        <span class="ll-ec-coming-tag">Coming Soon</span>
	      </div>

	      <!-- Pune -->
	      <div class="ll-ec-card coming-soon">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Pune
	        </div>
	        <h3 class="ll-ec-card-city">Pune</h3>
	        <div class="ll-ec-card-partner">&nbsp;</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">Opening soon — Pune's first NewTechWood Experience Centre.</p>
	        <span class="ll-ec-coming-tag">Coming Soon</span>
	      </div>

	      <!-- Chennai -->
	      <div class="ll-ec-card coming-soon">
	        <div class="ll-ec-city-badge">
	          <svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
	          Chennai
	        </div>
	        <h3 class="ll-ec-card-city">Chennai</h3>
	        <div class="ll-ec-card-partner">&nbsp;</div>
	        <div class="ll-ec-divider"></div>
	        <p class="ll-ec-card-address">Watch this space — Chennai Experience Centre coming soon.</p>
	        <span class="ll-ec-coming-tag">Coming Soon</span>
	      </div>

	    </div><!-- /ll-ec-grid -->
	  </div><!-- /ll-ec-inner -->
	</section>
				</div>
				</div>
				<footer data-elementor-type="footer" data-elementor-id="272" class="elementor elementor-272 elementor-location-footer" data-elementor-post-type="elementor_library">"""

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + grid_html + content[end_idx+len(footer_marker):]
else:
    print(f"Error finding markers. start_idx={start_idx}, end_idx={end_idx}")

# 6. Add footer branding
footer_insert_point = """				<div class="elementor-element elementor-element-0c8c31b elementor-widget elementor-widget-text-editor" data-id="0c8c31b" data-element_type="widget" data-widget_type="text-editor.default">
									<p><a href="../contact-us/index.html">Contact us</a></p><p><a href="index.html">Experience Centre</a></p>								</div>
				</div>"""

footer_brand = """		<!-- Lumber Life Branding Block -->
		<div class="e-con-full e-flex e-con e-child" style="min-width:260px;">
		  <div class="ll-footer-brand">
		    <img src="../wp-content/uploads/lumber-life-logo.png" alt="Lumber Life - Delivering Nature" onerror="this.style.display='none'" />
		    <div class="ll-footer-brand-divider"></div>
		    <div class="ll-footer-brand-info">
		      <span class="ll-footer-brand-label">Experience Centre — Nagpur</span>
		      <span class="ll-footer-brand-address">[Lumber Life Address — to be filled]</span>
		      <span class="ll-footer-brand-contact">[Phone &amp; Email — to be filled]</span>
		    </div>
		  </div>
		</div>"""

content = content.replace(footer_insert_point, footer_insert_point + "\\n" + footer_brand)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updates applied successfully.")
