# DoodleWear — Comprehensive User Flows & Navigation Journeys (user-flow.md)

---

## 📌 Executive Summary

This document defines the complete end-to-end user navigation flows, interaction states, decision logic, and error recovery paths across all 5 primary roles on **DoodleWear**:
1. 🛍️ **Customer Journeys**
2. 🏬 **Dealer / Print Partner Journeys**
3. 🏆 **Designer / Creator Journeys**
4. 🚚 **Shipping Agency / Logistics Journeys**
5. ⚙️ **Super Admin Operations Journeys**

---

## 0. 🔐 Authentication & Session Flows `[MVP]`

*(New — every downstream flow assumes the actor is authenticated; this section makes that explicit.)*

### Flow 0.1: Signup, Login & Guest Checkout Decision

```mermaid
flowchart TD
    A[Visitor Opens DoodleWear] --> B{Has Account?}
    B -->|New User| C[Click Sign Up]
    B -->|Existing User| D[Click Login]
    B -->|Skip for Now| E[Continue as Guest]

    C --> F{Signup Method}
    F -->|Email/Password| G[Enter Email, Password, Phone]
    F -->|Social OAuth| H[Google / Apple OAuth Consent]
    G --> I[Send OTP/Email Verification Link]
    I --> J{Verified?}
    J -->|Yes| K[Account Created -> Redirect to Homepage]
    J -->|No, 24hr expiry| L[Resend Verification / Account Stays Unverified]
    H --> K

    D --> M[Enter Credentials]
    M --> N{Valid?}
    N -->|Yes| K
    N -->|No, 3 attempts| O[Account Temp-Locked 15 min + Reset Link Sent]

    E --> P[Browse & Design as Guest - Session Cart Only]
    P --> Q[At Checkout: Prompt 'Create account to track this order?']
    Q -->|Yes| C
    Q -->|No| R[Guest Checkout: Email + Phone Only, No Saved Profile]
```

### Flow 0.2: Password Reset

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant Frontend
    participant Backend
    participant Email as Email/SMS Service

    User->>Frontend: Click "Forgot Password"
    User->>Frontend: Enter registered Email/Phone
    Frontend->>Backend: POST /api/auth/reset-request/
    Backend->>Email: Send Reset Link/OTP (expires in 15 min)
    User->>Frontend: Click Link -> Enter New Password
    Frontend->>Backend: POST /api/auth/reset-confirm/
    Backend-->>Frontend: Password Updated -> Auto Login
```

**Note:** All role dashboards (Dealer, Designer, Shipping Agency, Admin) reuse Flow 0.1's login pattern with role-based redirect after authentication, but do **not** offer guest access.

---

## 1. 🛍️ Customer Navigation Journeys

---

### Flow 1.1: Standard Catalog Shopping Flow `[MVP]`

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant Frontend as Website / App UI
    participant Backend as Django Server
    participant DB as Database
    participant Razorpay as Razorpay Gateway

    Customer->>Frontend: Open Homepage & Browse Catalog
    Frontend->>Backend: GET /api/products/?category=t-shirts&size=L
    Backend->>DB: Query Products
    DB-->>Backend: Return Filtered Apparel List
    Backend-->>Frontend: Display Product Cards
    Customer->>Frontend: Select Product (e.g., Heavyweight Oversized Tee)
    Customer->>Frontend: Select Color, Size (L), and Quantity
    Customer->>Frontend: Click "Add to Cart"
    Frontend->>Backend: POST /api/cart/add/
    Backend-->>Frontend: Cart Updated (Count + 1)
    Customer->>Frontend: Proceed to Checkout
    Customer->>Frontend: Enter Shipping Address & GSTIN (Optional)
    Frontend->>Backend: POST /api/checkout/
    Backend->>Razorpay: Create Order ID
    Razorpay-->>Backend: Order Token
    Backend-->>Frontend: Launch Razorpay Modal
    Customer->>Razorpay: Complete Payment (UPI / Card)
    Razorpay-->>Backend: Webhook: Payment.Captured
    Backend->>DB: Update Order Status -> "Paid", Generate Invoice PDF
    Backend-->>Frontend: Redirect to Order Confirmation Page
```

---

### Flow 1.2: AI Design Generation & Virtual Try-On Flow `[AI Enhancement]`

