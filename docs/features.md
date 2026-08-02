# DoodleWear — Product Requirements & Features (features.md)

---

## 📌 Executive Summary

**DoodleWear** is a next-generation AI-powered custom e-commerce platform designed to revolutionize personalized apparel shopping. By combining a 2D/3D design editor, AI design generation, AI image superimposition, AI virtual try-on, automated content moderation & IP protection, smart fashion recommendations, and multi-role operations (Customers, Dealers/Designers, Shipping Agencies, Super Admins), DoodleWear connects buyers, custom print production dealers, and logistics partners seamlessly.

---

## 👥 User Roles & Access Hierarchy (RBAC)

1. **Customer**: Browses products, designs custom apparel using templates or AI/manual tools, performs AI virtual try-ons, requests reprints/returns, purchases via Razorpay, and tracks orders.
2. **Dealer / Print Partner**: Undergoes certification onboarding, receives screened design print files, prepares & prints apparel, performs AI/manual quality checks, packages products, and hands over to shipping agencies.
3. **Designer / Creator**: Publishes designs to the marketplace, tracks performance on personal analytics dashboards, climbs the leaderboard, and earns royalties.
4. **Shipping Agency / Logistics Partner**: Manages package pickups, updates real-time tracking checkpoints, handles transit status, and completes deliveries (with OTP/photo proof).
5. **Super Admin**: Controls platform settings, reviews content moderation flags, manages dealer onboarding approvals, oversees GST tax compliance, handles payouts, and monitors fraud detection.

---

## 🚀 Feature Matrix & Prioritization

Features are categorized into 3 implementation phases:
- 🟢 **MVP (Phase 1)**: Core e-commerce, basic 2D studio, content moderation, order fulfillment, GST invoicing, defect reprints, Razorpay payments.
- 🔵 **AI Enhancements (Phase 2)**: AI Design Generator, Image Superimposition, AI Virtual Try-On, AI Automated QC, multi-language support, and fashion recommendations.
- 🟣 **Future Roadmap (Phase 3)**: Designer Leaderboard & Storefronts, Creator Marketplace with Royalties, AR try-on, multi-dealer order splitting, and AI style transfer.

---

## 1. 🛍️ Customer-Facing Features

### 1.1 Core E-Commerce & Shopping Experience
- **Product Catalog & Filtering** `[MVP]`
  - Browse apparel by category (T-Shirts, Hoodies, Sweatshirts, Caps, Jackets).
  - Filter by color, size (S, M, L, XL, XXL), gender, fabric GSM, price range, and popularity.
- **Product Detail Page (PDP)** `[MVP]`
  - High-res product images, fabric details, size guide chart, washing instructions, and stock availability.
  - **Sustainability Tagging** `[Phase 2]`: Displays eco-friendly fabric badges (100% Organic Cotton, Recycled Polyester) and estimated carbon footprint per order.
- **Wishlist & Save for Later** `[MVP]`
  - Save items or custom design concepts to account wishlist with one-click move to cart.
- **Reviews & Ratings** `[MVP]`
  - Verified buyer ratings with photo and video uploads showing received apparel. Feeds directly into product and designer credibility ratings.
- **Shopping Cart & Checkout** `[MVP]`
  - Add to Cart with selected size, color, quantity, and custom design metadata.
  - Price breakdown: Base product + customization fee + GST breakdown + shipping fee.
  - Coupon / promo code application.
- **Abandoned Cart Recovery & Nudges** `[MVP]`
  - Automated WhatsApp, Email, and Push notifications reminding users of unpurchased custom carts with direct checkout links.
- **Payment Gateway Integration** `[MVP]`
  - Native **Razorpay** integration supporting UPI, Credit/Debit Cards, Net Banking, and Wallet payments.
- **GST & Invoicing Automation** `[MVP]`
  - Automatic calculation of CGST, SGST, and IGST based on customer & dealer state location.
  - Downloadable GST-compliant PDF Tax Invoices generated automatically post-purchase.
- **Customer Account, Order Tracking & History** `[MVP]`
  - Order tracking timeline (Ordered -> Content Moderated -> Sent to Dealer -> In Printing -> Quality Checked -> Handed to Courier -> Out for Delivery -> Delivered).
- **Digital Gift Cards & E-Vouchers** `[MVP]`
  - Purchase and redeem custom apparel digital gift cards with custom messages.
- **Referral Program** `[Phase 2]`
  - "Give ₹100, Get ₹100" viral referral code system to incentivize new user acquisition.
- **Multi-Language Support** `[Phase 2]`
  - Regional language toggle (English, Hindi, Tamil, Telugu, Marathi, etc.) tailored for Indian market accessibility.

