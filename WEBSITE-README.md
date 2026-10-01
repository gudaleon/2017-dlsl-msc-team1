# SAMQWAN Environmental Science Website

Modern, responsive website for SAMQWAN Environmental Science Inc. - a leading environmental science laboratory and modelling firm.

## Overview

This website showcases SAMQWAN's comprehensive environmental science services, expertise, and commitment to sustainable development and Indigenous-led environmental stewardship.

## Features

### 🎨 Modern Design
- Clean, professional aesthetic with environmental color palette
- Smooth animations and transitions
- Interactive UI elements
- Responsive design for all devices

### 🚀 Performance Optimized
- Lightweight codebase
- Efficient CSS and JavaScript
- Fast loading times
- Debounced scroll events for better performance

### ♿ Accessibility
- Semantic HTML5
- ARIA labels
- Keyboard navigation support
- Skip to content link
- High contrast ratios

### 📱 Responsive
- Mobile-first approach
- Tablet and desktop optimized
- Touch-friendly interactions
- Hamburger menu for mobile

### ✨ Interactive Features
- Smooth scrolling navigation
- Animated statistics counter
- Fade-in animations on scroll
- Contact form with validation
- Scroll-to-top button
- Active navigation highlighting
- Parallax hero background

## Sections

1. **Hero Section** - Eye-catching introduction with call-to-action buttons
2. **Services** - Comprehensive grid of 6 core services with detailed features
3. **Expertise** - Areas of specialization with numbered highlights
4. **Stats** - Animated statistics showcasing experience and impact
5. **About** - Company overview with values and mission
6. **Contact** - Interactive form with contact information

## Services Offered

- **Sediment & Porewater Geochemistry** - Advanced sediment analysis
- **Reactive-Transport Modelling** - Computational modeling solutions
- **Microbial Process Assessment** - Biogeochemical evaluation
- **Advanced Characterization** - Raman, AFM, XRF techniques
- **Carbon MRV & Climate Solutions** - Carbon measurement and verification
- **Mine Closure & Risk Assessment** - Tailings and closure planning

## Technology Stack

- **HTML5** - Semantic markup with schema.org structured data
- **CSS3** - Modern styling with CSS Grid, Flexbox, and custom properties
- **Vanilla JavaScript** - No dependencies, pure JS for all interactions
- **Google Fonts** - Inter and Playfair Display typefaces

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## File Structure

```
.
├── index.html          # Main HTML file
├── styles.css          # All CSS styles
├── script.js           # JavaScript functionality
└── WEBSITE-README.md   # This file
```

## Setup & Deployment

### Local Development

1. Clone the repository
2. Open `index.html` in a web browser
3. No build process required - pure HTML/CSS/JS

### Production Deployment

1. Upload all files to your web hosting
2. Ensure all files are in the root directory or configure paths accordingly
3. Set up SSL certificate for HTTPS
4. Configure contact form backend (currently shows demo notification)

## Customization

### Colors
Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #2c6375;
    --primary-light: #4a90a4;
    --primary-dark: #1a3d47;
    /* ... */
}
```

### Content
Edit text directly in `index.html` - all content is in semantic HTML sections.

### Contact Form
Replace the demo setTimeout in `script.js` with your actual API endpoint:
```javascript
fetch('/api/contact', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
})
```

## SEO & Performance

- Meta tags for social sharing (Open Graph)
- Structured data (JSON-LD) for search engines
- Semantic HTML for better crawling
- Optimized for Core Web Vitals
- Mobile-friendly (Google Mobile-Friendly Test ready)

## Future Enhancements

- [ ] Blog/news section
- [ ] Project portfolio/case studies
- [ ] Team member profiles
- [ ] Publications library
- [ ] Multi-language support
- [ ] Progressive Web App (PWA) capabilities
- [ ] Dark mode toggle
- [ ] Advanced animations with intersection observer

## Contact Backend Setup

To make the contact form functional:

1. Set up a backend API endpoint (Node.js, Python, PHP, etc.)
2. Configure email service (SendGrid, AWS SES, Mailgun)
3. Update the form submission code in `script.js`
4. Add CSRF protection and rate limiting
5. Implement spam protection (reCAPTCHA, honeypot)

## License

© 2026 SAMQWAN Environmental Science Inc. All rights reserved.

## Credits

- Design & Development: Custom built
- Icons: Inline SVG
- Fonts: Google Fonts (Inter, Playfair Display)

---

For questions or support, contact: info@enviro-research.com
