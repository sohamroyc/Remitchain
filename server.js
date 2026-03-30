const express = require('express');
const path = require('path');
const cors = require('cors');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

// API Endpoints
// Example: Get user balance
app.get('/api/v1/balance', (req, res) => {
    res.json({
        success: true,
        data: {
            currency: "AED",
            available: 142580.00
        }
    });
});

// Example: Initiate transfer
app.post('/api/v1/transfer', (req, res) => {
    const { amount, recipient, currency } = req.body;
    
    // Simulate processing
    res.status(200).json({
        success: true,
        transactionId: "RC-9982736451",
        message: `Transfer of ${currency} ${amount} initiated to ${recipient}.`
    });
});

// Serve frontend files (RemitChain UI)
app.use(express.static(path.join(__dirname, 'public')));

// Fallback to index.html for undefined routes (Basic SPA behavior if needed)
app.use((req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Start the server
app.listen(PORT, () => {
    console.log(`\n======================================`);
    console.log(`RemitChain Backend Server Running!`);
    console.log(`- Frontend UI: http://localhost:${PORT}`);
    console.log(`- Base API:    http://localhost:${PORT}/api/v1`);
    console.log(`======================================\n`);
});
