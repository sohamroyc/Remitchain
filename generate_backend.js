const fs = require('fs');
const path = require('path');

const rootDir = path.join('d:', 'Project', 'Remitchain', 'backend');

const dirs = [
    'src/config',
    'src/modules/auth',
    'src/modules/user',
    'src/modules/wallet',
    'src/modules/transaction',
    'src/modules/beneficiary',
    'src/modules/kyc',
    'src/modules/notification',
    'src/services',
    'src/jobs',
    'src/middleware',
    'src/utils',
    'prisma'
];

// Create directories
dirs.forEach(dir => {
    fs.mkdirSync(path.join(rootDir, dir), { recursive: true });
});

// Create files with content
const files = {
    'package.json': `{
  "name": "remitchain-backend",
  "version": "1.0.0",
  "description": "Production-ready backend system for RemitChain",
  "main": "src/server.ts",
  "scripts": {
    "start": "ts-node src/server.ts",
    "dev": "nodemon --exec ts-node src/server.ts",
    "build": "tsc",
    "prisma:generate": "prisma generate",
    "prisma:push": "prisma db push"
  },
  "dependencies": {
    "@prisma/client": "^5.x",
    "bullmq": "^4.x",
    "cors": "^2.x",
    "dotenv": "^16.x",
    "ethers": "^6.x",
    "express": "^4.x",
    "ioredis": "^5.x",
    "jsonwebtoken": "^9.x",
    "zod": "^3.x"
  },
  "devDependencies": {
    "@types/cors": "^2.x",
    "@types/express": "^4.x",
    "@types/jsonwebtoken": "^9.x",
    "@types/node": "^20.x",
    "nodemon": "^3.x",
    "prisma": "^5.x",
    "ts-node": "^10.x",
    "typescript": "^5.x"
  }
}`,

    'tsconfig.json': `{
  "compilerOptions": {
    "target": "es2020",
    "module": "commonjs",
    "lib": ["es2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/**/*"]
}`,

    '.env': `PORT=5000
DATABASE_URL="postgresql://postgres:password@localhost:5432/remitchain_db?schema=public"
REDIS_URL="redis://localhost:6379"
JWT_SECRET="super-secret-key"
TWILIO_API_KEY="mock-twilio-key"
MOONPAY_API_KEY="mock-moonpay-key"
`,

    'docker-compose.yml': `version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: remitchain_db
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
`,

    'prisma/schema.prisma': `generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String   @id @default(uuid())
  phone         String   @unique
  walletAddress String?
  kycStatus     String   @default("PENDING") // PENDING, VERIFIED, REJECTED
  transactions  Transaction[]
  beneficiaries Beneficiary[]
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model Transaction {
  id          String   @id @default(uuid())
  amount      Float
  status      String   @default("PENDING") // PENDING, ON_CHAIN, COMPLETED, FAILED
  txHash      String?
  recipient   String
  currency    String   @default("USDC")
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model Beneficiary {
  id          String   @id @default(uuid())
  name        String
  phone       String?
  bankDetails String?
  userId      String
  user        User     @relation(fields: [userId], references: [id])
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
`,

    'src/server.ts': `import app from './app';
import { env } from './config/env';

app.listen(env.PORT, () => {
  console.log(\`🚀 Server running on port \${env.PORT}\`);
});
`,

    'src/app.ts': `import express from 'express';
import cors from 'cors';
import authRoutes from './modules/auth/auth.routes';
import userRoutes from './modules/user/user.routes';
import walletRoutes from './modules/wallet/wallet.routes';
import transactionRoutes from './modules/transaction/transaction.routes';
import { errorHandler } from './middleware/errorHandler';

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/wallet', walletRoutes);
app.use('/api/transactions', transactionRoutes);

app.use(errorHandler);

export default app;
`,

    'src/config/env.ts': `import dotenv from 'dotenv';
dotenv.config();

export const env = {
  PORT: process.env.PORT || 5000,
  DATABASE_URL: process.env.DATABASE_URL,
  REDIS_URL: process.env.REDIS_URL,
  JWT_SECRET: process.env.JWT_SECRET || 'secret',
};
`,
    
    'src/config/redis.ts': `import { Redis } from 'ioredis';
import { env } from './env';

export const redis = new Redis(env.REDIS_URL || 'redis://localhost:6379');
`,

    'src/jobs/transactionQueue.ts': `import { Queue, Worker } from 'bullmq';
import { redis } from '../config/redis';

export const txQueue = new Queue('transactions', { connection: redis });

const worker = new Worker('transactions', async job => {
  console.log(\`Processing transaction: \${job.id}\`);
  // Validate transaction
  // Simulate fiat -> USDC
  // Broadcast TX
  // Update status DB
  return { status: 'COMPLETED', txHash: '0xmockhash' };
}, { connection: redis });

worker.on('completed', job => {
  console.log(\`Job \${job.id} completed!\`);
});
`,

    'src/middleware/auth.middleware.ts': `import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { env } from '../config/env';

export const protect = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'Unauthorized' });

  try {
    const decoded = jwt.verify(token, env.JWT_SECRET);
    (req as any).user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
`,

    'src/middleware/errorHandler.ts': `import { Request, Response, NextFunction } from 'express';

export const errorHandler = (err: any, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: err.message || 'Server Error' });
};
`,

    'src/modules/auth/auth.routes.ts': `import { Router } from 'express';
// import { sendOtp, verifyOtp } from './auth.controller';

const router = Router();
router.post('/send-otp', (req, res) => res.json({ msg: 'OTP sent (mock)' }));
router.post('/verify-otp', (req, res) => res.json({ token: 'mock-jwt-token' }));

export default router;
`,

    'src/modules/user/user.routes.ts': `import { Router } from 'express';
import { protect } from '../../middleware/auth.middleware';

const router = Router();
router.get('/me', protect, (req, res) => res.json({ msg: 'Current User' }));

export default router;
`,

    'src/modules/wallet/wallet.routes.ts': `import { Router } from 'express';
import { protect } from '../../middleware/auth.middleware';

const router = Router();
router.get('/balance', protect, (req, res) => res.json({ balance: 142580.00, currency: 'USDC' }));

export default router;
`,

    'src/modules/transaction/transaction.routes.ts': `import { Router } from 'express';
import { protect } from '../../middleware/auth.middleware';
import { txQueue } from '../../jobs/transactionQueue';

const router = Router();
router.post('/send', protect, async (req, res) => {
  await txQueue.add('tx', req.body);
  res.json({ msg: 'Transaction queued' });
});
router.get('/', protect, (req, res) => res.json([]));

export default router;
`
};

Object.keys(files).forEach(file => {
    fs.writeFileSync(path.join(rootDir, file), files[file]);
});

console.log('Backend scaffolded successfully in d:\\Project\\Remitchain\\backend !');