### 1.2 Custom Design Studio & Canvas Editor
- **Starter Template Library** `[MVP]`
  - Pre-designed editable templates organized by occasion (Birthdays, College Fests, Corporate Events, Gym/Fitness, Gaming, Sports Teams).
- **2D Canvas Design Editor** `[MVP]`
  - Interactive canvas (powered by Fabric.js) for Front & Back print zones.
  - Text Tool: Add text with custom fonts, colors, curves, outlines, and shadows.
  - Image Upload: Upload custom PNG/JPEG logos/artwork with scaling, rotation, and grid alignment.
- **Drafts & Version History** `[MVP]`
  - Save in-progress custom designs to profile; auto-save functionality and version history undo/redo revert capabilities.
- **Collaborative Design Link Sharing** `[Phase 2]`
  - Shareable preview link allowing friends and family to view, comment on, or vote on a custom design before checkout.
- **Print Preview Simulation & Color Realism** `[MVP]`
  - True-color fabric preview simulating ink absorption on dark vs. light fabrics, avoiding screen-to-print color mismatch.
- **AI Background Remover** `[AI Enhancement - Phase 2]`
  - One-click background removal for user-uploaded logos/images before placement.

---

## 2. 🛡️ Content Moderation, Copyright & Post-Purchase Workflows `[MVP]`

### 2.1 Automated Content Moderation & IP Protection `[MVP]`
- **Perceptual Hashing & Trademark Screening**: Automated matching against known trademark database (Nike swoosh, Disney, Marvel, Adidas, sports team logos).
- **NSFW & Hate Speech Classifier**: AI vision model scans uploaded/generated graphics and text for offensive imagery, hate speech, or explicit content.
- **Moderation Flagging**: Suspicious designs are placed in an Admin Moderation Queue for manual approval before hitting the print queue, shielding the platform from legal liability.

### 2.2 Returns, Exchanges & Defect Reprint Workflow `[MVP]`
- **Defect Reprint Request**: Customers can flag physical print defects (peeling ink, misalignment, wrong color, damaged garment) by uploading 2 photos within 7 days.
- **1-Click Dealer Reprint Routing**: Direct re-issue of print job to the dealer without requiring a full refund cycle.
- **Return & Exchange Management**: Smooth returns/exchanges for sizing issues or damaged shipping packages.

---

## 3. 🤖 AI Suite (AI-Powered Customization & Shopping)

### 3.1 AI Design Generator & Style Transfer `[AI Enhancement - Phase 2]`
- **Text-to-Design Generation**: User inputs text prompt $\rightarrow$ AI generates 4 high-res design options $\rightarrow$ 1-click import to canvas.
- **AI Design Style Transfer / Re-Imaginer** `[Phase 3]`: Converts rough doodles or photos into artistic styles (Anime, Cyberpunk, Vintage, Vector, Watercolor).

### 3.2 AI Image-to-Apparel Superimposition (Smart Mockup) `[AI Enhancement - Phase 2]`
- **Auto-Fit & Superimpose**: AI detects clothing contours, perspective grid, and fabric wrinkles to realistic superimpose uploaded images onto apparel.

### 3.3 AI Virtual Try-On Engine `[AI Enhancement - Phase 2]`
- **User Photo Try-On**: User uploads photo $\rightarrow$ AI aligns torso & posture $\rightarrow$ renders realistic worn preview with natural shadows and fabric folds.

### 3.4 AI Fashion & Styling Recommendations `[AI Enhancement - Phase 2]`
- **Color Contrast & Harmony**: AI recommends optimal shirt colors matching the design artwork.
- **Fit & Size Recommendation**: Suggests regular vs. oversized fit based on body style and design aesthetic.
- **Outfit Cross-Selling**: Suggests matching products (jeans, jackets, caps).

### 3.5 AI Design Enhancement & Quality Audit `[AI Enhancement - Phase 2]`
- **Resolution Upscaling & Vectorization**: Upscales low-res uploads into crisp 300 DPI vector images using AI super-resolution.
- **Text Readability & Contrast Audit**: Warns if font size or color contrast will yield poor physical print quality.

---

## 4. 🏬 Dealer / Print Partner Operations & Quality Control

### 4.1 Dealer Onboarding & Certification Workflow `[MVP]`
- **Registration & Verification**: Dealers submit business GSTIN, machinery details (DTG, Screen Printing, Sublimation), and print capacity.
- **Sample Quality Certification**: Admin reviews sample print submissions before activating dealer accounts.