```mermaid
flowchart TD
    A[Customer enters Studio] --> B[Click 'AI Design Generator']
    B --> C[Enter Text Prompt e.g., 'Minimalist cyberpunk fox with neon highlights']
    C --> D[Select Style: Cyberpunk / Anime / Vector / Minimalist]
    D --> E[Submit Prompt to AI Generator API]

    E --> F{AI Content & IP Screening}
    F -->|Flagged IP/NSFW| G[Display Warning: 'Prompt violates copyright/safety policy']
    G --> C
    F -->|Passed| H[Generate 4 High-Res Design Options]
    F -->|API Timeout / Generation Failure| Z1[Show 'Generation Failed' + Retry Button]
    Z1 --> E

    H --> I[Customer selects preferred option]
    I --> J[Import directly into 2D Canvas Editor]
    J --> K[Optionally add custom text, scale, or rotate]
    K --> L[Click 'AI Virtual Try-On']

    L --> M[Upload User Photo or select Model Persona]
    M --> M1[Display Data Retention Notice: 'Photo stored 24h for preview, then auto-deleted unless saved to profile']
    M1 --> N[AI Torso Alignment & Fabric Overlay Engine]
    N --> O[Display Realistic Preview showing worn shirt]
    N -->|Alignment Failure - no torso detected| Z2[Prompt: 'Could not detect pose, try a clearer front-facing photo']
    Z2 --> M

    O --> P{Customer Action}
    P -->|Edit Further| J
    P -->|Delete Uploaded Photo Now| Z3[Immediate Purge from Storage & Preview]
    P -->|Satisfied| Q[Select Size & Add to Cart]
    Q --> R[Proceed to Razorpay Payment]
```

---

### Flow 1.3: Custom Image Upload & AI Superimposition Flow `[AI Enhancement]`

```mermaid
flowchart TD
    A[Customer clicks 'Upload My Artwork'] --> B[Select PNG/JPEG image from device]
    B --> C[AI Automated Content & IP Screening]

    C --> D{Perceptual Hash & NSFW Check}
    D -->|Match Trademark / NSFW| E[Block Upload: 'Copyrighted logo or inappropriate image detected']
    D -->|Passed| F[AI Background Removal Tool (Optional)]
    D -->|Scan Service Timeout| Z1[Hold Upload in 'Pending Review' + Notify Customer of Delay]
    Z1 --> C

    F --> G[AI Image-to-Apparel Superimposition Engine]
    G --> H[Auto-fit & map graphic onto apparel contours with realistic fabric folds]
    H --> I[True-Color Fabric Simulation Preview]
    G -->|Superimposition Engine Failure| Z2[Fallback: Show Flat 2D Print Preview Only + Notice]

    I --> J[Save Design Draft to Profile]
    J --> K[Select Apparel Color & Size]
    K --> L[Proceed to Checkout & Razorpay Payment]
```

---

### Flow 1.4: Defect Reprint & Return Claim Flow `[MVP]`

```mermaid
sequenceDiagram
    autonumber
    actor Customer
    participant Frontend as Website UI
    participant Backend as Django Server
    participant Admin as Super Admin / QC Desk
    participant Dealer as Print Partner

    Customer->>Frontend: Go to Order History -> Click "Report Issue"
    Customer->>Frontend: Select Reason: "Print Defect / Ink Peeling / Misalignment"
    Customer->>Frontend: Upload 2 Photos of physical defective garment + Description
    Customer->>Frontend: Submit Claim Request
    Frontend->>Backend: POST /api/orders/{id}/reprint-request/
    Backend->>Admin: Alert: Pending Defect Verification Queue
    Admin->>Backend: Approve Defect Claim (Valid Print Failure)
    Backend->>Dealer: Dispatch 1-Click Priority Reprint Order
    Backend-->>Customer: Email & SMS Notification: "Reprint Approved! Your new shirt is printing."
    Dealer->>Backend: Update Status -> "Reprint In Production"
```

---

### Flow 1.5: Order Cancellation Flow `[MVP]` *(New)*

