# Onda Agency: Business Playbook (Operations Manual)

This document outlines the exact step-by-step process for running your AI Agency, from finding a client to handing over the keys.

---

## Phase 1: Finding Clients (Lead Gen)

### 1. Who is your target?
*   **Niche**: Small businesses with high customer service volume but low tech (e.g., Real Estate Agents, Dentists, Law Firms, E-commerce stores doing <€50k/mo).
*   **Pain Point**: "I spend too much time answering the same questions" or "I miss leads because I don't reply fast enough."

### 2. Outreach Strategy
*   **The "Vibe" Audit (Cold Email/DM)**:
    *   Don't sell "AI". Sell "Time".
    *   *Script*: "Hola [Name], I saw your website and noticed you don't have an auto-responder for leads. I built a quick demo of how an AI agent could handle your FAQs instantly. Want to see it? It takes 30 seconds."
*   **The "Demo" Trap**:
    *   Use your `demos.html` page. Show them the **Lead Qualifier**.
    *   Say: "Imagine this running on your site 24/7 while you sleep."

---

## Phase 2: The Sale

### 1. The Discovery Call (15 mins)
*   **Goal**: Find the "Bleeding Neck" (the urgent problem).
*   **Ask**:
    *   "How many hours a week do you spend on email?"
    *   "What happens if a lead contacts you at 2 AM?"
    *   "If I could automate 80% of that, what would you pay?"

### 2. The Proposal
*   **Keep it Simple**: Offer the **Starter** or **Growth** package.
*   **Terms**: 50% Deposit upfront, 50% on delivery. **Never start work without a deposit.**

---

## Phase 3: Fulfillment (Building & Delivering)

This is the technical part. How do you actually give them the product?

### 1. The Website (If they bought a site)
*   **Development**: You clone your existing code (the one we built). Change the text, images, and colors to match their brand.
*   **Hosting**:
    *   Create a free account on **Netlify** or **Vercel**.
    *   Drag and drop the folder containing `index.html`.
    *   Connect their domain (e.g., `client-name.com`).
    *   *Cost to you*: €0/mo.

### 2. The AI Agent (The Bot)
*   **The "Brain"**: You need to host the Python script (`backend/rag_chat.py`).
    *   **Platform**: Use **Railway.app** or **Render.com** (easiest for Python).
    *   **Setup**: Upload the Python code. Set the environment variables (OPENAI_API_KEY).
*   **The "Body" (Chat Widget)**:
    *   You need a frontend chat widget to put on their site.
    *   *Option A (Custom)*: Use the code from `demos.html` and embed it as a widget.
    *   *Option B (SaaS)*: Connect their OpenAI Assistant to a tool like **Voiceflow** or **Botpress** (easier to manage, no coding required for you).
    *   *Recommendation*: For "Starter" clients, use **Voiceflow**. It's drag-and-drop, and you just paste a Javascript snippet onto their site.

### 3. The "Handover"
*   **Training**: Record a 5-minute Loom video showing them how to log in (if applicable) or how to test the bot.
*   **Payment**: Collect the final 50%.

---

## Phase 4: Support & Retention

### 1. The "Retainer" (Recurring Revenue)
*   **The Pitch**: "AI models update every month. For €99/mo, I will ensure your bot stays online, update its knowledge base with new company info, and send you a monthly report of leads captured."
*   **Why they buy**: They don't want to touch the tech. They pay for peace of mind.

### 2. Handling Bugs
*   If the bot hallucinates (lies), you tweak the "System Prompt" (the instructions).
*   If the site goes down, you check Netlify.

---

## Summary Checklist for Your First Client

1.  [ ] **Find**: Send 10 "Vibe Audit" emails to local businesses.
2.  [ ] **Close**: Get one "Yes" and a 50% deposit (€475 for Starter).
3.  [ ] **Build**: Clone your repo, customize it, deploy to Netlify.
4.  [ ] **Agent**: Set up a simple Voiceflow agent or deploy your Python script.
5.  [ ] **Launch**: Go live, collect the rest of the money.