### 4.2 Order Processing & Print Queue `[MVP]`
- **New Order Notifications**: Real-time alerts for print-approved orders.
- **Print Asset Pack Export**: One-click download of 300 DPI vector files, color separation specs, and precise placement coordinates.
- **Workflow Pipeline**: `Assigned` $\rightarrow$ `In Printing` $\rightarrow$ `QC Passed` $\rightarrow$ `Packed` $\rightarrow$ `Ready for Pickup`.

### 4.3 Multi-Dealer Order Splitting `[Phase 2]`
- **Auto-Routing Bulk Orders**: Algorithm splits large corporate or multi-item orders across multiple certified dealers based on geographic proximity, item type, and daily print capacity.

### 4.4 Automated Quality Control (QC) via AI `[AI Enhancement - Phase 2]`
- **Camera-Based Defect Inspection**: Dealer scans printed apparel photo prior to packaging; AI vision detects misalignments, ink bleeds, or color mismatches, reducing return rates.

---

## 5. 🏆 Creator Marketplace, Leaderboard & Analytics `[Phase 3]`

### 5.1 Best-Selling Designer Leaderboard `[Phase 3]`
- **Rankings & Gamified Badges**: Real-time leaderboard with badges (*"Top Seller"*, *"Trending Creator"*, *"Master Designer"*).
- **Auto-Promotions**: Top designers automatically featured on homepages, category feeds, and AI recommendations.

### 5.2 Designer Storefront & Analytics Dashboard `[Phase 3]`
- **Personalized Storefront**: Custom creator landing pages (`/designer/brand-name`).
- **Designer Analytics Dashboard**: Designers track total views, sales volume, conversion rates, trending designs, and royalty payouts.

---

## 6. 🚚 Shipping Agency & Logistics Dashboard `[MVP]`

- **Pickup Queue & Barcode Scan**: Scan package barcodes to confirm package pickup into transit.
- **Real-Time Checkpoints**: Status pipeline (`Picked Up` $\rightarrow$ `In Transit` $\rightarrow$ `Out for Delivery` $\rightarrow$ `Delivered`).
- **Proof of Delivery (PoD)**: 4-digit customer OTP verification upon delivery.

---

## 7. ⚙️ Super Admin, Security & Operations `[MVP]`

- **Comprehensive Analytics Dashboard**: Sales metrics, top designs, dealer performance, shipping status.
- **Content Moderation Desk**: Review flagged copyright/NSFW designs.
- **Payouts & Commission Management**: Automated dealer print payments, creator royalties, and platform commission calculations.
- **Fraud & Anomaly Detection**: Automated flagging of suspicious order patterns, fake address patterns, or unusual payment attempts.

---

## 🔄 Updated Complete User Flow Architecture

```mermaid
flowchart TD
    A[Customer Visits DoodleWear] --> B{Choose Action}
    B -->|Option 1| C[Browse Catalog or Templates]
    B -->|Option 2| D[AI Design Generator - Text Prompt]
    B -->|Option 3| E[Upload Custom Image]
    B -->|Option 4| F[Browse Top Designer Leaderboard]

    D -->|Generates Options| G[Select Design]
    E -->|AI Image Superimposition| H[Auto-Fit & Superimpose on Garment]
    F -->|Select Designer Art| G

    C --> I[Open 2D Canvas Editor]
    G --> I
    H --> I

    I -->|Save Draft / Customize Layout| J[AI & Automated IP Content Moderation]
    J -->|Flagged| K[Admin IP/NSFW Review]
    J -->|Passed| L[AI Quality & Contrast Audit]
    K -->|Approved| L

    L --> M[AI Virtual Try-On Realistic Preview]
    M --> N[Select Size & View True-Color Preview]
    N --> O[Checkout with Razorpay & Auto GST Invoice]

    O -->|Payment Success| P[Order Assigned to Certified Dealer]
    
    subgraph Production, QC & Delivery
        P --> Q[Dealer Downloads 300 DPI Print File]
        Q --> R[Garment Printed & AI Camera QC Verified]
        R --> S[Packed & Waybill Generated]
        S --> T[Shipping Agency Accepts Package]
        T --> U[Live Tracking & Out for Delivery]
        U --> V[Delivered with OTP Verification]
        V -->|If Defective| W[1-Click Customer Defect Reprint Request]
    end
```

---

## 🎯 Summary of Documentation Progress

- [x] **Requirements (`features.md`)** — Fully Complete & Updated
- [ ] **User Flows (`user-flow.md`)** — Pending Next Step
- [ ] **Design System (`design.md`)**
- [ ] **Technical Architecture (`architecture.md`)**
- [ ] **Database Schema (`database.md`)**
- [ ] **API Specification (`api.md`)**
- [ ] **Development Roadmap (`roadmap.md`)**