```mermaid
flowchart TD
    A[Customer opens Order History] --> B[Click 'Cancel Order']
    B --> C{Current Order Status?}

    C -->|Paid, Not Yet Assigned to Dealer| D[Instant Cancellation]
    D --> E[Full Refund Initiated to Original Payment Method]
    E --> F[Refund Confirmation Email - 5-7 Business Days]

    C -->|Assigned to Dealer, Not Yet Printing| G[Cancellation Request Sent to Dealer]
    G --> H{Dealer Confirms Not Started?}
    H -->|Confirmed| D
    H -->|Already Cutting/Printing Material| I[Partial Refund Offered - Material Cost Deducted]
    I --> J{Customer Accepts Partial Refund?}
    J -->|Yes| K[Partial Refund Processed]
    J -->|No| L[Order Proceeds to Completion - Cancellation Denied]

    C -->|In Printing / Packed / Shipped| M[Cancellation Blocked]
    M --> N[Redirect to Flow 1.4 - Defect Claim Applies Only After Delivery]
```

---

### Flow 1.6: Bulk / Corporate Order Flow `[Phase 3]` *(New)*

```mermaid
sequenceDiagram
    autonumber
    actor Org as Corporate Buyer
    participant Frontend
    participant Backend
    participant Sales as Admin / Sales Desk
    participant Dealer as Print Partner(s)

    Org->>Frontend: Click "Bulk Order Inquiry" (50+ units)
    Org->>Frontend: Submit Quantity, Design(s), Sizes Breakdown, Delivery Deadline
    Frontend->>Backend: POST /api/bulk-orders/quote-request/
    Backend->>Sales: New Bulk Quote Request Alert
    Sales->>Backend: Review & Apply Tiered Volume Discount
    Backend-->>Org: Auto-Generated Quotation PDF (Price, Timeline, Terms)

    Org->>Frontend: Accept Quotation & Pay (Advance/Full via Razorpay)
    Backend->>Backend: Evaluate Single-Dealer vs Multi-Dealer Capacity (see Flow 2.4)
    Backend->>Dealer: Assign Order (Split if Required)
    Backend-->>Org: Order Confirmed with Consolidated Tracking ID
    Note over Org,Dealer: Proceeds through standard Flow 2.2 Production Workflow per dealer
```

---

### Flow 1.7: Post-Delivery Review & Rating `[MVP]` *(New)*

```mermaid
flowchart TD
    A[Order marked 'Delivered'] --> B[System sends Review Request - Email/App Notification after 3 days]
    B --> C[Customer opens 'Rate Your Order']
    C --> D[Rate Product Quality 1-5 Stars]
    C --> E[Rate Designer's Artwork 1-5 Stars - if applicable]
    C --> F[Optional Photo Upload of Worn Apparel]
    C --> G[Optional Written Review]
    D & E & F & G --> H[Submit Review]
    H --> I[Review Passed Through Auto-Moderation - Spam/Profanity Filter]
    I -->|Flagged| J[Held for Admin Approval]
    I -->|Clean| K[Published to Product Page & Designer Storefront]
    K --> L[Feeds Designer Leaderboard Rating Score]
```

---

## 2. 🏬 Dealer / Print Partner Operations Journeys

---

### Flow 2.1: Dealer Onboarding & Certification `[MVP]`

```mermaid
flowchart TD
    A[Print Vendor visits /dealer/register] --> B[Fill Business Form: GSTIN, Address, Machine Specs]
    B --> C[Submit Application]
    C --> D[Admin Reviews GSTIN & Capacity]
    D -->|Rejected| E[Send Rejection Email with Feedback]
    D -->|Approved| F[Request Sample Print Package]

    F --> G[Dealer prints and mails sample test apparel to Admin HQ]
    G --> H[Admin Quality Inspection]
    H -->|Failed QC| E
    H -->|Passed QC| I[Activate Dealer Account & Assign Geographic Print Region]
```

---

### Flow 2.2: Order Fulfillment & Printing Workflow `[MVP]`

```mermaid
flowchart TD
    A[New Approved Customer Order] --> B[Order assigned to Dealer via Proximity & Capacity]
    B --> C[Real-Time Notification & Dashboard Alert]
    C --> D[Click 'Download 300 DPI Print Asset Pack']

    D --> E[Print Asset Zip Contains: Vector PNG/SVG, Exact Position Coords, Color Codes]
    E --> F[Print Apparel on DTG / Sublimation Machine]
    F --> G[Manual & AI Camera Quality Inspection]

    G --> H{Defect Detected?}
    H -->|Yes| I[Discard & Re-print Garment]
    H -->|No| J[Package Garment & Attach Printed Shipping Label with Barcode]

    J --> K[Mark Order Status: 'Ready for Pickup']
    K --> L[Notify Shipping Agency for Pickup]
```

---

