import { ethers } from 'ethers';

// Connect to an RPC provider (e.g., Polygon or Ethereum mainnet/testnet)
// In production, this URL should come from env variables.
const RPC_URL = process.env.RPC_URL || 'https://cloudflare-eth.com';
const provider = new ethers.JsonRpcProvider(RPC_URL);

// Contract address for USDC (Example: Ethereum Mainnet USDC)
const USDC_ADDRESS = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48';

// Minimal ERC-20 ABI to fetch balance
const ERC20_ABI = [
    "function balanceOf(address owner) view returns (uint256)",
    "function decimals() view returns (uint8)"
];

export class WalletService {
    /**
     * Generates a new cryptographically secure wallet.
     * @returns The wallet's public address, secure private key, and mnemonic phrase.
     */
    static generateWallet() {
        const wallet = ethers.Wallet.createRandom();
        return {
            address: wallet.address,
            privateKey: wallet.privateKey,
            mnemonic: wallet.mnemonic?.phrase
        };
    }

    /**
     * Connects to the Ethereum/EVM blockchain and fetches the live USDC balance for a given address.
     * @param address The public wallet address.
     * @returns Formatted USDC balance.
     */
    static async getUSDCBalance(address: string): Promise<string> {
        try {
            const contract = new ethers.Contract(USDC_ADDRESS, ERC20_ABI, provider);
            const rawBalance = await contract.balanceOf(address);
            const decimals = await contract.decimals();
            
            // Format the balance based on the exact token's decimals (e.g. USDC uses 6)
            return ethers.formatUnits(rawBalance, decimals);
        } catch (error) {
            console.error('Error fetching USDC balance:', error);
            throw new Error('Could not fetch wallet balance from the blockchain network');
        }
    }
}
