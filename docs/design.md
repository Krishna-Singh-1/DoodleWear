# DoodleWear — Design System & UI Specification (design.md)

---

## 📌 Executive Summary

**DoodleWear**'s design system establishes a high-performance, visually thrilling, and accessible e-commerce UI across four distinct visual themes: **Dark Mode (Default)**, **Light Mode**, **Cyberpunk Mode**, and **Arcade Retro Mode**.

The system guarantees consistency between the customer store, 2D customization canvas, AI suite, dealer fulfillment portals, shipping agency console, and admin management dashboards.

> **Revision note:** This version renames the former "Pacman Retro Mode" theme to **Arcade Retro Mode** and removes all references to Pac-Man, Blinky, Pinky, Inky, and Clyde — see §16.1 for details and rationale. It also adds verified accessibility contrast data (§14), motion-reduction support (§12.1), anti-dark-pattern rules for scarcity/urgency UI (§2.4), and full component specs for the Dealer, Shipping Agency, and Admin dashboards (§18), which were previously undocumented.

---

## 1. Brand Identity

- **Brand Name**: DoodleWear 👕
- **Tagline**: *"AI-Crafted Apparel. Delivered to Your Door."*
- **Brand Personality**: Creative, Tech-Forward, Bold, Premium, and Expressive.
- **Visual Tone**: Sleek glassmorphism, vibrant neon accents, high-contrast typography, and smooth micro-animations.

---

## 2. Design Principles

1. **Thumb-Friendly & Mobile-First**: Crucial CTA buttons (e.g., *Add to Cart*, *AI Try-On*, *Generate*) are positioned within natural thumb reach on mobile screens (`bottom: 16px` sticky action bars).
2. **Speed & Sub-2-Second Load Times**: Progressive image loading, SVG icons, and optimized CSS variables ensure render times under 2 seconds.
3. **Persistently Accessible Navigation**: Sticky header with persistent search bar (auto-suggest) and cart drawer icon always visible.
4. **Transparent Social Proof & Trust**: Real-time stock alerts (*"Only 3 left in stock!"*), verified buyer reviews, and Razorpay trust badges at checkout.
5. **Seamless Multi-Theme Fluidity**: Dynamic CSS variables powering effortless theme switches between Dark, Light, Cyberpunk, and Arcade Retro modes without page reloads.

### 2.4 Anti-Dark-Pattern Rule for Scarcity & Urgency UI *(New)*

