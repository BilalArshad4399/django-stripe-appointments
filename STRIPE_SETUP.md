# Stripe Test Keys Setup

## For Evaluators

The Stripe test keys are provided in `.env.test` file. These are TEST keys that cannot process real payments.

## Setup Instructions

### Option 1: Manual Setup (Non-Docker)
```bash
cp .env.test .env
```

### Option 2: Docker Setup
1. Copy the keys from `.env.test`
2. Update `.env.docker` or set them as environment variables:
   ```bash
   export STRIPE_PUBLISHABLE_KEY=pk_test_YOUR_KEY
   export STRIPE_SECRET_KEY=sk_test_YOUR_KEY
   docker-compose up
   ```

### Option 3: Koyeb Deployment
Add these as environment variables in Koyeb dashboard:
- `STRIPE_PUBLISHABLE_KEY`: (copy from .env.test)
- `STRIPE_SECRET_KEY`: (copy from .env.test)

## Test Keys Information
- These are Stripe TEST mode keys
- They start with `pk_test_` and `sk_test_`
- No real payments can be processed
- Use test card: `4242 4242 4242 4242`

## Security Note
GitHub blocks Stripe keys (even test keys) for security. This is why they're in `.env.test` and not directly in Docker files.