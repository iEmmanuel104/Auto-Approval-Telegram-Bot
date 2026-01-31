# Trading Bot Funnel Template

## Overview
This document explains how the automated trading bot funnel works to convert leads into verified users through a systematic onboarding process.

## Funnel Architecture

### Stage 1: Entry Point
**Trigger:** User joins Telegram channel OR sends message to bot
**Action:** Auto-approve join request + Start onboarding sequence

### Stage 2: Welcome Sequence
**Message 1 - Welcome Message (Immediate)**
- Personalized greeting using {first_name}
- Value proposition (90% win accuracy, FREE access)
- Scarcity/urgency messaging
- Clear CTA: Click /start

**Message 2 - Immediate Follow-up (2 seconds after welcome)**
- Reinforcement message
- Urgency reminder
- Simple CTA: Click /start

### Stage 3: Setup Instructions
**Trigger:** User clicks /start
**Messages Sent:**

**Setup Instructions Message:**
- Confirmation of entry
- Trading account requirement explanation
- Link to step-by-step deposit guide
- Minimum deposit requirement ($20-30)
- Link to results channel for social proof

**Support Message (immediately after):**
- Instructions to send proof to support team
- Support username provided
- Verification process explanation
- One-time setup messaging

### Stage 4: Follow-up Sequences

**1-Hour Follow-up**
- Timing: 60 minutes after onboarding starts (configurable)
- Check-in message asking about account status
- Interactive buttons: "Yes, I have" / "No, not yet"
- WhatsApp link integration (if configured)

**3-Hour Follow-up**
- Timing: 180 minutes after onboarding starts (configurable)
- Final check-in with urgency
- Direct contact username for help
- Reminder of value proposition
- Link to setup guide

### Stage 5: Response Handling

**If User Clicks "Yes, I have" (Setup Complete):**
- Congratulations message
- Confirmation of access
- Instructions to follow bot signals

**If User Clicks "No, not yet" (Needs Help):**
- Helpful reminder message
- Setup guide link with promo code
- Support contact information
- Encouragement to complete setup

## Configuration Variables

### Bot Information
- `bot_name`: Your bot's display name
- `support_username`: Telegram username for support
- `direct_contact_username`: Personal contact for escalations
- `promo_code`: Registration bonus code

### Links
- `deposit_guide_link`: Step-by-step account setup guide
- `results_channel_link`: Social proof/results channel
- `channel_url`: Main trading channel
- `support_url`: Support team contact

### Timing Controls
- `follow_up_1_minutes`: Minutes until first follow-up (default: 60)
- `follow_up_3_minutes`: Minutes until second follow-up (default: 180)

## Message Templates

### Variables Available
- `{first_name}` - User's first name
- `{bot_name}` - Your bot name
- `{deposit_guide_link}` - Setup guide URL
- `{results_channel_link}` - Results channel URL
- `{support_username}` - Support team username
- `{direct_contact_username}` - Direct contact username
- `{promo_code}` - Bonus code
- `{whatsapp_link}` - WhatsApp contact (if configured)

### Sample Messages

**Welcome Message:**
```
Welcome, {first_name}!

This is the exact system that changed my life entirely as well as thousands of others....same system I used to charge over $1k for — and now, I'm giving it to you for FREE.

automatic signal delivery straight from my private bot with over 90% WIN Accuracy

This opportunity won't stay FREE forever. Once access closes, IT'S DONE.

Click 👉 /start now to get FREE ACCESS IMMEDIATELY
```

**Setup Instructions:**
```
🔥 You made it in, {first_name}!

Let's plug you into the system properly:

You know you need a Trading account to Access my Bot right?? You need to be ready

Creating your trading account isn't hard, but I have provided you a detailed step by Step Guide to achieve that below 👇

{deposit_guide_link}

Only serious ones get access, so a minimum of $20 deposit on your personal trading would grant you FREE Access

Infact, you can join my public telegram I opened recently where I share RESULTS 👇

{results_channel_link}
```

**1-Hour Follow-up:**
```
Hey 👋

Just checking in — have you created your account and sent proof to support yet?

✅ Yes, I have
❌ No, not yet
```

**3-Hour Follow-up:**
```
Hey again, {first_name}!

Just checking one last time.

If you got stuck or have questions, reach out to me directly here @{direct_contact_username}

Let's not waste time — this bot is literally printing results every day.

You either plug in or watch others eat.

You need the Step by step guide to setting up your account? Here 👇

{deposit_guide_link}
```

## Technical Implementation

### Database Tracking
The bot tracks each user's progress through:
- User ID and name
- Onboarding stage
- Follow-up messages sent
- Setup completion status
- Account verification status

### Automation Features
- Auto-approval of channel join requests
- Automatic message scheduling
- Stage-based progression tracking
- Rate limiting to prevent spam
- Error handling for blocked users

### Admin Controls
- `/resetonboarding [user_id]` - Reset user's funnel progress
- `/test` - Test message functionality
- `/users` - View user statistics
- `/bcast` - Broadcast to all users
- `/fcast` - Forward message to all users

## Best Practices

1. **Timing is Critical**
   - Keep initial messages close together (build momentum)
   - Space follow-ups appropriately (60min, 180min)
   - Don't overwhelm with too many messages

2. **Personalization**
   - Always use first name in messages
   - Reference specific benefits/results
   - Make CTAs clear and simple

3. **Social Proof**
   - Link to results channel early
   - Show success stories
   - Build trust through transparency

4. **Support Integration**
   - Make support easily accessible
   - Provide clear verification instructions
   - Have backup contact methods

5. **Testing**
   - Test full funnel flow regularly
   - Monitor completion rates
   - Adjust timing based on data

## Metrics to Track

- Join request to /start conversion rate
- /start to setup completion rate
- Time to completion average
- Drop-off points in funnel
- Response rates to follow-ups

## Customization Guide

To adapt this funnel for your trading bot:

1. Update all bot configuration in `config.json`
2. Customize message content while maintaining structure
3. Adjust timing based on your audience
4. Set appropriate minimum deposit amounts
5. Ensure all links are working
6. Test complete flow before launch

## Support Setup

Ensure your support team knows:
- How to verify deposits
- Bot activation process
- Common user questions
- Escalation procedures
- Response time expectations

---

This template provides a complete framework for implementing an automated trading bot funnel that guides users from initial interest to verified account setup.