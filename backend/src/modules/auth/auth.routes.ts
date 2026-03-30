import { Router } from 'express';
import { validate } from '../../middleware/validate.middleware';
import { sendOtpSchema, verifyOtpSchema } from './auth.schema';
import jwt from 'jsonwebtoken';
import { PrismaClient } from '@prisma/client';
import { env } from '../../config/env';

const router = Router();
const prisma = new PrismaClient();

// Endpoint to send OTP, protected by Zod Regex phone validation
router.post('/send-otp', validate(sendOtpSchema), (req, res) => {
    // In production: Queue SMS via Twilio using req.body.phone
    res.json({ success: true, message: 'OTP successfully dispatched to ' + req.body.phone });
});

// Endpoint to verify OTP, protected by 4-digit requirement validation
router.post('/verify-otp', validate(verifyOtpSchema), async (req, res) => {
    const { phone } = req.body;
    
    // In production: check OTP against Redis...
    
    // Upsert User in DB
    const user = await prisma.user.upsert({
        where: { phone },
        update: {},
        create: { phone }
    });

    const token = jwt.sign({ id: user.id, phone: user.phone }, env.JWT_SECRET);

    res.json({ 
        success: true, 
        token,
        user: { id: user.id, phone: user.phone, kycStatus: user.kycStatus }
    });
});

export default router;
