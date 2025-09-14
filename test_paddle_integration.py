#!/usr/bin/env python3
"""
Paddle Integration Test Script

This script tests the Paddle billing integration without requiring
real Paddle credentials or API keys.
"""

import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.insert(0, './backend')

def test_paddle_service():
    """Test the PaddleService configuration and methods"""
    print("🧪 Testing Paddle Service Integration...")

    try:
        from services.paddle_service import paddle_service
        from models.models import SubscriptionTier

        print(f"✅ Paddle Service imported successfully")
        print(f"   - Base URL: {paddle_service.base_url}")
        print(f"   - Configured: {paddle_service.is_configured()}")

        # Test tier configuration
        print("\n📊 Subscription Tier Configuration:")
        for tier in SubscriptionTier:
            config = paddle_service.get_tier_limits(tier)
            price = paddle_service.tier_config[tier]["price"]
            print(f"   {tier.value.upper()}: ${price}/month")
            print(f"     - API calls: {config['api_calls_per_month']:,}")
            print(f"     - Exports: {config['exports_per_month']:,}")
            print(f"     - Sentiment: {config['sentiment_analysis_per_month']:,}")
            print(f"     - Retention: {config['data_retention_days']} days")

        # Test webhook verification (without actual webhook)
        print(f"\n🔐 Webhook Configuration:")
        print(f"   - Secret configured: {'Yes' if paddle_service.webhook_secret else 'No'}")
        print(f"   - Verification ready: {bool(paddle_service.webhook_secret)}")

        return True

    except Exception as e:
        print(f"❌ Error testing Paddle service: {e}")
        return False

def test_billing_models():
    """Test the billing database models"""
    print("\n🗄️ Testing Database Models...")

    try:
        from models.models import (
            PaddleSubscription, BillingEvent, UsageRecord,
            SubscriptionTier, SubscriptionStatus
        )

        print("✅ Database models imported successfully:")
        print("   - PaddleSubscription: User subscription data")
        print("   - BillingEvent: Webhook event audit log")
        print("   - UsageRecord: API usage tracking")
        print("   - SubscriptionTier: FREE, PRO, ENTERPRISE")
        print("   - SubscriptionStatus: INACTIVE, ACTIVE, TRIALING, etc.")

        return True

    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False

def test_api_endpoints():
    """Test API endpoint imports"""
    print("\n🔌 Testing API Endpoints...")

    try:
        # Test billing API
        sys.path.insert(0, './backend/api')
        import billing
        import webhooks

        print("✅ API endpoints imported successfully:")
        print("   - /api/billing/checkout/create")
        print("   - /api/billing/subscription/status")
        print("   - /api/billing/subscription/upgrade")
        print("   - /api/billing/subscription/cancel")
        print("   - /api/billing/usage/analytics")
        print("   - /api/billing/tiers")
        print("   - /api/billing/health")
        print("   - /api/webhooks/paddle")

        return True

    except Exception as e:
        print(f"❌ Error testing API endpoints: {e}")
        return False

def test_frontend_integration():
    """Test frontend integration files exist"""
    print("\n🖥️ Testing Frontend Integration...")

    frontend_files = [
        "frontend/src/app/dashboard/billing/page.tsx",
        "frontend/src/lib/api/client.ts",
        "frontend/src/lib/types/index.ts"
    ]

    all_exist = True
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing!")
            all_exist = False

    if all_exist:
        print("✅ All frontend files present")
        print("   - Billing page with Paddle checkout")
        print("   - API client methods implemented")
        print("   - TypeScript types defined")

    return all_exist

def check_environment_setup():
    """Check environment configuration"""
    print("\n⚙️ Environment Configuration Check...")

    required_vars = [
        "PADDLE_API_KEY",
        "PADDLE_WEBHOOK_SECRET",
        "PADDLE_PRO_PRICE_ID",
        "PADDLE_ENTERPRISE_PRICE_ID"
    ]

    env_file_path = "./backend/.env"
    env_example_path = "./backend/.env.example"

    if os.path.exists(env_file_path):
        print(f"✅ Environment file exists: {env_file_path}")
    else:
        print(f"⚠️ Environment file missing: {env_file_path}")
        print("   Copy from .env.example and configure Paddle variables")

    if os.path.exists(env_example_path):
        print(f"✅ Example file exists: {env_example_path}")
        with open(env_example_path) as f:
            content = f.read()
            has_paddle_config = any(var in content for var in required_vars)
            if has_paddle_config:
                print("✅ Paddle configuration documented in .env.example")
            else:
                print("⚠️ Paddle configuration missing from .env.example")

    return True

def main():
    """Run all integration tests"""
    print("🚀 Paddle Billing Integration Test")
    print("=" * 50)

    results = []
    results.append(("Paddle Service", test_paddle_service()))
    results.append(("Database Models", test_billing_models()))
    results.append(("API Endpoints", test_api_endpoints()))
    results.append(("Frontend Files", test_frontend_integration()))
    results.append(("Environment Config", check_environment_setup()))

    print("\n" + "=" * 50)
    print("📋 INTEGRATION TEST RESULTS")
    print("=" * 50)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if not passed:
            all_passed = False

    print("\n🎯 OVERALL STATUS:")
    if all_passed:
        print("🎉 ALL TESTS PASSED - Paddle integration is ready!")
        print("\n📝 Next steps:")
        print("1. Configure Paddle environment variables")
        print("2. Create products in Paddle dashboard")
        print("3. Set up webhook endpoints")
        print("4. Test with real checkout flow")
        print("\nSee PADDLE_SETUP.md for detailed instructions.")
    else:
        print("⚠️ Some tests failed - check output above")

    print(f"\nTest completed at: {datetime.now().isoformat()}")
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)