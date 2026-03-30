import { Queue, Worker } from 'bullmq';
import { redis } from '../config/redis';

export const txQueue = new Queue('transactions', { connection: redis });

const worker = new Worker('transactions', async job => {
  console.log(`Processing transaction: ${job.id}`);
  // Validate transaction
  // Simulate fiat -> USDC
  // Broadcast TX
  // Update status DB
  return { status: 'COMPLETED', txHash: '0xmockhash' };
}, { connection: redis });

worker.on('completed', job => {
  console.log(`Job ${job.id} completed!`);
});
