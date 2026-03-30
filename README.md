# 🏦 RemitChain | Modern Private Banking & Remittance Platform

RemitChain is a high-performance, full-stack digital private banking platform designed for secure global remittances and institutional-grade financial management. It provides a stunning, premium user experience combined with a robust, scalable backend architecture.

---

## ✨ Key Features

- **🔐 Secure Authentication**: Multi-step phone-based identity verification with JWT session management.
- **📊 Institutional Dashboard**: Real-time balance monitoring (AED/INR) and integrated transaction ledger.
- **💸 Global Remittances**: Multi-step transfer flow with support for saved beneficiaries and instant currency settlements.
- **👥 Beneficiary Management**: Full CRUD interface for managing international recipients, bank accounts, and UPI IDs.
- **📄 Ledger Overview**: Grouped transaction history with advanced filtering and status tracking.
- **🏛️ Multi-Asset Support**: Engineered for AED-backed digital assets (USDC) with zero-fee settlements.

---

## 🛠️ Technology Stack

### **Frontend**
- **Architecture**: Single Page Application flow (using Vanilla HTML5/JS).
- **Styling**: TailwindCSS with a custom "Digital Private Bank" design system.
- **Components**: Material Symbols for iconography, Google Fonts for typography (Manrope/Inter).

### **Backend**
- **Runtime**: Node.js with TypeScript.
- **Framework**: Express.js 5.x (modularized architecture).
- **ORM**: Prisma (Postgres connection).
- **Queue System**: BullMQ for asynchronous transaction processing.
- **Data Validation**: Zod (strictly enforced schemas).
- **Authentication**: JsonWebToken (JWT).

### **Infrastructure**
- **Database**: PostgreSQL 15 (Dockerized).
- **Cache/Queue Store**: Redis 7 (Dockerized).

---

## 🚀 Getting Started

### **Prerequisites**
- [Node.js](https://nodejs.org/) (v18+)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Remitchain
   ```

2. **Setup Infrastructure (Docker)**:
   ```bash
   docker-compose up -d
   ```

3. **Install Dependencies**:
   ```bash
   # Root (Frontend server)
   npm install

   # Backend
   cd backend
   npm install
   ```

4. **Initialize Database**:
   ```bash
   npx prisma generate
   npx prisma db push
   ```

5. **Start the Application**:
   ```bash
   # Run from root (Two terminals)
   npm start          # Frontend on http://localhost:3000
   cd backend && npm run dev  # Backend on http://localhost:5000
   ```

---

## ⚙️ Environment Variables

Create a `.env` file in the `backend/` directory:

```env
PORT=5000
DATABASE_URL="postgresql://postgres:password@localhost:5432/remitchain_db?schema=public"
REDIS_URL="redis://localhost:6379"
JWT_SECRET="your-very-secure-secret-key"
```

---

## 🛡️ Security Architecture

- **Protected API**: All sensitive endpoints (`/api/wallet`, `/api/transactions`, `/api/beneficiaries`) require a valid Bearer Token.
- **Async Processing**: Financial transactions are decoupled from the request cycle using `BullMQ` to ensure high availability and prevent race conditions.
- **Type Safety**: End-to-end type safety from the DB level (Prisma) to the API layer (TypeScript/Zod).

---

## 🗺️ Roadmap

- [ ] **Multi-Currency Wallets**: Native support for EUR, GBP, and USD.
- [ ] **KYC Integration**: Automated identity verification flow.
- [ ] **Smart Contracts**: On-chain settlement for real-time liquidity.
- [ ] **Mobile App**: Native iOS/Android experience via React Native.

---

## 📄 License
MIT License. Created by [Antigravity](https://github.com/google-deepmind).
