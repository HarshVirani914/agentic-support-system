"""
Evaluation dataset for the RAG pipeline.

24 hand-written Q&A pairs (8 per category: order, shipping, general), with
`ground_truth` answers verified against the actual content of
`backend/data/sample_docs.txt` (not guessed). Each ground truth paraphrases
the relevant section of that file so RAGAS scores answers against what is
genuinely retrievable from the knowledge base.
"""

EVAL_CASES = [
    # --- order ---
    {
        "question": "What is your refund policy?",
        "category": "order",
        "ground_truth": (
            "Customers can request a full refund within 30 days of purchase for any "
            "reason, as long as items are in original condition with tags attached. "
            "Refunds are processed within 5-7 business days to the original payment "
            "method. Sale items are refunded as store credit only, and final sale "
            "'AS-IS' items and accessed digital products are not refundable."
        ),
    },
    {
        "question": "How do I cancel my order?",
        "category": "order",
        "ground_truth": (
            "Orders can be cancelled within 2 hours of placement if they haven't "
            "shipped yet, by going to Order History and clicking 'Cancel Order'. "
            "Expedited (Express/Overnight) and custom/personalized orders cannot be "
            "cancelled. Refunds for cancelled orders are processed within 3-5 "
            "business days."
        ),
    },
    {
        "question": "What is the process for returning an item?",
        "category": "order",
        "ground_truth": (
            "Returns must be initiated within 30 days of delivery. Items should be "
            "unused, unworn, and in original packaging with tags attached. "
            "Inspection takes 2-3 business days after we receive the return, and "
            "approved refunds are processed immediately. A $7.99 return shipping fee "
            "applies unless the item is defective, in which case we cover return "
            "shipping."
        ),
    },
    {
        "question": "Can I exchange an item for a different size?",
        "category": "order",
        "ground_truth": (
            "Yes, free exchanges for a different size or color are offered within 45 "
            "days of purchase. Request the exchange through your account and the new "
            "item ships immediately; return the original item using the provided "
            "label within 14 days of receiving the exchange. If the desired item is "
            "out of stock, store credit is issued instead."
        ),
    },
    {
        "question": "What payment methods do you accept?",
        "category": "order",
        "ground_truth": (
            "We accept Visa, Mastercard, American Express, Discover, PayPal, Apple "
            "Pay, Google Pay, and Shop Pay, plus Buy Now Pay Later through Klarna and "
            "Afterpay for orders over $50."
        ),
    },
    {
        "question": "Is my payment information secure?",
        "category": "order",
        "ground_truth": (
            "All transactions are secured with 256-bit SSL encryption, and we do not "
            "store your full credit card number, only the last 4 digits for order "
            "reference."
        ),
    },
    {
        "question": "How do I apply a promotional or discount code?",
        "category": "order",
        "ground_truth": (
            "Promotional codes can be applied at checkout. Only one promo code can be "
            "used per order, and codes cannot be combined with other offers unless "
            "explicitly stated."
        ),
    },
    {
        "question": "What are the benefits of a business account?",
        "category": "order",
        "ground_truth": (
            "Business accounts get Net 30 payment terms after credit approval, "
            "multiple user access with different permission levels, purchase order "
            "support, detailed invoice history, a dedicated account manager, and "
            "volume discount pricing. Approval typically takes 1-2 business days."
        ),
    },
    # --- shipping ---
    {
        "question": "How long does standard shipping take?",
        "category": "shipping",
        "ground_truth": (
            "Standard shipping typically takes 3-5 business days within the "
            "continental US, and is free on orders over $50."
        ),
    },
    {
        "question": "Do you offer expedited or overnight shipping?",
        "category": "shipping",
        "ground_truth": (
            "Express shipping (1-2 days) is available for an additional $15, and "
            "overnight shipping is available for $25 in select metro areas."
        ),
    },
    {
        "question": "Do you offer international shipping?",
        "category": "shipping",
        "ground_truth": (
            "International shipping is available to over 100 countries and takes "
            "7-14 business days via DHL Express. International customers are "
            "responsible for any customs fees, import duties, or taxes."
        ),
    },
    {
        "question": "How can I track my order?",
        "category": "shipping",
        "ground_truth": (
            "You can track your order by logging into your account and viewing "
            "Order History, which shows real-time status updates: Order Confirmed, "
            "Processing, Shipped, Out for Delivery, and Delivered. A tracking number "
            "is also emailed once the order ships."
        ),
    },
    {
        "question": "What happens if my package is lost in transit?",
        "category": "shipping",
        "ground_truth": (
            "If a package is lost in transit, contact support within 7 days of the "
            "expected delivery date. We'll file a claim with the carrier and either "
            "reship the order or issue a full refund."
        ),
    },
    {
        "question": "What should I do if I receive a damaged item?",
        "category": "shipping",
        "ground_truth": (
            "Take photos of the packaging and product damage, and contact support "
            "within 48 hours of delivery. We'll arrange a replacement or full refund "
            "without requiring the damaged item to be returned."
        ),
    },
    {
        "question": "Are my shipments insured?",
        "category": "shipping",
        "ground_truth": (
            "All shipments over $100 are automatically insured. High-value orders "
            "require signature confirmation to prevent theft."
        ),
    },
    {
        "question": "What should I do if my tracking shows no movement for several days?",
        "category": "shipping",
        "ground_truth": (
            "If tracking shows no movement for 3+ days, contact support immediately "
            "so we can investigate with the carrier and provide updates within 24 "
            "hours."
        ),
    },
    # --- general ---
    {
        "question": "How do I reset my password?",
        "category": "general",
        "ground_truth": (
            "Use the 'Reset Password' link on the login page. You'll receive a "
            "password reset email within 5 minutes, and the reset link expires after "
            "1 hour for security."
        ),
    },
    {
        "question": "How do I delete my account?",
        "category": "general",
        "ground_truth": (
            "Contact customer support to delete your account. This will permanently "
            "remove all order history, saved addresses, payment methods, and "
            "preferences, though active orders will still be fulfilled."
        ),
    },
    {
        "question": "How do I contact customer support?",
        "category": "general",
        "ground_truth": (
            "Support is available Monday-Friday, 9 AM - 6 PM EST via email "
            "(support@example.com, 24-hour response), phone (1-800-EXAMPLE), live "
            "chat on the website, or SMS by texting 'HELP' to 55555. Urgent issues "
            "outside business hours can be emailed to urgent@example.com."
        ),
    },
    {
        "question": "What is your product warranty policy?",
        "category": "general",
        "ground_truth": (
            "Electronics come with a 1-year manufacturer warranty covering defects "
            "in materials and workmanship, but not damage from misuse, accidents, "
            "normal wear, or unauthorized repairs. Extended warranties (2-year and "
            "3-year plans) are available at checkout and cover accidental damage."
        ),
    },
    {
        "question": "Do you offer a subscription service?",
        "category": "general",
        "ground_truth": (
            "Yes, you can subscribe to receive products automatically every 30, 60, "
            "or 90 days. Subscribers save 15% on every order and get free shipping "
            "regardless of order size, and can skip, pause, or cancel anytime."
        ),
    },
    {
        "question": "What do I get with the VIP membership program?",
        "category": "general",
        "ground_truth": (
            "The VIP membership costs $99/year and includes free 2-day shipping on "
            "all orders, 20% off every purchase, exclusive access to new products, "
            "early access to sales, a birthday gift, and a dedicated VIP support "
            "line, with no minimum purchase required."
        ),
    },
    {
        "question": "Do gift cards expire?",
        "category": "general",
        "ground_truth": (
            "No, gift cards never expire and can be combined with promotional codes. "
            "They are available in denominations of $25, $50, $100, and $200, and "
            "digital gift cards are delivered instantly via email."
        ),
    },
    {
        "question": "How can I make my account more secure?",
        "category": "general",
        "ground_truth": (
            "You can enable two-factor authentication (2FA) in your account "
            "settings, which sends a verification code to your phone each time you "
            "log in from a new device."
        ),
    },
]
