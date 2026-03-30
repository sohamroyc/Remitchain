import { Router, Request, Response } from 'express';
import { protect } from '../../middleware/auth.middleware';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

// Get all beneficiaries for the authenticated user
router.get('/', protect, async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  try {
    const beneficiaries = await prisma.beneficiary.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' }
    });
    res.json(beneficiaries);
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to fetch beneficiaries' });
  }
});

// Add a new beneficiary
router.post('/', protect, async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  const { name, phone, bankDetails } = req.body;
  try {
    const beneficiary = await prisma.beneficiary.create({
      data: {
        name,
        phone,
        bankDetails,
        userId
      }
    });
    res.json(beneficiary);
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to create beneficiary' });
  }
});

router.delete('/:id', protect, async (req: Request, res: Response) => {
  const userId = (req as any).user.id;
  try {
    await prisma.beneficiary.deleteMany({
      where: { id: req.params.id, userId }
    });
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Failed to delete' });
  }
});

export default router;