### Flow 2.3: Dealer Payout Processing `[MVP]` *(New)*

```mermaid
sequenceDiagram
    autonumber
    actor Dealer
    participant Dashboard as Dealer Dashboard
    participant Backend
    participant Admin as Finance Admin
    participant Bank as Bank Transfer / Payout Gateway

    Dealer->>Dashboard: View Earnings Summary (Completed Orders)
    Dealer->>Dashboard: Click "Request Payout"
    Dashboard->>Backend: POST /api/dealer/payout-request/
    Backend->>Backend: Validate Minimum Payout Threshold (e.g., ₹500)
    Backend-->>Dashboard: Threshold Not Met -> Show Balance Needed
    Backend->>Admin: Payout Request Queued for Approval
    Admin->>Backend: Verify Order Completion & Approve
    Backend->>Bank: Initiate NEFT/IMPS Transfer
    Bank-->>Backend: Transfer Success/Failure Webhook
    Backend-->>Dealer: Notification - "Payout of ₹X Credited" or "Payout Failed - Update Bank Details"
```

---

### Flow 2.4: Multi-Dealer Order Splitting `[Phase 3]` *(New)*

```mermaid
flowchart TD
    A[Bulk or Large Order Received] --> B[System Checks Nearest Dealer Capacity]
    B --> C{Single Dealer Can Fulfill Full Quantity?}
    C -->|Yes| D[Assign Entire Order to One Dealer]
    C -->|No| E[Split Order by Size/Quantity Across 2+ Nearby Dealers]

    E --> F[Each Dealer Receives Partial Print Asset Pack & Sub-Order ID]
    F --> G[Each Sub-Order Proceeds via Flow 2.2 Independently]
    G --> H[Backend Tracks All Sub-Orders Under Parent Order ID]
    H --> I{All Sub-Orders 'Ready for Pickup'?}
    I -->|No| J[Wait & Notify Customer of Partial Progress]
    I -->|Yes| K[Consolidate Pickup Request - Single or Multi-Location]
    K --> L[Shipping Agency Collects from All Dealer Locations]
    L --> M[Packages Consolidated or Shipped as Multi-Parcel to Customer]
```

---

## 3. 🏆 Designer / Creator Journeys `[Phase 3]`

---

### Flow 3.0: Designer Application & Approval `[Phase 3]` *(New)*

```mermaid
flowchart TD
    A[User clicks 'Become a Designer'] --> B[Fill Creator Profile: Bio, Portfolio Samples, Social Links]
    B --> C[Submit Application]
    C --> D[Admin Reviews Portfolio for Originality & Quality]
    D -->|Rejected| E[Send Feedback - Reapply After 30 Days]
    D -->|Approved| F[Creator Role Unlocked]
    F --> G[Personalized Storefront URL Generated]
    G --> H[Redirect to Design Studio -> Flow 3.1]
```

---

### Flow 3.1: Publishing Design & Earning Royalties

```mermaid
sequenceDiagram
    autonumber
    actor Creator as Designer / Creator
    participant Studio as Design Studio
    participant Moderation as IP Content Screening
    participant Marketplace as Public Design Hub
    participant Dashboard as Designer Analytics

    Creator->>Studio: Create or Upload Unique Artwork
    Creator->>Studio: Click "Publish to Creator Marketplace"
    Creator->>Studio: Set Custom Royalty Fee (e.g., ₹150 per shirt sold)
    Studio->>Moderation: Automated Copyright & NSFW Scan
    Moderation-->>Studio: Scan Passed
    Studio->>Marketplace: Publish Artwork to Designer Portfolio
    Marketplace-->>Creator: Unique URL Generated (doodlewear.com/designer/alex)

    Note over Marketplace: Customer buys apparel with Creator's Design
    Marketplace->>Dashboard: Credit ₹150 Royalty to Creator Wallet Balance
    Creator->>Dashboard: View Real-Time Sales Metrics & Click "Request Payout"
```

---

### Flow 3.2: Designer Payout Processing `[Phase 3]` *(New)*

