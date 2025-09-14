# Paddle Billing Integration Setup Guide

This guide walks you through setting up Paddle billing for the Trendit platform. The integration is fully implemented and ready to use - you just need to configure the environment variables and create products in Paddle.

## 🚀 Quick Start

The Paddle integration includes:
- ✅ **Complete backend service** (`backend/services/paddle_service.py`)
- ✅ **Full webhook handling** (`backend/api/webhooks.py`)
- ✅ **Billing API endpoints** (`backend/api/billing.py`)
- ✅ **Frontend billing UI** (`frontend/src/app/dashboard/billing/page.tsx`)
- ✅ **Database models** for subscriptions and usage tracking
- ✅ **TypeScript types** for all billing operations

## 📋 Prerequisites

1. **Paddle Account**: Sign up at https://paddle.com
2. **PostgreSQL Database**: For storing subscription and usage data
3. **Domain**: For webhook endpoints (can use ngrok for development)

## 🔧 Configuration Steps

### Step 1: Environment Variables

Add these to your `backend/.env` file:

```bash
# Paddle Billing Configuration
PADDLE_API_KEY=your_paddle_api_key_here
PADDLE_WEBHOOK_SECRET=your_webhook_secret_here
PADDLE_ENVIRONMENT=sandbox  # Change to 'production' for live

# Paddle Price IDs (create these in Paddle dashboard)
PADDLE_PRO_PRICE_ID=pri_01234567890abcdef
PADDLE_ENTERPRISE_PRICE_ID=pri_abcdef1234567890
```

### Step 2: Create Products in Paddle Dashboard

1. **Log into Paddle Dashboard**: https://sandbox-vendors.paddle.com (or production)

2. **Create Products**:

   **Pro Plan ($29/month)**:
   - Product Name: "Trendit Pro"
   - Price: $29.00 USD
   - Billing Interval: Monthly
   - Copy the Price ID to `PADDLE_PRO_PRICE_ID`

   **Enterprise Plan ($299/month)**:
   - Product Name: "Trendit Enterprise"
   - Price: $299.00 USD
   - Billing Interval: Monthly
   - Copy the Price ID to `PADDLE_ENTERPRISE_PRICE_ID`

### Step 3: Configure Webhooks

1. **In Paddle Dashboard**: Go to Developer Tools > Notifications

2. **Add Webhook Endpoint**:
   - URL: `https://yourdomain.com/api/webhooks/paddle`
   - Events to subscribe to:
     - `subscription.created`
     - `subscription.updated`
     - `subscription.canceled`
     - `subscription.resumed`
     - `subscription.paused`
     - `transaction.completed`
     - `transaction.payment_failed`
     - `customer.updated`
     - `subscription.trial_ended`

3. **Copy Webhook Secret**: Add to `PADDLE_WEBHOOK_SECRET` in your `.env`

### Step 4: Testing (Development)

For local development, use ngrok to expose your localhost:

```bash
# Install ngrok
npm install -g ngrok

# Start your backend server
cd backend && uvicorn main:app --reload --port 8000

# In another terminal, expose it
ngrok http 8000

# Use the ngrok URL for webhook endpoint
# Example: https://abc123.ngrok.io/api/webhooks/paddle
```

## 🧪 Testing the Integration

### Backend Health Check

```bash
curl -X GET "https://your-api-domain.com/api/billing/health"
```

Expected response:
```json
{
  "status": "healthy",
  "paddle_configured": true,
  "timestamp": "2025-01-13T..."
}
```

### Frontend Testing

1. **Navigate to**: `https://your-frontend-domain.com/dashboard/billing`

2. **Test Flow**:
   - View current subscription status
   - See usage percentages
   - Click "Upgrade to Pro" button
   - Should redirect to Paddle checkout

### API Testing

Create a test checkout session:

```bash
curl -X POST "https://your-api-domain.com/api/billing/checkout/create" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "tier": "pro",
    "success_url": "https://your-domain.com/billing/success",
    "cancel_url": "https://your-domain.com/billing/cancel"
  }'
```

## 📊 Subscription Tiers & Limits

The system is pre-configured with three tiers:

