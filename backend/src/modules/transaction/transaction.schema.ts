import { z } from 'zod';

export const sendTransactionSchema = z.object({
  body: z.object({
    amount: z.number().positive('Amount must be greater than zero'),
    recipientId: z.string().uuid('Invalid recipient ID format'),
    currency: z.enum(['USDC']).default('USDC'),
  }),
});
