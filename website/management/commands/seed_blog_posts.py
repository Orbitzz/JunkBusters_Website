"""
Seed 3 SEO-targeted blog posts. Run once: python manage.py seed_blog_posts
Skips any post whose slug already exists.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta


POSTS = [
    # ── Post 1 ───────────────────────────────────────────────────────────────
    {
        "title": "Hoarder House Cleanout in Nashville: Costs, Timeline & What to Expect",
        "slug": "hoarder-house-cleanout-nashville-guide",
        "excerpt": (
            "Cleaning out a hoarding situation is nothing like a standard junk removal job. "
            "Here's what Nashville homeowners, property managers, and families need to know "
            "about costs, timelines, and how to choose the right crew."
        ),
        "published": timezone.now() - timedelta(days=2),
        "body": """
<p>A hoarding cleanout is one of the most physically and emotionally demanding jobs in the junk removal business. Standard crews aren't equipped for it. The right crew changes everything.</p>

<p>If you're in Nashville, Clarksville, or Bowling Green and facing a home packed floor-to-ceiling, here's exactly what to expect — the costs, the timeline, and how to choose a company that won't make the situation worse.</p>

<h2>What Makes a Hoarder Cleanout Different</h2>

<p>A typical junk removal job takes 1–2 hours. A hoarding cleanout can take 1–5 full days depending on the size of the home and how many years the accumulation has been building. The challenges are different:</p>

<ul>
  <li><strong>Volume</strong> — entire rooms may be inaccessible</li>
  <li><strong>Sensitivity</strong> — items with sentimental value are mixed in with actual trash</li>
  <li><strong>Hazards</strong> — mold, pest infestations, biohazardous materials, and structural instability are common</li>
  <li><strong>Sorting</strong> — the homeowner or family often needs to be present to make keep/discard decisions</li>
</ul>

<p>A good crew respects this process. We've worked jobs where a client broke down crying over a box of photographs buried under years of magazines — and we stopped, set it aside, and made sure those photos made it home. That's not in the contract. It's just right.</p>

<h2>How Much Does a Hoarder House Cleanout Cost in Nashville?</h2>

<p>Pricing varies significantly based on:</p>

<ul>
  <li>Square footage of the home</li>
  <li>How many rooms are affected</li>
  <li>Whether hazardous materials (mold, waste, sharps) are present</li>
  <li>How many truckloads of debris need to be hauled</li>
</ul>

<p>As a general range for the Nashville metro:</p>

<table style="width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;">
  <thead>
    <tr style="background:#f1f5f9;text-align:left;">
      <th style="padding:10px 14px;border:1px solid #e2e8f0;">Situation</th>
      <th style="padding:10px 14px;border:1px solid #e2e8f0;">Estimated Range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">Single room or garage</td>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">$300 – $700</td>
    </tr>
    <tr style="background:#f8fafc;">
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">Small home (2 BR) partial hoarding</td>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">$800 – $1,800</td>
    </tr>
    <tr>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">Full home cleanout, moderate hoarding</td>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">$2,000 – $4,500</td>
    </tr>
    <tr style="background:#f8fafc;">
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">Severe hoarding, large home</td>
      <td style="padding:10px 14px;border:1px solid #e2e8f0;">$4,500 – $9,000+</td>
    </tr>
  </tbody>
</table>

<p>These are not firm quotes — every situation is different. We always offer a <a href="/quote/">free on-site estimate</a> before any work begins so there are no surprises on invoice day.</p>

<h2>The Cleanout Process: Step by Step</h2>

<h3>1. Initial Walk-Through</h3>
<p>We assess the home room by room before quoting. This lets us estimate crew size, number of trucks, and any special equipment needed. We identify any hazardous materials that require separate handling.</p>

<h3>2. Sort and Stage</h3>
<p>Working systematically through the home, we create three categories: keep, donate, discard. The homeowner or a designated family member is involved in this step as much or as little as they want to be.</p>

<h3>3. Load and Haul</h3>
<p>We load trucks continuously throughout the job. Depending on volume, we may need to make multiple dump runs. We recycle and donate everything possible — mattresses, furniture, clothing, and electronics all have a second life before they hit the landfill.</p>