### Free Tier
- **Price**: $0/month
- **API Calls**: 500/month (increased from 100 for dashboard usage)
- **Exports**: 10/month
- **Sentiment Analysis**: 100/month
- **Data Retention**: 30 days

### Pro Tier ($29/month)
- **API Calls**: 10,000/month
- **Exports**: 100/month
- **Sentiment Analysis**: 2,000/month
- **Data Retention**: 365 days
- **Support**: Priority email

### Enterprise Tier ($299/month)
- **API Calls**: 100,000/month
- **Exports**: 1,000/month
- **Sentiment Analysis**: 20,000/month
- **Data Retention**: Unlimited
- **Support**: Phone & chat
- **Features**: Custom integrations, dedicated account manager

## 🔄 Webhook Event Handling

The system handles these Paddle events:

| Event | Action |
|-------|--------|
| `subscription.created` | Activate user subscription, set limits |
| `subscription.updated` | Update tier, billing period, limits |
| `subscription.canceled` | Downgrade to free tier |
| `subscription.resumed` | Reactivate subscription |
| `subscription.paused` | Suspend access |
| `transaction.completed` | Ensure subscription is active |
| `transaction.payment_failed` | Suspend subscription |
| `customer.updated` | Update customer portal URL |
| `subscription.trial_ended` | Clear trial status |

## 🔐 Security Features

- **Webhook Signature Verification**: Using Paddle's 2025 enhanced security
- **API Key Authentication**: Required for all billing operations
- **Usage Tracking**: Prevents overuse with real-time monitoring
- **Audit Logging**: All billing events stored in `billing_events` table

## 🗄️ Database Schema

The integration uses these tables:

- `paddle_subscriptions`: Core subscription data and limits
- `usage_records`: API usage tracking for billing periods
- `billing_events`: Audit log of all Paddle webhook events

## 🚦 Production Deployment

1. **Environment**: Change `PADDLE_ENVIRONMENT=production`
2. **API Keys**: Use production Paddle keys
3. **Webhook URL**: Point to production domain
4. **SSL**: Ensure HTTPS for webhook endpoints
5. **Monitoring**: Set up alerts for failed payments

## 🛠️ Customization

### Modify Subscription Limits

Edit the tier configuration in `backend/services/paddle_service.py:58`:

```python
self.tier_config = {
    SubscriptionTier.FREE: {
        "limits": {
            "api_calls_per_month": 500,  # Modify as needed
            # ...
        }
    }
    # ...
}
```

### Add New Subscription Tiers

1. Add enum to `backend/models/models.py:36`
2. Update `paddle_service.py` tier configuration
3. Create product in Paddle dashboard
4. Add price ID to environment variables
5. Update frontend billing page UI

### Custom Checkout Options

The checkout creation supports:
- **Trial Periods**: `trial_days` parameter
- **Custom URLs**: Success/cancel redirects
- **Discount Codes**: Via Paddle dashboard
- **Currency**: Currently USD, expandable

## ❓ Troubleshooting

### Common Issues

1. **"Billing service not configured"**
   - Check `PADDLE_API_KEY` is set
   - Verify price IDs are configured
   - Ensure `paddle_service.is_configured()` returns `true`

2. **Webhook signature verification fails**
   - Verify `PADDLE_WEBHOOK_SECRET` matches Paddle dashboard
   - Check webhook URL is accessible
   - Ensure HTTPS in production

3. **Checkout creation fails**
   - Verify Paddle price IDs exist
   - Check API key permissions
   - Confirm customer creation worked

### Debug Commands

```bash
# Check Paddle service configuration
python -c "from services.paddle_service import paddle_service; print(paddle_service.is_configured())"

# Test webhook signature verification
curl -X POST "https://your-api-domain.com/api/webhooks/paddle/status"
```

## 📞 Support

- **Paddle Documentation**: https://developer.paddle.com
- **Webhook Testing**: Use Paddle's webhook simulator
- **API Logs**: Check FastAPI logs for detailed error messages

---

**🎉 Your Paddle integration is ready to accept payments!**

The system will automatically:
- Track usage and enforce limits
- Handle subscription upgrades/downgrades
- Process webhooks and update user access
- Provide beautiful billing UI for customers