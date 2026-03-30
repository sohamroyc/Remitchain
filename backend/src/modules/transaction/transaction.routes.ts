import { Router, Request, Response } from 'express';
import { protect } from '../../middleware/auth.middleware';
import { validate } from '../../middleware/validate.middleware';
import { sendTransactionSchema } from './transaction.schema';
import { txQueue } from '../../jobs/transactionQueue';

const router = Router();

// Zod validation strictly enforces positive floats and UUIDv4 format for recipients
router.post('/send', protect, validate(sendTransactionSchema), async (req: Request, res: Response) => {
  const { amount, recipientId, currency } = req.body;
  
  // Safely cast authenticated user from protect middleware
  const userId = (req as any).user.id; 

  console.log(`User ${userId} queuing ${amount} ${currency} to ${recipientId}`);

  // Send the robust transaction logic to BullMQ for asynchronous processing
  await txQueue.add('tx', { ...req.body, userId });
  
  res.status(202).json({ 
    success: true, 
    message: 'Transaction successfully queued for execution',
    status: 'PENDING'
  });
});

router.get('/', protect, (req, res) => res.json([]));

export default router;