<h3>4. Final Sweep and Broom-Clean</h3>
<p>Once the debris is out, we do a final sweep. For full cleanouts, we can leave the home broom-clean and ready for the next step — whether that's a deep clean, repairs, or listing.</p>

<h2>When to Call in a Professional (Not a DIY Dumpster)</h2>

<p>Some families try to handle hoarding cleanouts themselves or rent a dumpster. This works for mild situations. But when any of the following are present, professional help is the right call:</p>

<ul>
  <li>There are signs of mold, rodents, or pest infestation</li>
  <li>The primary occupant is elderly, disabled, or recently deceased</li>
  <li>The home is heading to estate sale, foreclosure, or eviction</li>
  <li>There are more than 3 rooms affected</li>
  <li>Family members are emotionally unable to sort through items themselves</li>
</ul>

<p>We work closely with property managers and real estate agents across Nashville, Clarksville, and Bowling Green who call us when a property needs to be turned around fast. We also work directly with families navigating the difficult process of <a href="/estate-clean-out/">estate cleanouts</a> after a loved one passes.</p>

<h2>Frequently Asked Questions</h2>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">How long does a hoarder house cleanout take?</summary>
  <p style="margin-top:10px;margin-bottom:0;">For a single room, expect 2–4 hours. A full home with severe hoarding can take 2–4 full days with a crew of 3–4. We can give you a realistic timeline after our initial walk-through.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do you handle biohazardous materials?</summary>
  <p style="margin-top:10px;margin-bottom:0;">We handle general waste including spoiled food, rotted materials, and typical household hazards. For situations involving human waste, blood, or sharps, we partner with licensed biohazard remediation companies and can refer you directly.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Will you donate or recycle what you haul?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Yes. We donate usable furniture, clothing, and household goods to local Nashville nonprofits and recycle metals, electronics, and cardboard. We aim to keep as much out of the landfill as possible.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do I need to be home during the cleanout?</summary>
  <p style="margin-top:10px;margin-bottom:0;">For straightforward jobs where everything is going, no. For cleanouts where items need to be sorted, we strongly recommend you or a trusted representative be present — at least for the first few hours.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do you serve areas outside Nashville?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Yes. We serve Nashville, Clarksville, Bowling Green, Murfreesboro, Franklin, Brentwood, Hendersonville, and surrounding Middle Tennessee and Southern Kentucky communities. Check our <a href="/areas-we-serve/">service area page</a> for the full list.</p>
</details>

<p style="margin-top:32px;">If you're facing a hoarding situation and don't know where to start, call us. We've seen it all, and we're not here to judge — we're here to help you get your space back. <a href="/estate-hoarder-cleanout/">Learn more about our hoarding cleanout service</a> or <a href="/quote/">request a free quote online</a>.</p>
""",
    },

    # ── Post 2 ───────────────────────────────────────────────────────────────
    {
        "title": "Estate Cleanout After a Death: A Step-by-Step Guide for Nashville Families",
        "slug": "estate-cleanout-after-death-nashville-guide",
        "excerpt": (
            "Losing a loved one is hard enough. Figuring out what to do with a house full of "
            "belongings shouldn't make it harder. Here's a practical, compassionate guide to "
            "estate cleanouts for Nashville-area families."
        ),
        "published": timezone.now() - timedelta(days=1),
        "body": """
<p>When a family member passes away, the last thing anyone wants to think about is what to do with their belongings. But often there's a hard deadline — a lease ending, an estate sale scheduled, a house going to probate. The clock starts whether you're ready or not.</p>

<p>This guide walks you through the estate cleanout process from start to finish, including what to do first, how to decide what to keep versus donate versus discard, and when to bring in professional help.</p>

<h2>Step 1: Give Yourself Permission to Wait (A Little)</h2>

<p>There's no law that says you have to clean out a house within days of someone passing. Unless there's an immediate landlord deadline or the property is in foreclosure, take a breath. Give yourself and your family a week or two before beginning the process.</p>

<p>That said, if the deceased was renting, the clock starts immediately. Most landlords will give a grieving family 30–60 days to clear the unit, but you'll need to communicate with them quickly to understand your timeline.</p>

<h2>Step 2: Secure the Property and Gather Documents</h2>

<p>Before touching anything:</p>

