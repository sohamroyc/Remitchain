import { z } from 'zod';

export const sendOtpSchema = z.object({
  body: z.object({
    phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid international phone number format'),
  }),
});

export const verifyOtpSchema = z.object({
  body: z.object({
    phone: z.string().regex(/^\+?[1-9]\d{1,14}$/, 'Invalid international phone number format'),
    otp: z.string().length(4, 'OTP must be exactly 4 digits').regex(/^\d+$/, 'OTP must strictly contain numbers'),
  }),
});