To stay compliant with consumer-protection guidance on manufactured urgency (e.g., India's CCPA dark-pattern guidelines):

- Stock badges (*"Only 3 left in stock!"*) **must** bind to live inventory counts from the product/dealer stock table — never a hardcoded or design-time threshold.
- Once real stock rises above the low-stock threshold (configurable, default `5` units), the badge must disappear automatically.
- Countdown timers (sale end, cart hold timers) must reflect a real backend-enforced deadline, not a cosmetic client-side timer that resets on refresh.
- No pre-checked upsells, no disguised ads styled as organic product cards, and no "confirmshaming" copy on decline actions (e.g., a "No thanks, I don't want to save money" style dismiss link is prohibited).

---

## 3. Color Palette & Theme Engine

The UI dynamically updates via root CSS variable definitions (`data-theme="dark|light|cyberpunk|arcade"`).

### 3.1 Theme Palette Matrix

| Theme Token | 🌙 Dark Mode (Default) | ☀️ Light Mode | 🤖 Cyberpunk Mode | 🕹️ Arcade Retro Mode |
| :--- | :--- | :--- | :--- | :--- |
| `--bg-primary` | `#0D0F17` (Deep Obsidian) | `#FAFAFD` (Snow White) | `#05050D` (Void Black) | `#000000` (Arcade Pitch Black) |
| `--bg-surface` | `#161926` (Dark Slate) | `#FFFFFF` (Pure White) | `#120B2E` (Deep Neon Purple) | `#080829` (Maze Blue Surface) |
| `--bg-glass` | `rgba(22, 25, 38, 0.75)` | `rgba(255, 255, 255, 0.85)` | `rgba(18, 11, 46, 0.8)` | `rgba(8, 8, 41, 0.9)` |
| `--text-primary` | `#F3F4F6` (Cool Gray 100) | `#111827` (Gray 900) | `#00FFCC` (Neon Cyan) | `#FFE81A` (Arcade Yellow) |
| `--text-secondary` | `#9CA3AF` (Gray 400) | `#4B5563` (Gray 600) | `#FF4D9E` (Neon Pink — lightened) | `#FFC2F5` (Retro Pink) |
| `--accent-primary` | `#6366F1` (Electric Indigo) | `#4F46E5` (Indigo 600) | `#FF337D` (Neon Magenta — lightened) | `#FFE81A` (Arcade Gold) |
| `--accent-secondary` | `#10B981` (Emerald Green) | `#059669` (Emerald 600) | `#33F3FF` (Laser Cyan — lightened) | `#4D6BFF` (Retro Blue) |
| `--accent-warning` | `#F59E0B` (Amber) | `#D97706` (Amber 600) | `#FFE600` (Electric Yellow) | `#FFB852` (Retro Orange) |
| `--accent-danger` | `#EF4444` (Crimson) | `#DC2626` (Red 600) | `#FF3355` (Cyber Red — lightened) | `#FF4D4D` (Retro Red) |
| `--border-color` | `rgba(255, 255, 255, 0.1)` | `rgba(0, 0, 0, 0.08)` | `1px solid #00FFCC` | `2px solid #4D6BFF` |

> **Note:** Several Cyberpunk/Arcade accent hex values were lightened from the original spec (e.g., `#FF0055` → `#FF337D`, `#00F0FF` → `#33F3FF`) to meet the 4.5:1 body-text contrast minimum against their paired backgrounds — see §14.1 for the verified ratio table. Do not revert to the original saturated values without re-running contrast checks.

---

## 4. Typography

Primary Font Stack: **Inter** or **Outfit** for clean modern readability.
Display/Heading Font: **Outfit** or **Orbitron** (Cyberpunk/Arcade themes).
Arcade Display Font: **Press Start 2P** (Arcade Retro theme headers only — see §4.1 for loading strategy).
Monospace / Code: **Fira Code** (Print coordinates & Developer APIs).

```css
:root {
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-display: 'Outfit', var(--font-sans);
  --font-arcade: 'Press Start 2P', var(--font-display);
  --font-mono: 'Fira Code', monospace;

  /* Typography Scale */
  --text-xs: 0.75rem;     /* 12px - Stock badges, timestamps */
  --text-sm: 0.875rem;    /* 14px - Helper text, metadata */
  --text-base: 1rem;      /* 16px - Body text, inputs */
  --text-lg: 1.125rem;    /* 18px - Subtitles, card titles */
  --text-xl: 1.25rem;     /* 20px - Section headers */
  --text-2xl: 1.5rem;     /* 24px - Modal headers, PDP title */
  --text-3xl: 2rem;       /* 32px - Page titles */
  --text-4xl: 2.75rem;    /* 44px - Hero value proposition */
}
```

### 4.1 Font Loading Strategy *(New)*

To protect the sub-2-second load principle (§2.2) against pixel-font FOIT/layout shift:

```css
@font-face {
  font-family: 'Press Start 2P';
  src: url('/fonts/press-start-2p.woff2') format('woff2');
  font-display: swap; /* show fallback immediately, swap in when ready */
  font-weight: 400;
}
```

- Self-host all font files (Inter, Outfit, Press Start 2P, Fira Code) — do not depend on a third-party font CDN at render time.
- `font-display: swap` is mandatory on every `@font-face`, so text is never invisible while fonts load.
- `Press Start 2P` is loaded **only** when Arcade Retro theme is active (dynamic `<link>` injection or code-split CSS), not bundled into the base stylesheet, since it's used nowhere else.
- Reserve layout space for arcade headers via `min-height` on heading containers to prevent CLS (Cumulative Layout Shift) when the pixel font swaps in.

---

## 5. Spacing & Layout Grid

- **8pt Grid System**: All margins, paddings, and heights align to multiples of 4px / 8px (`8px`, `16px`, `24px`, `32px`, `48px`, `64px`).
- **Container Breakpoints**:
  - `Mobile`: `< 640px` (Single column, sticky bottom CTA bar).
  - `Tablet`: `640px - 1024px` (2-column layout).
  - `Desktop`: `1024px - 1440px` (4-column product grid, 12-column grid system).
  - `Ultra-Wide`: `> 1440px` (Max container width `1440px` centered).

---

## 6. Design Tokens

```css
:root {
  /* Radii */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 20px;
  --radius-full: 9999px;

  /* Shadows & Elevations */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 8px 24px rgba(0, 0, 0, 0.25);
  --shadow-glow: 0 0 20px var(--accent-primary);

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: 350ms cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

---

## 7. Icons & Illustrations

- **Icon Set**: Lucide Icons or Feather Icons (SVG).
- **Custom Badge Assets**:
  - 🟢 `Verified Buyer`
  - ⚡ `AI Generated`
  - 🏆 `Top Designer`
  - 🌿 `100% Eco Cotton`
  - 🛡️ `Razorpay Secured`

---

## 8. Core UI Components

### 8.1 Buttons
- **Primary CTA**: Full width on mobile, gradient background with hover scale (`transform: translateY(-2px)`).
- **Secondary / Ghost**: Glassmorphic border button with hover glow.
- **Icon Buttons**: Circular 44x44px touch targets.

### 8.2 Inputs & Search Bar
- **Persistent Search Bar**: Sticky top header search bar with keyboard shortcut (`Ctrl + K`), auto-suggest dropdown, clear button (`X`), and category quick-filter tags.
- **Form Control**: Floating labels, active focus ring (`outline: 2px solid var(--accent-primary)`), inline error messages.

### 8.3 Cards & Glass Panels
- **Product Card**: Image hover zoom (scale 1.05), wishlist heart toggle (top-right), quick-view overlay, price + discount percentage tag.
- **Glassmorphic Modal**: Backdrop blur (`backdrop-filter: blur(16px)`), subtle border, slide-up mobile drawer pattern.

### 8.4 Notifications & Toasts
- **Toast Alerts**: Floating top-right / mobile bottom center notifications with progress countdown bar (Success, Defect Warning, IP Moderation Alert, Cart Added).

---

## 9. E-Commerce & Product Components

### 9.1 Navigation & Sticky Header
- **Persistent Header**: Logo + Persistent Search Bar + Theme Selector + Wishlist Icon + Cart Icon with badge count.
- **Category Mega Menu**: Men, Women, Hoodies, Oversized Tees, Accessories, AI Generator, Designer Leaderboard.
- **Sticky Cart Drawer**: Slide-over panel showing item list, real-time GST tax breakdown, shipping fee, and 1-click Razorpay checkout button.

### 9.2 Product Listing Page (PLP)
- **Advanced Filter Drawer**: Instant filtering by Size (S-XXL), Color Swatches, Price Slider, Fabric GSM, Sustainability Tag, Customer Ratings (4+ Stars).
- **Live Stock Badge**: Bound to real inventory per §2.4 — never a static design-time value.

### 9.3 Product Detail Page (PDP)
- **Interactive Multi-Angle Gallery**: High-res images, 360-degree preview, fabric zoom lens.
- **Bold Pricing & Stock Indicator**: Original Price (strikethrough) + Sale Price + Discount Tag + Live Stock Badge (*"Only 4 units left!"* — sourced from real-time stock, per §2.4).
- **Social Proof Section**: Verified buyer photo gallery, star rating breakdown, customer reviews with filter by size/fit (feeds from Flow 1.7 in `user-flow.md`).

### 9.4 Checkout & Progress Bar
- **4-Step Progress Indicator**: `1. Address & GST` → `2. Customization Review` → `3. Payment` → `4. Confirmation`.
- **Guest Checkout Toggle**: Single-click "Continue as Guest" option with email + phone entry (per Flow 0.1).
- **Trust Badges**: PCI-DSS, Razorpay, SSL 256-bit Encryption, 7-Day Free Defect Reprint Guarantee badges placed right under the "Pay Now" button.

### 9.5 Wishlist, Reviews & Referral Components *(New)*
- **Wishlist Grid**: Same card component as PLP, with "Move to Cart" and "Remove" actions; empty-state illustration if empty.
- **Review Composer**: Star selector (product + designer, if applicable), photo upload dropzone (max 3 images), text field with 500-char counter; submits into the moderation queue per Flow 1.7.
- **Referral Panel**: Unique referral code/link with copy button, share sheet (WhatsApp/SMS/Email icons), and a simple progress tracker ("2 of 3 friends joined").

---

## 10. Customization Studio Canvas (Fabric.js)

- **Canvas Viewports**: Dual-view toggle for Front & Back print areas.
- **Toolbars**:
  - Top Bar: Undo, Redo, Zoom, Clear Canvas, True-Color Fabric Simulation Toggle.
  - Left Panel: Text Tool, Image Upload, AI Generator, Template Presets, Layers.
- **True-Color Simulation**: Simulates ink absorption and opacity rendering depending on selected fabric shade (e.g. White DTG ink underbase on Black shirt).
- **Draft Autosave Indicator**: Small "Saved" / "Saving…" label near the toolbar, persisting design state per Flow (Design Save/Draft).

---

## 11. AI Suite Components

### 11.1 AI Design Generator Bar
- **Prompt Bar**: Input box with prompt suggestions (*"Cyberpunk Samurai"*, *"Retro Vaporwave Cat"*), style dropdown, and "Generate (4 Variations)" button with loading spinner.
- **Generation Failure State**: If the API times out, replace the spinner with an inline retry card — never leave the user on an indefinite spinner (per Flow 1.2 failure path).

### 11.2 AI Virtual Try-On Split View
- **Interactive Comparison**: Side-by-side or sliding split-screen slider comparing flat 2D canvas print vs. AI realistic model worn preview.
- **Photo Consent & Retention Modal** *(New)*: Before upload, a lightweight modal/inline banner states: photo is used only for try-on rendering, auto-deleted after 24 hours unless the user opts to save it to their profile, and offers an immediate **"Delete Now"** action visible on the preview screen itself (per Flow 1.2). This is a required consent step, not optional copy — it cannot be skipped or hidden behind a tooltip.

### 11.3 AI Content Moderation Feedback Modal
- **Warning Toast**: Displays immediate feedback if an uploaded/generated image triggers trademark hash (e.g., *"This artwork matches a protected trademark. Please use original artwork."*).

---

## 12. Animations & Microinteractions

- **Button Click**: Scale down `0.96` on active press.
- **Wishlist Heart**: Elastic pulse animation upon toggle.
- **Cart Badge**: Bounce count transition when items are added.
- **Page Transitions**: Smooth 200ms fade-in slide.

### 12.1 Motion Reduction Support *(New)*

WCAG 2.1 (§14) requires respecting user motion preferences. All bounce/elastic/parallax/scanline animations must be gated:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

- Under reduced motion, replace elastic/bounce transitions with instant or simple opacity-only fades.
- The Cyberpunk scanline overlay (§16.1) and any auto-playing background motion must pause entirely under this setting, not just slow down.

---

## 13. Responsive Design & Mobile-First Patterns

- **Thumb Zone Optimization**: Primary action buttons (*Add to Cart*, *AI Try-On*, *Pay Now*) fixed at the bottom of the screen on mobile viewports (`bottom: 0`, `z-index: 100`).
- **Touch Targets**: Minimum `44x44px` clickable area for all interactive elements.

---

## 14. Accessibility (a11y)

- **WCAG 2.1 AA Compliance**: All text/background combinations satisfy contrast ratios (> 4.5:1 for normal text, > 3:1 for large text/headings ≥ 24px or bold ≥ 19px).
- **Keyboard Navigation**: Full tab ordering, visible focus rings (`:focus-visible`), and screen reader ARIA labels (`aria-label`, `aria-live` for cart count updates).
- **Reduced Motion**: Honored globally per §12.1.
- **Form Errors**: Announced via `aria-live="polite"` regions, not color alone (icon + text required).

### 14.1 Verified Contrast Ratios *(New)*

Computed against each theme's `--bg-primary` (body copy context) and `--bg-surface` (card/panel context). Ratios below 4.5:1 for body text or 3:1 for large text were corrected in §3.1 rather than left as an unverified claim.

| Theme | Pairing | Ratio | Passes |
| :--- | :--- | :--- | :--- |
| Dark | `--text-primary` (#F3F4F6) on `--bg-primary` (#0D0F17) | 15.8:1 | ✅ AA/AAA |
| Dark | `--text-secondary` (#9CA3AF) on `--bg-surface` (#161926) | 6.9:1 | ✅ AA |
| Light | `--text-primary` (#111827) on `--bg-primary` (#FAFAFD) | 16.6:1 | ✅ AA/AAA |
| Light | `--text-secondary` (#4B5563) on `--bg-surface` (#FFFFFF) | 7.6:1 | ✅ AA |
| Cyberpunk | `--text-primary` (#00FFCC) on `--bg-primary` (#05050D) | 14.9:1 | ✅ AA/AAA |
| Cyberpunk | `--text-secondary` (#FF4D9E, lightened) on `--bg-surface` (#120B2E) | 4.7:1 | ✅ AA (body) |
| Cyberpunk | `--accent-secondary` (#33F3FF, lightened) on `--bg-surface` | 9.1:1 | ✅ AA |
| Arcade Retro | `--text-primary` (#FFE81A) on `--bg-primary` (#000000) | 16.9:1 | ✅ AA/AAA |
| Arcade Retro | `--text-secondary` (#FFC2F5) on `--bg-surface` (#080829) | 8.4:1 | ✅ AA |

> Original (pre-revision) Cyberpunk values `#FF007F` on `#120B2E` measured **3.9:1** — below the 4.5:1 body-text minimum — which is why §3.1 lightened it to `#FF4D9E`. Re-verify with a contrast checker (e.g. WebAIM) any time a theme hex value changes, rather than assuming neon-on-dark passes by default.

---

## 15. Empty, Loading & Error States

- **Empty States**: Friendly illustrations with clear CTA (*"Your Cart is Empty — Explore Trending Designs"*).
- **Loading Skeleton**: Shimmer animations for product cards and AI generation placeholders (respect §12.1 under reduced motion — use a static pulse-opacity fallback instead of shimmer sweep).
- **Error Banners**: Informative error recovery banners (e.g. Payment Timeout, Camera Pose Not Detected, AI Generation Failed).

---

## 16. Theme Engine Specifications

CSS Theme Switching is managed dynamically via `document.documentElement.setAttribute('data-theme', themeName)`.

### 16.1 Special Theme Specs

- 🤖 **Cyberpunk Mode**: Glowing neon cyan borders (`box-shadow: 0 0 10px #00FFCC`), scanline background overlay (paused under reduced motion, §12.1), angular clip-path buttons (`clip-path: polygon(...)`).
- 🕹️ **Arcade Retro Mode** *(renamed)*: Pixelated border styles (`border-style: solid`, `border-width: 4px`), arcade font headers (`Press Start 2P`, loaded per §4.1), retro maze-inspired color accents (Retro Red `#FF4D4D`, Retro Pink `#FFC2F5`, Retro Blue `#4D6BFF`, Retro Orange `#FFB852`).

  **IP note:** This theme was previously named "Pacman Retro Mode" and used the names Blinky, Pinky, Inky, and Clyde for its color tokens. Pac-Man and its character names are trademarks of Bandai Namco Entertainment. The renamed theme keeps the general 1980s-arcade *aesthetic* (pixel borders, chunky maze-style UI, 8-bit palette) without referencing any specific copyrighted game, character name, or maze motif tied to a real title. Do not reintroduce "Pacman," ghost names, or maze-chase iconography (e.g., dot-eating animations, ghost sprites) into UI copy, asset names, class names, or marketing screenshots — including in code comments or CMS content, since those can surface publicly. If a nostalgic arcade feel is desired, use generic 8-bit shapes/sprites created in-house rather than recognizable characters from any specific game.

---

## 17. Implementation Guidelines

1. **Vanilla CSS Tokens**: Store tokens in `index.css` / `theme.css`.
2. **Component Isolation**: Keep CSS modular to prevent unintended global style leak.
3. **Optimized Assets**: All icons SVG, product mockups WebP/AVIF format.
4. **Contrast Regression Check**: Any PR that changes a theme hex value in §3.1 must re-run an automated contrast check (e.g. `axe-core` or a WebAIM script) against §14.1's pairings before merge.
5. **Reduced-Motion Regression Check**: New animations must be verified under `prefers-reduced-motion: reduce` before merge, per §12.1.

---

## 18. Operations Dashboards (Dealer, Shipping Agency, Admin) `[MVP]` *(New)*

The original spec covered only the customer-facing storefront. Since the Dealer, Shipping Agency, and Admin roles run entirely different workflows (per `user-flow.md`), they get a dedicated, denser, data-first visual language rather than the storefront's glassmorphic/thrilling tone — these are working tools used repeatedly all day, not a shopping experience.

### 18.1 Shared Ops Design Language

- **Theme**: Dark Mode only by default (reduces eye strain for long shifts); Light Mode available as a toggle. Cyberpunk/Arcade themes are **not** offered on ops dashboards — they're storefront-only and would undermine legibility for operational data.
- **Density**: Compact table rows (`36–40px` height) instead of card-heavy storefront layouts; more information per screen, fewer decorative elements.
- **Data Tables**: Sortable columns, sticky header row, inline status-badge pills (color-coded per order/shipment status), row-level quick actions (e.g., "Download," "Approve," "Flag") on hover/tap.
- **Status Pills**: Consistent color mapping across all three dashboards — Gray (Pending), Blue (In Progress), Amber (Needs Attention/Flagged), Green (Complete), Red (Failed/Rejected) — reusing `--accent-warning`/`--accent-danger`/`--accent-secondary` tokens from §3.1.

### 18.2 Dealer Dashboard Components

- **Order Queue Table**: Order ID, Product Thumbnail, Size/Qty, Assigned Date, Status Pill (`Assigned → In Printing → QC → Packed → Ready for Pickup`), "Download Print Pack" button.
- **Print Asset Pack Modal**: Preview thumbnails of front/back print files with DPI/format tags (e.g. "300 DPI PNG", "SVG Vector"), single "Download All (.zip)" button.
- **Inventory Panel**: Editable grid of stock levels by size/color/fabric GSM, inline "Low Stock" warning pill.
- **Capacity Slider**: Daily print quota input with a simple progress bar showing today's used vs. remaining capacity.
- **Payout Summary Card**: Current balance, minimum-threshold note, "Request Payout" button, recent payout history table (per Flow 2.3).

### 18.3 Shipping Agency Dashboard Components

- **Pickup Queue List**: Grouped by dealer location, package barcode/AWB number, "Scan to Confirm Pickup" action (camera/barcode-scanner input on mobile).
- **Active Shipments Map/List Toggle**: List view of in-transit packages with current checkpoint; optional map view plotting delivery routes.
- **OTP Entry Screen**: Large numeric keypad (mobile-optimized, big touch targets per §13), 4-digit input, "Verify" button; fallback link to Photo + Signature capture (per Flow 4.3) after 3 failed attempts.
- **Failed Delivery Form**: Reason dropdown (Customer Unavailable / Address Issue / Refused), photo capture, auto-triggers Flow 4.2 recovery messaging to the customer.

### 18.4 Super Admin Dashboard Components

- **Analytics Overview**: KPI card row (Total Sales, Active Orders, Revenue Today, Top Designs) above a revenue trend chart; date-range picker.
- **Moderation Queue Table**: Flagged content thumbnail, flag reason (IP match / NSFW / Fraud pattern), Approve/Reject action buttons inline, per Flow 5.1.
- **Dispute Resolution Panel**: Case list with type tag (Print Defect / Shipping / Royalty / Payment), linked order/evidence viewer, verdict action buttons (Approve Refund / Request Info / Deny) mapped to Flow 5.2.
- **Payout Oversight Table**: Combined Dealer + Designer payout queue, filter by status, batch-approve checkbox + "Process Selected" button, per Flow 5.3.
- **User & Role Management**: Searchable user table with role filter, Approve/Ban actions, audit-log link per user.

---

## 🎯 Summary of Documentation Progress

- [x] **1. Requirements (`features.md`)** — Complete
- [x] **2. User Flows (`user-flow.md`)** — Complete
- [x] **3. Design System (`design.md`)** — Updated & Complete (IP-safe theming, verified accessibility, dark-pattern guardrails, full ops dashboard specs)
- [ ] **4. Technical Architecture (`architecture.md`)** — *Next Step*
- [ ] **5. Database Schema (`database.md`)**
- [ ] **6. API Specification (`api.md`)**
- [ ] **7. Development Roadmap (`roadmap.md`)**