<ul>
  <li>Change the locks if multiple people have keys (sadly, theft from estate properties is common)</li>
  <li>Locate the will, deed, insurance policies, financial statements, and any prepaid funeral arrangements</li>
  <li>Note any valuables — jewelry, cash, firearms, collectibles — and secure them separately</li>
  <li>Contact a probate attorney if the estate is going through probate; there may be restrictions on what can be removed before the process closes</li>
</ul>

<h2>Step 3: Sort Before You Haul</h2>

<p>The biggest mistake families make is hauling everything to the dumpster in a panic. Go room by room and create four piles:</p>

<ol>
  <li><strong>Keep</strong> — items with sentimental value or that heirs want</li>
  <li><strong>Sell</strong> — furniture, tools, collectibles, and housewares that have resale value</li>
  <li><strong>Donate</strong> — clothing, kitchenware, books, and gently used items that can go to a local charity</li>
  <li><strong>Discard</strong> — broken items, expired food, expired medications, old paperwork that doesn't need to be retained</li>
</ol>

<p>Take photos of valuable items before selling or donating for your estate accounting records.</p>

<h2>Step 4: Handle Medications and Documents Properly</h2>

<p><strong>Medications:</strong> Don't flush them and don't throw them in the trash. Nashville has medication drop-off sites at many Walgreens, CVS, and police stations. Controlled substances require special disposal.</p>

<p><strong>Financial documents:</strong> Shred anything with account numbers, Social Security numbers, or personal identifying information. Keep tax returns for at least 3 years.</p>

<p><strong>Electronics:</strong> Old computers and phones often contain personal data. Wipe or physically destroy hard drives before disposal.</p>

<h2>Step 5: Estate Sale, Auction, or Donation</h2>

<p>If the estate has significant furniture, antiques, or collectibles, consider hiring an estate sale company. They handle pricing, advertising, and the sale itself — typically taking 25–40% of proceeds. For smaller estates, Facebook Marketplace and local online auctions work well.</p>

<p>For bulk donations, Nashville-area organizations like Habitat for Humanity ReStore, Room in the Inn, and St. Vincent de Paul accept furniture and household goods and can sometimes arrange pickup for large quantities.</p>

<h2>Step 6: Bring in a Cleanout Crew for the Rest</h2>

<p>Once sorting is done and valuables are out, what remains is the physical labor of hauling. This is where a professional junk removal company earns its keep.</p>

<p>A good estate cleanout crew will:</p>
<ul>
  <li>Load everything remaining in the home — furniture, appliances, boxes, trash</li>
  <li>Do multiple truckloads if needed without upcharging per trip</li>
  <li>Donate and recycle everything possible rather than landfilling it all</li>
  <li>Leave the home broom-clean and ready for the next step</li>
</ul>

<p>We've worked dozens of estate cleanouts across Nashville, Clarksville, and Bowling Green. Families often tell us they didn't realize how much weight they were carrying — literally and emotionally — until we cleared it out. <a href="/estate-clean-out/">Learn more about our estate cleanout service</a>.</p>

<h2>How Much Does an Estate Cleanout Cost in Nashville?</h2>

<p>For a standard single-family home with a full load of furniture and household goods, expect to pay $400–$1,200 for the junk removal portion. Larger homes or those with significant volume will be on the higher end. We offer free on-site estimates — there's no obligation and no surprises. <a href="/quote/">Request an estimate here.</a></p>

<h2>Frequently Asked Questions</h2>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">How soon after a death can we start the cleanout?</summary>
  <p style="margin-top:10px;margin-bottom:0;">There's no set rule unless the estate is in probate. If the property is in probate, consult with the executor or probate attorney before removing any items — the court may need an inventory first.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Can you work around our family's sorting process?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Absolutely. We can come in stages — first haul the obvious trash while the family sorts valuables, then return for a final cleanout once decisions are made. We're flexible and work around your timeline.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">What if the house is in bad condition — animal waste, mold, pests?</summary>
  <p style="margin-top:10px;margin-bottom:0;">We handle general debris even in difficult conditions. For situations involving significant mold, sewage, or biohazardous material, we partner with licensed remediation specialists and can refer you to the right people.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do you donate what you take?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Yes. Furniture, clothing, household items, and tools that are in good shape go to local Nashville nonprofits. We document donations when requested — useful for estate records.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Can you help with a foreclosure cleanout as well?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Yes. We work frequently with property managers, banks, and real estate agents on <a href="/foreclosure-clean-out/">foreclosure cleanouts</a> across the Nashville metro. Same-day and next-day scheduling is often available.</p>