```mermaid
flowchart TD
    A[Creator clicks 'Request Payout' from Wallet] --> B{Wallet Balance >= Minimum Threshold?}
    B -->|No| C[Show 'Minimum ₹500 required' + Current Balance]
    B -->|Yes| D[Payout Request Logged]
    D --> E[Admin Finance Review - Verify No Pending Disputes on Sales]
    E -->|Dispute Pending on a Sale| F[Hold Disputed Amount, Process Remainder]
    E -->|Clear| G[Approve Full Payout]
    F & G --> H[Initiate Bank Transfer / UPI Payout]
    H --> I{Transfer Successful?}
    I -->|Yes| J[Wallet Debited, Payout History Updated, Notification Sent]
    I -->|No| K[Retry Once -> If Fails, Flag for Manual Admin Resolution]
```

---

## 4. 🚚 Shipping Agency & Logistics Journeys `[MVP]`

---

### Flow 4.1: Pickup, Tracking & OTP Delivery Workflow

```mermaid
sequenceDiagram
    autonumber
    actor Logistics as Shipping Driver
    participant App as Logistics Mobile/Web App
    participant Backend as Django Server
    actor Customer as Buyer

    Logistics->>App: View Daily Pickup Queue (Dealer Locations)
    Logistics->>App: Arrive at Dealer Location & Scan Package Barcode
    App->>Backend: POST /api/shipments/scan-pickup/
    Backend-->>App: Pickup Verified -> Status: "In Transit"

    Note over Logistics,Backend: Package moves through transit hubs
    Logistics->>App: Update Checkpoint: "Arrived at Regional Hub"
    Logistics->>App: Mark Order: "Out for Delivery"
    Backend-->>Customer: SMS/WhatsApp Notification with 4-Digit Delivery OTP

    Logistics->>Customer: Arrive at Customer Address
    Logistics->>Customer: Request 4-Digit OTP
    Customer->>Logistics: Provides OTP (e.g., 5824)
    Logistics->>App: Enter OTP
    App->>Backend: POST /api/shipments/verify-otp/
    Backend-->>App: OTP Match Confirmed
    Backend-->>Customer: Status Updated -> "Delivered", Invoice & Receipt Sent
```

---

### Flow 4.2: Failed Delivery Attempt Recovery `[MVP]` *(New)*

```mermaid
flowchart TD
    A[Delivery Attempt Made] --> B{Outcome?}
    B -->|Customer Unavailable| C[Mark 'Failed Delivery Attempt 1' + Reason]
    B -->|Wrong/Incomplete Address| D[Mark 'Address Issue' + Reason]
    B -->|Customer Refuses Package| E[Mark 'Refused' + Reason]

    C --> F[Auto-SMS/WhatsApp to Customer: Reschedule Link]
    D --> G[Auto-Notify Customer: 'Please Update Address' Link]
    F & G --> H{Customer Responds within 48h?}
    H -->|Reschedules| I[New Delivery Slot Booked -> Retry, Attempt 2]
    H -->|No Response| J{Attempt Count < 3?}
    J -->|Yes| I
    J -->|No| K[Mark 'Delivery Failed - Returning to Dealer']

    E --> K
    K --> L[Package Routed Back to Origin Dealer]
    L --> M[Admin Notified -> Initiate Refund minus Return Shipping, per Policy]
    M --> N[Customer Notified of Refund & Reason]
```

---

### Flow 4.3: Proof of Delivery Exception Handling `[MVP]`

```mermaid
flowchart TD
    A[OTP Verification Fails 3x] --> B[Logistics App Offers Fallback]
    B --> C[Capture Digital Photo of Package at Doorstep]
    C --> D[Customer Digital Signature on Device - Optional]
    D --> E[Mark 'Delivered - Alternate Verification']
    E --> F[Flag Order for Admin Review if Customer Later Disputes Non-Receipt]
```

---

## 5. ⚙️ Super Admin Operations Journeys `[MVP]`

---

### Flow 5.1: Content Moderation & Fraud Inspection

```mermaid
flowchart TD
    A[System flags uploaded/generated graphic] --> B[Order sent to Admin Moderation Queue]
    B --> C[Admin inspects image against Trademark / NSFW guidelines]

    C --> D{Admin Verdict}
    D -->|Violates Policy| E[Reject Order & Refund Customer with Reason]
    D -->|Safe / Clear| F[Approve Order -> Send to Dealer Print Queue]

    G[System detects unusual COD / Payment pattern] --> H[Flag Order as Potential Fraud]
    H --> I[Admin calls/verifies customer address before approving dispatch]
```

---

### Flow 5.2: Dispute & Refund Resolution `[MVP]` *(New)*

