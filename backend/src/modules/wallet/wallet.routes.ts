import { Router } from 'express';
import { protect } from '../../middleware/auth.middleware';

const router = Router();
router.get('/balance', protect, (req, res) => res.json({ balance: 142580.00, currency: 'USDC' }));

export default router;
