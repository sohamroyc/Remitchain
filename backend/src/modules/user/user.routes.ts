import { Router, Request, Response } from 'express';
import { protect } from '../../middleware/auth.middleware';
import { PrismaClient } from '@prisma/client';

const router = Router();
const prisma = new PrismaClient();

router.get('/me', protect, async (req: Request, res: Response) => {
    const userId = (req as any).user.id;
    try {
        const user = await prisma.user.findUnique({
            where: { id: userId }
        });
        res.json(user);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch user' });
    }
});

export default router;