```mermaid
flowchart TD
    A[Dispute Raised] --> B{Dispute Source}
    B -->|Print Defect - No Resolution via Flow 1.4| C[Escalated Defect Dispute]
    B -->|Lost/Never Arrived Shipment| D[Shipping Dispute]
    B -->|Designer Royalty Disagreement| E[Marketplace Dispute]
    B -->|Refund Not Received| F[Payment Dispute]

    C --> G[Admin Reviews Photos, Order History, Dealer QC Logs]
    D --> H[Admin Cross-Checks Shipping Agency Tracking Logs]
    E --> I[Admin Reviews Sales Ledger vs Royalty Terms]
    F --> J[Admin Checks Razorpay Refund Webhook Status]

    G & H & I & J --> K{Verdict}
    K -->|Customer/Designer Favor| L[Process Refund / Adjust Royalty / Reissue Payout]
    K -->|Insufficient Evidence| M[Request Additional Info -> 7-Day Window]
    K -->|Denied| N[Send Explanation with Policy Reference]
    L --> O[Close Ticket & Notify All Parties]
    M --> P{Response Received?}
    P -->|Yes| K
    P -->|No| N
```

---

### Flow 5.3: Analytics & Payout Oversight `[MVP]` *(New)*

```mermaid
flowchart TD
    A[Admin Opens Analytics Dashboard] --> B[View Revenue, Active Orders, Top Designs]
    B --> C[Navigate to 'Pending Payouts' Tab]
    C --> D[Review Queued Dealer Payouts - Flow 2.3]
    C --> E[Review Queued Designer Payouts - Flow 3.2]
    D & E --> F{Approve, Hold, or Flag for Dispute Check?}
    F -->|Approve| G[Batch Process Transfers]
    F -->|Hold| H[Add Note & Notify Recipient of Delay Reason]
    F -->|Flag| I[Route to Flow 5.2 Dispute Resolution]
```

---

## 🛑 Key Edge Cases & Error Recovery Pathways

| Scenario | Possible Trigger | System Resolution / User Path |
| :--- | :--- | :--- |
| **Payment Failed** | Bank server timeout / Invalid UPI PIN | Order stays in `Pending Payment` for 30 mins; automated recovery link sent via SMS/WhatsApp. |
| **Copyright Flagged** | Uploaded image contains Nike Swoosh | Instant modal feedback explaining trademark restriction with 1-click option to remove background/replace logo. |
| **Print Defect Claim** | Ink peeling post-washing | Customer submits 2 photos; Admin verifies & triggers 1-click free dealer reprint without return friction. |
| **Wrong Delivery OTP** | Customer typed wrong number | Logistics app allows 3 retries; fallback to digital photo proof + customer signature approval (Flow 4.3). |
| **Dealer Out of Stock** | Selected shirt size/color unavailable | System automatically re-routes order to 2nd nearest certified dealer with matching stock. |
| **Order Cancellation Mid-Production** | Customer cancels after dealer starts printing | Partial refund offered (material cost deducted) or cancellation denied if already packed (Flow 1.5). |
| **AI Generation Timeout** | Design or try-on API unresponsive | Show retry prompt; do not charge or lock the customer's session (Flow 1.2 / 1.3). |
| **Failed Delivery x3** | Customer unavailable across 3 attempts | Package auto-returns to dealer; refund minus return shipping initiated (Flow 4.2). |
| **Payout Below Threshold** | Dealer/Designer balance under ₹500 | Payout request blocked with balance-needed message; auto-processes once threshold met (Flow 2.3 / 3.2). |
| **Disputed Royalty** | Designer claims underpayment | Routed to Admin Dispute Resolution with sales ledger cross-check (Flow 5.2). |
| **Guest Checkout Follow-up** | Guest wants to track order later | Order lookup via email + Order ID, with prompt to convert to full account. |

---

## 🎯 Summary of Documentation Progress

- [x] **Requirements (`features.md`)** — Complete
- [x] **User Flows (`user-flow.md`)** — Updated & Complete (Auth, Cancellation, Payouts, Designer Onboarding, Bulk Orders, Multi-Dealer Split, Failed Delivery Recovery, Dispute Resolution, Reviews)
- [ ] **Design System (`design.md`)** — *Next Step*
- [ ] **Technical Architecture (`architecture.md`)**
- [ ] **Database Schema (`database.md`)**
- [ ] **API Specification (`api.md`)**
- [ ] **Development Roadmap (`roadmap.md`)**