</details>

<p style="margin-top:32px;">If you're navigating an estate cleanout and could use help, we're here. <a href="/quote/">Get a free estimate</a> — we'll come to the property and give you a straight number with no pressure.</p>
""",
    },

    # ── Post 3 ───────────────────────────────────────────────────────────────
    {
        "title": "Storage Unit Cleanout: What to Keep, Sell, and Toss (Nashville Guide)",
        "slug": "storage-unit-cleanout-nashville-guide",
        "excerpt": (
            "Paying $150/month for a storage unit you haven't opened in two years? "
            "Here's how Nashville locals decide what to keep, what to sell, and how to clear "
            "out a storage unit without losing a whole weekend to it."
        ),
        "published": timezone.now(),
        "body": """
<p>Storage units have a way of becoming very expensive closets. You move something in with good intentions, pay monthly for years, and eventually the rental cost has exceeded the value of everything inside. Sound familiar?</p>

<p>This guide covers how to tackle a storage unit cleanout efficiently — what's worth keeping, what sells well, and when it makes sense to call a junk removal crew instead of renting a truck yourself.</p>

<h2>Before You Start: Is It Worth It?</h2>

<p>Do a quick mental accounting before you drive to the unit. If the contents are worth less than 6 months of rent, the math isn't in your favor to keep renting. Even if items have sentimental value, ask yourself if you've missed them in the past year. If not, you probably won't miss them next year either.</p>

<p>The average storage unit in Nashville runs $80–$200/month. A 10×10 unit you've had for 3 years at $120/month has cost you $4,320. If the contents aren't worth that to you, it's time to close it out.</p>

<h2>Step 1: Go In With a System</h2>

<p>Don't open the door and start pulling things out randomly. You'll create chaos and end up overwhelmed. Instead:</p>

<ol>
  <li>Bring three large tarps or plastic sheets to lay outside the unit</li>
  <li>As you pull items out, sort them into three zones: <strong>Keep, Sell/Donate, Discard</strong></li>
  <li>Work from front to back, row by row</li>
  <li>Don't open every box — if you labeled it and haven't needed it in 2 years, it goes in the sell/discard zone</li>
</ol>

<p>Set a hard time limit. Two to three hours is about as long as most people can sustain good decision-making in a hot or cold storage unit before fatigue sets in and everything starts looking like it should be kept.</p>

<h2>What's Actually Worth Selling</h2>

<p>These categories sell consistently well in Nashville:</p>

<ul>
  <li><strong>Power tools and hand tools</strong> — Facebook Marketplace, OfferUp, and local pawn shops pay well for working tools</li>
  <li><strong>Vintage furniture</strong> — Mid-century pieces, solid wood dressers, and antiques move quickly; skip particleboard</li>
  <li><strong>Exercise equipment</strong> — Weights, treadmills, and bikes always have buyers</li>
  <li><strong>Musical instruments</strong> — Guitars, keyboards, and amps have a strong resale market</li>
  <li><strong>Collectibles and memorabilia</strong> — Sports cards, records, and vintage toys can bring significant money if you research values first</li>
</ul>

<p>List high-value items individually on Facebook Marketplace or eBay before the cleanout date. What doesn't sell can be bundled and donated or hauled.</p>

<h2>What to Donate</h2>

<p>Nashville has excellent donation options for usable goods:</p>

<ul>
  <li><strong>Habitat for Humanity ReStore</strong> — furniture, building materials, appliances</li>
  <li><strong>Goodwill Nashville</strong> — clothing, housewares, small electronics</li>
  <li><strong>Room in the Inn</strong> — bedding, clothing, household essentials for the unhoused community</li>
  <li><strong>Books</strong> — Nashville Public Library accepts donations; so do local Little Free Libraries</li>
</ul>

<p>For large donation loads, call ahead — many nonprofits have pickup services for furniture and bulk items.</p>

<h2>What to Toss (and How)</h2>

<p>Some things just need to go:</p>

<ul>
  <li>Water-damaged or mold-affected items (don't donate these)</li>
  <li>Mattresses older than 7–10 years</li>
  <li>Broken electronics (recycle — Best Buy and Staples accept e-waste)</li>
  <li>Old paint (Tennessee has hazardous waste drop-off events; don't landfill it)</li>
  <li>Anything you wouldn't give to a friend</li>
</ul>

<h2>When to Hire a Junk Removal Company</h2>

<p>DIY works if you have a truck, a few friends willing to help, and the time to make multiple donation drop-offs. But if any of these are true, it's worth calling a crew:</p>

<ul>
  <li>The unit is 10×10 or larger and mostly full</li>
  <li>There's large furniture or heavy items (sofas, appliances, treadmills)</li>
  <li>You don't own a truck and truck rental + dump fees add up to $200+ anyway</li>
  <li>You want it gone in one day without coordinating multiple trips</li>
</ul>

<p>We handle storage unit cleanouts across Nashville, Clarksville, Brentwood, and Bowling Green. We show up with a truck and crew, sort what's donate-able, and handle the hauling — you just point at what goes. Most storage unit cleanouts take 1–3 hours. <a href="/storage-unit-clean-out/">See our storage unit cleanout service page</a> or <a href="/quote/">request a free estimate</a>.</p>

<h2>How Much Does a Storage Unit Cleanout Cost?</h2>

<p>Our pricing is based on volume. A small 5×5 or 5×10 unit with miscellaneous items typically runs $150–$350. A full 10×20 unit can run $400–$800 depending on the type of items. Compare that to a 24-hour truck rental ($75–$150) plus dump fees ($50–$100) plus your time and labor — professional cleanout often comes out close or ahead, especially for larger units.</p>

<h2>Frequently Asked Questions</h2>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Can you clean out a storage unit the same day I call?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Often, yes. We offer same-day and next-day scheduling for most storage unit cleanouts in the Nashville metro. Call us in the morning and we can frequently be there that afternoon.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do I need to be present at the storage unit?</summary>
  <p style="margin-top:10px;margin-bottom:0;">For cleanouts where everything goes, no — you can arrange access with the facility and we'll handle it. If you want to sort as we go, having you there for at least the first 30 minutes speeds things up significantly.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">What storage facilities do you work with in Nashville?</summary>
  <p style="margin-top:10px;margin-bottom:0;">We work with all major facilities including Public Storage, CubeSmart, Extra Space, and local independently owned facilities. Just let us know the address and unit number when you book.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Do you recycle or donate what you haul?</summary>
  <p style="margin-top:10px;margin-bottom:0;">Yes. Usable furniture, clothing, and tools go to local Nashville nonprofits. Metals and electronics are recycled. We aim to divert as much as possible from the landfill.</p>
</details>

<details style="border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:10px;">
  <summary style="font-weight:700;cursor:pointer;font-size:15px;">Can you help me figure out what to keep before you haul?</summary>
  <p style="margin-top:10px;margin-bottom:0;">That's not our core service — we're not appraisers. But our crew can flag obvious high-value items (tools, instruments, vintage furniture) before they go in the truck if you ask us to keep an eye out.</p>
</details>

<p style="margin-top:32px;">Ready to close out that storage unit for good? <a href="/quote/">Get a free estimate from Junk Busters</a> — we serve Nashville, Clarksville, Bowling Green, and all of Middle Tennessee.</p>
""",
    },
]


class Command(BaseCommand):
    help = "Seed 3 SEO blog posts — skips existing slugs"

    def handle(self, *args, **options):
        from website.models import BlogPost

        created = 0
        skipped = 0
        for post_data in POSTS:
            if BlogPost.objects.filter(slug=post_data["slug"]).exists():
                self.stdout.write(f"  skip  {post_data['slug']}")
                skipped += 1
                continue
            BlogPost.objects.create(
                title=post_data["title"],
                slug=post_data["slug"],
                excerpt=post_data["excerpt"],
                body=post_data["body"].strip(),
                published=post_data["published"],
                is_live=True,
            )
            self.stdout.write(self.style.SUCCESS(f"  created  {post_data['slug']}"))
            created += 1

        self.stdout.write(f"\nDone. Created: {created}  Skipped: {skipped}")
