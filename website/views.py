from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views.decorators.http import require_http_methods
from .forms import QuoteForm, BookingForm
from .models import BookingRequest

# ── Shared data ───────────────────────────────────────────────────────────────

REVIEWS = [
    {'stars': 5, 'text': "They were great! Moved everything out quickly and would absolutely use them again! I had to add to my review...I called them a couple of days ago for the 2nd time and they came this morning! They are great to work with so nice and kind! I know who I will be calling next time!", 'author': 'Jennifer B.'},
    {'stars': 5, 'text': "I am so glad we hired Junk Busters to come help us and clean up our yard. Christian was very responsive, professional, and scheduled to come take care of it in 24 hours. He seriously did such a great job in the awful heat of July. I cannot recommend him enough!", 'author': 'Shelby H.'},
    {'stars': 5, 'text': "Christian and his team at Junk Busters were quick, professional, and so nice! I gave out their info to two other friends who plan to book them as well! Absolutely would recommend them to anyone who needs to get rid of old junk, big or small.", 'author': 'Claire W.'},
    {'stars': 5, 'text': "Needed a shed cleaned out and Christian and his wife did an amazing job! They were very thorough and got the job done quickly and painlessly! Would definitely use them again if needed!", 'author': 'Leslie D.'},
]

SERVICE_AREAS_PRIMARY = [
    'Orlinda, TN', 'White House, TN', 'Goodlettsville, TN', 'Gallatin, TN',
    'Hendersonville, TN', 'Nashville, TN', 'Bowling Green, KY', 'Franklin, TN',
    'Portland, TN', 'Springfield, TN', 'Clarksville, TN',
]
SERVICE_AREAS_SECONDARY = [
    'Adairville, KY', 'Scottsville, KY', 'Russellville, KY', 'Robertson County, TN',
    'Sumner County, TN', 'Davidson County, TN', 'Williamson County, TN',
    'Logan County, KY', 'Wilson County, TN', 'Rutherford County, TN',
    'Cheatham County, TN', 'Montgomery County, TN', 'Middle, TN',
]

NASHVILLE_AREAS = [
    'Hendersonville', 'Springfield', 'Gallatin', 'Franklin TN',
    'White House', 'Smyrna', 'Lebanon', 'Clarksville',
    'Goodlettsville', 'Spring Hill', 'Portland', 'La Vergne',
]

# ── Service page data ─────────────────────────────────────────────────────────

SERVICES = {
    'junk-removal': {
        'slug': 'junk-removal',
        'title': 'Junk Removal Services',
        'hero_h1': 'Full-Service Junk Removal: Nashville to Bowling Green',
        'hero_sub': 'Fast, affordable appliance removal, furniture hauling, and residential junk pickup across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green. Call for a free estimate.',
        'meta_desc': 'Professional Junk Removal serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'junk removal Nashville TN, junk removal Clarksville TN, junk removal Bowling Green KY, junk hauling Middle Tennessee, appliance removal Nashville, furniture hauling Clarksville, residential junk pickup Bowling Green, junk removal Davidson County, junk removal Robertson County, junk removal Montgomery County, same day junk removal Nashville',
        'section1_title': 'From Clutter to Clean in No Time',
        'section1_body': [
            'Junk Busters LLC provides efficient junk removal services throughout Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green. Unwanted items create clutter and take up valuable space. Removing junk without assistance becomes a time-consuming task. That\'s where we come in. Our timely junk removal service prevents waste from piling up. We clear out unused objects to create more room for important belongings. Your property stays in better condition when junk disappears quickly.',
            'Large furniture, broken appliances, and scattered debris make homes and businesses look untidy. Heavy lifting, loading, and disposal require effort, equipment, and transportation. Handling everything alone leads to frustration. Our professional services help you clear spaces without hassle. Our team handles old furniture, unwanted electronics, and construction debris removal. Whether it\'s an estate clean-out, furniture disposal, or construction debris removal, trust us to make the process simple. Let us help you maintain a clutter-free environment that looks better and improves safety.',
        ],
        'cards_title': 'Our Range of Junk Removal Services',
        'yellow_cards': [
            {'title': 'Household Junk Removal', 'body': 'Old furniture, broken appliances, and scattered clutter reduce available space. We remove sofas, tables, chairs, mattresses, and other large objects. Electronics, old clothes, and miscellaneous household items also get hauled away. Our team handles each job safely and responsibly. Junk disposal should not be a burden. Our services make it quick and stress-free.'},
            {'title': 'Garage and Storage Clean-Outs', 'body': 'Garages and storage units often become crowded with unused items. A cluttered storage area makes finding important belongings difficult. Our team removes outdated furniture, tools, machinery, and proper disposal keeps the process efficient. Clearing a garage or storage unit creates more room for essential belongings.'},
            {'title': 'Furniture and Appliance Removal', 'body': 'Removing old furniture and appliances without assistance takes time and effort. Heavy objects require careful handling to prevent property damage. Our junk removal services include removing sofas, tables, cabinets, refrigerators, washing machines, and other large items. We transport bulky items to proper disposal sites.'},
            {'title': 'Construction Debris Removal', 'body': 'Renovation and construction projects create a lot of waste. Leftover materials clutter workspaces and create safety hazards. Our hauling service includes the removal of wood, insulation, drywall, and other construction materials. Cleaning up after a project improves safety and prevents delays.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Trust Junk Busters LLC to deliver fast and professional junk removal services across Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green. We have access to the knowledge, tools, and expertise to handle items of all sizes, including heavy and bulky ones. Our team follows a structured approach, making each job seamless and hassle-free. Every job is handled with professionalism, efficiency, and proper disposal methods. Our safe disposal practices help reduce environmental impact. Give us a call now to schedule a service.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'White House, TN', 'Springfield, TN', 'Gallatin, TN', 'Hendersonville, TN', 'Franklin, KY', 'Portland, TN', 'Goodlettsville, TN', 'Russellville, KY', 'La Vergne, TN'],
    },

    'fence-removal': {
        'slug': 'fence-removal',
        'title': 'Fence Removal',
        'hero_h1': 'Fence Removal & Teardown in Middle TN & Southern KY',
        'hero_sub': 'Professional wood, vinyl, and chain-link fence disposal and property line clearing across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Fence Removal serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'fence removal Nashville TN, fence removal Clarksville TN, fence removal Bowling Green KY, wood fence disposal Middle Tennessee, vinyl fence removal Nashville, chain-link fence disposal Clarksville, property line clearing Bowling Green, fence removal Robertson County, fence hauling Middle TN',
        'section1_title': 'Fence Removal Services',
        'section1_body': [
            'Junk Busters in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, is your premier service provider for all your fence removal needs. Whether you\'re renovating your property or clearing out old boundaries, our expert team is equipped to handle both residential and commercial fence removal projects efficiently and responsibly.',
            'Understanding the nuances of proper fence disposal, Junk Busters offers a comprehensive service that includes not just the dismantling of your old fence but also ensures eco-friendly disposal and recycling of the materials. Our services cover a wide range of fence types including wood, metal, and vinyl, making us a versatile choice for any fence removal task in the Nashville area.',
            'Our process begins with a thorough assessment of your site and fencing materials. This enables us to provide a precise and transparent quote, ensuring you understand the scope and cost of the project upfront, with no hidden fees. We then schedule the removal at a time that suits your business operations, ensuring maximum convenience.',
            'We pride ourselves on our commitment to customer satisfaction and our ability to provide hassle-free services. Once the old fence is removed, your property is left clean and ready for your next project. If you\'re in Nashville and need reliable fence removal services, don\'t hesitate to contact Junk Busters. Schedule your service online at our website or give us a call directly at 615-881-2505 to discuss your project. Let us help you reclaim your space with our efficient and environmentally conscious fence removal services.',
        ],
        'cards_title': None,
        'yellow_cards': [],
        'section2_title': 'We Provide Fence Removal in Surrounding Areas',
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Our team is trained to handle your project with the utmost professionalism, ensuring that all debris is removed completely and your property is left clean and ready for your next project.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Hendersonville, TN', 'Gallatin, TN', 'Goodlettsville, TN', 'Springfield, TN', 'White House, TN', 'Spring Hill, TN', 'Franklin, TN', 'Lebanon, TN', 'Portland, TN', 'Franklin, KY', 'Russellville, KY'],
    },

    'estate-clean-out': {
        'slug': 'estate-clean-out',
        'title': 'Estate Clean-Out',
        'hero_h1': 'Compassionate Estate Cleanouts in Middle TN & KY',
        'hero_sub': 'Probate cleanout assistance, real estate readiness, and senior downsizing help across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Estate Clean-Out serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'estate clean out Nashville TN, estate cleanout Clarksville TN, estate cleanout Bowling Green KY, probate cleanout Nashville, real estate readiness Middle TN, senior downsizing help Clarksville, estate cleanout Davidson County, estate cleanout Robertson County, full estate clearing Middle Tennessee',
        'section1_title': 'Junk Busters LLC Estate Cleanout Services',
        'section1_body': [
            'Embarking on the journey of an estate clean-out with Junk Busters in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, is akin to orchestrating a symphony of transformation. With a delicate balance of sensitivity and efficiency, we navigate the remnants of a lifetime, honoring memories while clearing space for new beginnings.',
            'Our process begins with a comprehensive assessment, where we listen attentively to your needs and concerns. Whether it\'s downsizing, relocating, or managing the estate of a loved one, we tailor our approach to suit your unique circumstances.',
            'Once we\'ve crafted a personalized plan, our dedicated team springs into action, meticulously sorting, hauling, and disposing of items with care and respect. From bulky furniture to sentimental mementos, no task is too daunting for our seasoned professionals.',
            'Throughout the process, we prioritize sustainability, striving to minimize waste through responsible disposal and donation efforts. By partnering with local charities and recycling facilities, we ensure that your unwanted items find new purpose in the community.',
            'As the final resonates of the estate are cleared, we leave behind a transformed space, ready for its next chapter. If you\'re ready to embark on this journey of renewal, call Junk Busters at 615-881-2505 or schedule online today. Let us help you reclaim your space and usher in a new era of possibility.',
        ],
        'cards_title': 'Efficiently Clearing Out Estate Properties — Step-By-Step',
        'yellow_cards': [
            {'title': 'Evaluation and Customized Planning', 'body': 'Start by scheduling a consultation with Junk Busters. Our team will conduct an on-site assessment to gauge the scale of the cleanout, and discuss your specific requirements and timeframe. From there, we\'ll develop a tailored plan to the property\'s unique needs.'},
            {'title': 'Removal of Belongings and Debris', 'body': 'Once the plan is set, our skilled professionals will efficiently clear out belongings, furniture, and debris from the property. We handle each item with care, ensuring that sentimental possessions are identified and treated according to your preferences.'},
            {'title': 'Donation and Recycling Efforts', 'body': 'Sustainability is at the core of our practices. Items are sorted for donation to local charities, benefiting those in need in our community. Additionally, we prioritize recycling to minimize waste and promote environmental responsibility.'},
            {'title': 'Final Inspection and Completion', 'body': 'After the cleanout and any additional services are rendered, we conduct a thorough final inspection to ensure the property meets your standards. Our aim is to leave the space in optimal condition.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'At Junk Busters, we understand the sensitive nature of estate cleanouts. Our dedicated team is committed to providing compassionate support and dependable services every step of the way. Contact us today at 615-881-2505 to schedule a consultation and entrust us with the cleanout and restoration of your estate.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Lebanon, TN', 'Franklin, TN', 'Mt. Juliet, TN', 'Hendersonville, TN', 'Gallatin, TN', 'Brentwood, TN', 'Thompson\'s Station, TN', 'Spring Hill, TN', 'Franklin, KY'],
    },

    'eviction-clean-out': {
        'slug': 'eviction-clean-out',
        'title': 'Eviction Clean-Out',
        'hero_h1': 'Fast Eviction Trash-Outs for Nashville & Clarksville',
        'hero_sub': 'Property manager services, rapid turnover cleanouts, and tenant debris removal across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Eviction Clean-Out serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'eviction clean out Nashville TN, eviction cleanout Clarksville TN, eviction cleanout Bowling Green KY, property manager services Nashville, rapid turnover cleanout Clarksville, tenant debris removal Bowling Green, landlord junk removal Middle Tennessee, eviction debris removal Davidson County',
        'section1_title': 'Junk Busters LLC Eviction Cleanout Services',
        'section1_body': [
            'Engaging in an eviction cleanout with Junk Busters in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, signifies our dedication to reinstating order and peace to spaces transitioning through challenging times. With our committed team, we navigate the aftermath of eviction with lean efficiency and compassion, ensuring a smooth process for everyone involved.',
            'Our journey commences with a thorough assessment, where we attentively listen to property owners, landlords, and property management companies, understanding their unique circumstances and needs. Acknowledging the urgency and sensitivity of eviction situations, we prioritize prompt action and meticulous planning.',
            'Upon devising a strategy, our experienced professionals swiftly leap into action, removing belongings, furniture, and debris from the premises. Each item is handled with care, adhering to local regulations and standards, and in coordination with local sheriffs and tax enforcement agencies to ensure safe removal in compliance with the law.',
            'Throughout the cleanout process, we emphasize responsible disposal practices, maximizing recycling and donation efforts to minimize waste and benefit the community.',
        ],
        'cards_title': 'How To Clean Out An Eviction Property — Step-By-Step',
        'yellow_cards': [
            {'title': 'Assessment & Planning', 'body': 'Schedule a consultation where we evaluate the property\'s condition and your specific needs & develop a customized plan tailored to the property\'s requirements, ensuring swift and efficient action.'},
            {'title': 'Removal', 'body': 'Our experienced team swiftly clears belongings, furniture, and debris, adhering to local laws and coordinating with law enforcement when necessary. Prioritize responsible disposal practices, maximizing recycling and donation efforts.'},
            {'title': 'Final Inspection', 'body': 'Conduct a thorough inspection to ensure the property is left in optimal condition.'},
        ],
        'section2_title': 'Junk Busters LLC Provides Eviction Cleanout Services Across Middle TN & Southern KY Including:',
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Trust Junk Busters for professional and compassionate eviction property cleanouts. Contact us at 615-881-2505 or schedule online.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Lebanon, TN', 'La Vergne, TN', 'Smyrna, TN', 'Franklin, TN', 'Mt. Juliet, TN', 'Hendersonville, TN', 'Gallatin, TN', 'Thompson\'s Station, TN', 'Spring Hill, TN', 'Franklin, KY'],
    },

    'foreclosure-clean-out': {
        'slug': 'foreclosure-clean-out',
        'title': 'Foreclosure Clean-Out',
        'hero_h1': 'REO & Foreclosure Clean-Out Specialists',
        'hero_sub': 'Bank-owned property clearing, trash-out services, and yard cleanup for REO agents across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Foreclosure Clean-Out serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'foreclosure clean out Nashville TN, foreclosure cleanout Clarksville TN, foreclosure cleanout Bowling Green KY, bank-owned property clearing Nashville, trash-out services Clarksville, REO yard cleanup Middle Tennessee, REO property junk removal Nashville, foreclosure cleanout Southern KY',
        'section1_title': 'Junk Busters LLC Foreclosure & REO Cleanout Services',
        'section1_body': [
            'Foreclosure cleanouts present significant challenges, combining emotional effort with the physical effort of clearing belongings. Enter Junk Busters, your go-to full-service junk removal experts specializing in foreclosure cleanouts. We handle everything from furniture and appliances to hazardous materials with precision and care.',
            'Understanding the difficulty of this time, we strive to offer a stress-free experience. Benefit from a complimentary estimate for complete transparency.',
            'Our comprehensive foreclosure cleanout services include furniture and appliance removal, debris cleanup, hazardous material disposal, dismantling large items, donating usable items, and secure document shredding.',
            'Enjoy same-day service, free estimates, and peace of mind with our full insurance coverage. Reclaim your space and your peace of mind — reach out to Junk Busters today at 615-881-2505 or book online. Let us restore order to your home, empowering you to move forward.',
        ],
        'cards_title': 'How Do We Price Foreclosure Cleanouts?',
        'yellow_cards': [
            {'title': 'Initial Assessment', 'body': 'We begin by conducting an initial assessment of the property to determine the scope of the cleanout project. This involves evaluating the size of the property, the volume of items to be removed, and any specific requirements or challenges involved.'},
            {'title': 'Custom Quote', 'body': 'Based on the assessment, we provide a custom quote tailored to the needs of the client. At Junk Busters our jobs are priced based on volume, so larger properties with more volume of junk will cost more.'},
            {'title': 'Transparent Communication', 'body': 'Throughout the pricing process, we maintain transparent communication with our clients, explaining the breakdown of costs and answering any questions or concerns they may have. We believe in building trust and ensuring satisfaction with our services.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Our pricing approach is designed to provide competitive rates while delivering high-quality and reliable foreclosure cleanout services to our clients. We strive to exceed expectations and ensure a smooth and stress-free experience from start to finish. Call us at 615-881-2505 or book online today to find out why we are the preeminent service provider in the area.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Lebanon, TN', 'La Vergne, TN', 'Smyrna, TN', 'Franklin, TN', 'Mt. Juliet, TN', 'Hendersonville, TN', 'Gallatin, TN', 'Brentwood, TN', 'Franklin, KY', 'Spring Hill, TN'],
    },

    'bulk-cardboard-removal': {
        'slug': 'bulk-cardboard-removal',
        'title': 'Bulk Cardboard Removal & Pickup',
        'hero_h1': 'Commercial Bulk Cardboard Removal & Recycling',
        'hero_sub': 'Warehouse recycling, scheduled pickups, and cardboard hauling for businesses and homes across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Bulk Cardboard Removal serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'bulk cardboard removal Nashville TN, cardboard removal Clarksville TN, cardboard hauling Bowling Green KY, warehouse recycling Nashville, scheduled cardboard pickups Clarksville, commercial cardboard removal Middle TN, cardboard pickup Nashville, cardboard recycling Middle Tennessee',
        'section1_title': 'Bulk Cardboard Removal & Pickup',
        'section1_body': [
            'If you\'re in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, and in need of bulk cardboard removal, Junk Busters is your go-to service. We specialize in efficient and environmentally-friendly cardboard recycling, ensuring that your excess packaging material is disposed of correctly. Our services are tailored to meet the needs of both residential and commercial clients, making us a popular choice for bulk cardboard disposal in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green.',
            'At Junk Busters, we understand the importance of sustainability, which is why we emphasize cardboard recycling as a key component of our services. Whether it\'s a one-time pickup or a regular commercial cardboard removal contract, we are equipped to handle jobs of any size. Our team is committed to providing reliable service, including scheduled hassle-free bulk cardboard pickups that work around your business operations to minimize disruption.',
            'For those particularly large or urgent jobs, we offer a streamlined process that includes easy online booking and upfront pricing. This transparency in pricing ensures that you know exactly what the service will cost without any hidden fees. Plus, our local presence in Nashville means we\'re always just a phone call away from helping you manage your cardboard disposal needs efficiently.',
            'Choose Junk Busters for your cardboard removal and join countless other satisfied customers who rely on us for their recycling and waste management needs. We\'re proud to help keep Nashville clean and green, one pickup at a time.',
        ],
        'cards_title': 'HOW To Set Up A Contract For Your Business Cardboard Pickup:',
        'yellow_cards': [
            {'title': 'Step 1: Initial Contact', 'body': 'Reach out to Junk Busters: Contact Junk Busters by phone, email, or through their website. Provide basic information about your business, including the type of business, volume of cardboard waste, and your location.'},
            {'title': 'Step 2: Assess Your Needs', 'body': 'Evaluate Your Cardboard Disposal Needs: Determine how much cardboard your business typically accumulates and how frequently you need it picked up. This will help in negotiating the terms of the contract.'},
            {'title': 'Step 3: Discuss Service Details', 'body': 'Pickup Frequency: Decide how often you need cardboard pickup services (e.g., weekly, biweekly, monthly). Service Customization: Discuss any specific requirements you might have, such as after-hours pickup or handling particularly large or small quantities of cardboard.'},
            {'title': 'Step 4: Negotiate the Contract', 'body': 'Pricing: Get a detailed breakdown of the costs. This could be a flat rate per pickup or a variable rate depending on the volume of cardboard. Contract Terms: Review the terms of the service agreement, which should include the length of the contract, cancellation policy, and any penalties for service interruptions.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Junk Busters LLC is proud to help Middle TN & Southern KY businesses and homeowners recycle responsibly. Call 615-881-2505 to schedule your bulk cardboard pickup anywhere in Nashville, Clarksville, or Bowling Green today.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Hendersonville, TN', 'Springfield, TN', 'Gallatin, TN', 'White House, TN', 'Smyrna, TN', 'Lebanon, TN', 'Goodlettsville, TN', 'Spring Hill, TN', 'Portland, TN', 'La Vergne, TN', 'Franklin, KY'],
    },

    'garage-clean-out': {
        'slug': 'garage-clean-out',
        'title': 'Garage Clean-Out Service',
        'hero_h1': 'Garage & Basement Clean-Out: Reclaim Your Space',
        'hero_sub': 'Clutter removal, shelving teardown, and organized disposal across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Garage Clean-Out serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'garage clean out Nashville TN, garage cleanout Clarksville TN, basement clean out Bowling Green KY, clutter removal Nashville, shelving teardown service Middle TN, organized disposal Clarksville, garage junk removal Nashville, garage cleanout Bowling Green KY',
        'section1_title': 'Garage & Basement Clean-Out Services',
        'section1_body': [
            'Junk Busters in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, offers top-notch garage clean-out services that cater to both residential and commercial needs. Our team specializes in efficiently cleaning out clutter, leaving your garage space clean and usable. We understand that over time, garages can accumulate not just junk — from outdated appliances to general furniture to everyday items — that can\'t just be thrown away.',
            'Our services include hauling away junk, garbage, and unwanted items from your garage quickly. We also pride ourselves on being able to provide hassle-free service, all while being mindful of the environment. We use a popular Google Keywords to ensure you\'re finding the most relevant information. Here\'s a step-by-step guide incorporating top SEO keywords to ensure you\'re finding the most relevant information.',
            'For residents and businesses in Nashville seeking reliable and efficient junk removal services, Junk Busters is your go-to provider. We pride ourselves on our customer satisfaction and our ability to provide hassle-free service, all while being mindful of the environment. Take advantage of our online scheduling system for the quickest service. Alternatively, if you prefer a more personal touch, you can always call us at 615-881-2505 to discuss your needs and set up a service time. Don\'t let junk take over your valuable space — contact Junk Busters today and reclaim your garage!',
        ],
        'cards_title': 'How Does Garage Clean Out Work? (Step by Step Guide)',
        'yellow_cards': [
            {'title': 'Step 1: Schedule a Consultation', 'body': 'Visit the Junk Busters website or call them directly to schedule a consultation. You can discuss the scope of your garage clean out and any specific requirements you might have. This is a great time to ask about their recycling and donation guidelines to ensure eco-friendly disposal.'},
            {'title': 'Step 2: Receive a Free Quote', 'body': 'Based on your provided information, Junk Busters will give you a quote for the clean-out service. Ensure the quote includes all costs associated with hauling and disposal of your garage junk.'},
            {'title': 'Step 3: Prepare Your Garage', 'body': 'Before the scheduled pick-up day, organize your garage. Separate items into categories like keep, donate, and trash. Label items clearly and make sure the driveway is clear to facilitate easy access for the Junk Busters team.'},
            {'title': 'Step 4: The Clean-Out Day', 'body': 'On the day of the clean-out, the Junk Busters team will arrive to remove the items you\'ve designated for disposal. They\'ll handle the heavy lifting and proper disposal, ensuring your garage is left clean and spacious.'},
            {'title': 'Step 5: Follow Up', 'body': 'After the clean-out service, Junk Busters may follow up to ensure that everything was completed to your satisfaction. This is a good time to provide feedback on the service to help them improve.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Ready to reclaim your garage space? Schedule your garage clean-out with Junk Busters today by visiting our website at calling us directly at 615-881-2505 to discuss your needs and set up a service time.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Hendersonville, TN', 'Springfield, TN', 'Gallatin, TN', 'White House, TN', 'Smyrna, TN', 'Lebanon, TN', 'Goodlettsville, TN', 'Spring Hill, TN', 'Portland, TN', 'La Vergne, TN', 'Franklin, KY'],
    },

    'storage-unit-clean-out': {
        'slug': 'storage-unit-clean-out',
        'title': 'Storage Unit Clean-Out',
        'hero_h1': 'Storage Unit Cleanouts: We Handle the Haul',
        'hero_sub': 'Delinquent unit clearing, downsizing, and off-site junk removal across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Storage Unit Clean-Out serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'storage unit clean out Nashville TN, storage unit cleanout Clarksville TN, storage unit cleanout Bowling Green KY, delinquent unit clearing Nashville, downsizing storage cleanout Clarksville, off-site junk removal Bowling Green, storage unit junk removal Middle TN, storage facility cleanout Middle Tennessee',
        'section1_title': 'Storage Unit Cleanout Services Across Middle TN & Southern KY',
        'section1_body': [
            'Looking for a reliable storage unit cleanout service in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green? Look no further than Junk Busters! We specialize in clearing out storage units quickly and efficiently, helping you vacate the space without the hassle. Our professional team is trained to handle items of all sizes and types, ensuring that everything from old furniture and electronics to miscellaneous clutter is removed with care.',
            'At Junk Busters, we understand that your time is valuable. That\'s why we offer flexible scheduling to fit your busy lifestyle, providing cleanout services at a time that\'s convenient for you. We also pride ourselves on our commitment to environmental responsibility, recycling or donating items whenever possible to minimize waste.',
            'Whether you\'re downsizing, relocating, or simply decluttering, Junk Busters is here to help with your storage unit cleanout needs in Nashville. Our transparent pricing model means no hidden fees, providing you with a straightforward quote based on the volume of items to be removed.',
            'Don\'t let a cluttered storage unit weigh you down. Contact Junk Busters today at 615-881-2505 or book our services online. Take the first step towards a clutter-free life with our trusted storage unit cleanout services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green. Let us do the heavy lifting for you!',
        ],
        'cards_title': 'Common Items Junk Busters Disposes Of In Storage Unit Cleanouts',
        'yellow_cards': [
            {'title': 'Assessment & Planning', 'body': 'Schedule a consultation where we evaluate the storage unit\'s condition and your specific needs & develop a customized plan tailored to the property\'s requirements, ensuring swift and efficient action.'},
            {'title': 'Removal', 'body': 'Our experienced team swiftly clears belongings, furniture, and debris, adhering to local laws and coordinating with law enforcement when necessary. Prioritize responsible disposal practices, maximizing recycling and donation efforts.'},
            {'title': 'Final Inspection', 'body': 'Conduct a thorough inspection to ensure the property is left in optimal condition.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Trust Junk Busters LLC for professional storage unit clean-outs across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green. Contact us at 615-881-2505 or schedule online.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Hendersonville, TN', 'Springfield, TN', 'Gallatin, TN', 'White House, TN', 'Smyrna, TN', 'Lebanon, TN', 'Goodlettsville, TN', 'Spring Hill, TN', 'Portland, TN', 'La Vergne, TN', 'Franklin, KY'],
    },

    'hot-tub-removal': {
        'slug': 'hot-tub-removal',
        'title': 'Hot Tub Removal',
        'hero_h1': 'Hot Tub Removal & Disposal Specialists',
        'hero_sub': 'Safe electrical disconnect, spa teardown, and deck-mounted hot tub removal across Middle TN & Southern KY — Nashville, Clarksville, and Bowling Green.',
        'meta_desc': 'Professional Hot Tub Removal serving Middle TN and Southern KY. Fast, reliable, and eco-friendly. Call 615-881-2505 for a free regional estimate.',
        'meta_keywords': 'hot tub removal Nashville TN, hot tub removal Clarksville TN, hot tub removal Bowling Green KY, safe electrical disconnect spa removal Nashville, spa teardown Clarksville, deck-mounted hot tub removal Bowling Green, jacuzzi removal Nashville, hot tub disposal Middle Tennessee',
        'section1_title': 'Hot Tub Removal & Disposal Services',
        'section1_body': [
            'Are you looking to remove an old hot tub from your property? Junk Busters specializes in hot tub removal services, providing a hassle-free way to reclaim your space. Our experienced team in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, is equipped to handle the heavy lifting and proper disposal of unwanted hot tubs, ensuring a seamless process from start to finish.',
            'Hot tub removal can be a daunting task, given the size and complexity of the job. These units are not only heavy but are often connected to electrical and plumbing systems that require careful disconnection. Junk Busters has the expertise to safely disconnect and remove hot tubs, regardless of their location on your property. Whether it\'s nestled on an outdoor deck, fitted into a bathroom, or freestanding in a garden, our professionals manage the extraction without damaging your property.',
            'We are committed to environmentally responsible disposal practices. Depending on the condition and age of the hot tub, Junk Busters also aims to recycle parts when possible. For units that are beyond salvage, we ensure that they are disposed of in compliance with local health regulations, reducing the impact on the environment.',
            'Junk Busters offers competitive pricing and transparent quotes, with no hidden fees. Our straightforward process means you can get a quote quickly and schedule your hot tub removal at a time that works best for you. Residents of Nashville can trust us for efficient and reliable service.',
        ],
        'cards_title': 'How to Remove a Hot Tub — Middle TN & Southern KY (Step by Step Guide)',
        'yellow_cards': [
            {'title': 'Assessment and Preparation', 'body': 'Our team conducts a thorough assessment to understand the setup and integration of your hot tub, including its connection to electrical and plumbing systems. We prepare the area to prevent any damage to your property during removal.'},
            {'title': 'Safe Disconnection', 'body': 'Safety is our top priority. We carefully disconnect the hot tub from all power sources and plumbing, according to Nashville\'s safety regulations to ensure that there are no hazards.'},
            {'title': 'Removal and Transportation', 'body': 'Using specialized equipment, such as reciprocating saws, sledge hammers, or other cutting tools, the hot tub is safely removed and loaded onto our removal trucks. Our team is trained to handle heavy and awkward items smoothly.'},
        ],
        'section2_title': 'We Provide Hot Tub Removal Services In Surrounding Areas:',
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Junk Busters LLC provides competitive pricing and transparent quotes, with no hidden fees. Residents across Middle TN and Southern KY — Nashville, Clarksville, Bowling Green, and beyond — can trust us for efficient and reliable hot tub removal. Call 615-881-2505 today.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Hendersonville, TN', 'Gallatin, TN', 'Goodlettsville, TN', 'Springfield, TN', 'White House, TN', 'Smyrna, TN', 'Spring Hill, TN', 'Franklin, TN', 'Lebanon, TN', 'Portland, TN', 'La Vergne, TN', 'Franklin, KY'],
    },

    'residential-cleaning': {
        'slug': 'residential-cleaning',
        'title': 'Residential Cleaning Services',
        'hero_h1': 'Residential Cleaning Services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green',
        'hero_sub': 'Professional, thorough residential cleaning for homes across Davidson, Robertson, Sumner & surrounding counties.',
        'meta_desc': 'Professional residential cleaning services in Nashville, White House & Middle Tennessee. Junk Busters keeps your home spotless. General cleaning, deep cleaning & more. Call 615-881-2505.',
        'meta_keywords': 'residential cleaning Nashville TN, house cleaning Nashville Tennessee, home cleaning White House TN, residential cleaning Davidson County, maid service Nashville, cleaning service Robertson County',
        'section1_title': 'Bringing Shine Back to Your Space',
        'section1_body': [
            'A clean home provides a comfortable and healthy living space. Dirt, dust, and clutter accumulate quickly, making rooms feel untidy. If you are looking for a reliable residential cleaning service in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, that can help you remove clutter, Junk Busters LLC. Many people struggle to find time for deep cleaning. Our professional services handle this task, making home maintenance easier. We understand that household cleaning requires both light upkeep, while others require a more detailed approach. Our process addresses floors, surfaces, furniture, and other areas that need frequent attention.',
            'High-traffic areas collect more dirt and dust. Kitchen grease, bathroom buildup, and unclean surfaces create an unhealthy environment. Expert cleaning removes these problems efficiently. Our methods help you maintain dust-free furniture, spotless floors, and sanitized countertops. Improving indoor air quality. Scheduling routine cleanings with us will enable you to keep your home looking and feeling fresh.',
        ],
        'cards_title': 'Residential Cleaning Services We Offer',
        'yellow_cards': [
            {'title': 'General House Cleaning', 'body': 'Keeping a home clean improves daily living. Dust, dirt, and grime build up on furniture, floors, and surfaces. Cleaning removes these particles, keeping the environment fresh. Our services include mopping, sweeping, dusting, and disinfecting high-touch surfaces. Appliances, door handles, and light switches receive special attention.'},
            {'title': 'One-Time Deep Cleaning', 'body': 'Deep cleaning focuses on hidden dirt and neglected areas. Standard cleaning removes surface dust, but deeper grime requires extra attention. Over time, buildup forms on baseboards, vents, and ceiling fans. We clean baseboards, walls, windowsills, and hard-to-reach areas. A detailed approach creates a healthier home.'},
            {'title': 'Move-In and Move-Out Cleaning', 'body': 'Moving brings excitement and stress. Getting into the space looks better when the space is clean. Our services include a thorough cleaning of floors, walls, appliances, and cabinets. Those moving out also benefit from our dependable cleaning service. Leaving a property clean helps get a smooth transition.'},
            {'title': 'Recurring Cleaning Services', 'body': 'Regular cleaning keeps a busy lifestyle in check. A cleaning schedule prevents dust and dirt from accumulating. We offer weekly, bi-weekly, and monthly cleaning plans. Mopping, vacuuming, dusting, and sanitizing help maintain cleanliness. Routine maintenance makes home care simpler.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Junk Busters LLC delivers reliable residential cleaning for a better living experience. We help keep your property clean, making sure all areas receive proper care. Our experienced cleaning crew in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, pays attention to every room, making sure all areas receive proper care. If you want to learn more about our residential cleaning services in White House & Nashville, reach out to us today.',
        'local_areas': ['White House', 'Nashville TN', 'Goodlettsville', 'Springfield', 'Gallatin', 'Hendersonville', 'La Vergne', 'Davidson County', 'Robertson County', 'Sumner County'],
    },

    'air-bnb-cleaning': {
        'slug': 'air-bnb-cleaning',
        'title': 'Air BnB Cleaning Services',
        'hero_h1': 'Air BnB Cleaning Services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green',
        'hero_sub': 'Professional Airbnb cleaning to keep your rental spotless and guests happy across Middle TN & Southern KY.',
        'meta_desc': 'Professional Airbnb cleaning services in Nashville, White House & Middle Tennessee. Fast turnovers, spotless results. Junk Busters keeps your rental 5-star ready. Call 615-881-2505.',
        'meta_keywords': 'airbnb cleaning Nashville TN, Airbnb cleaning service Nashville Tennessee, vacation rental cleaning Nashville, short term rental cleaning Nashville, Airbnb turnover cleaning White House TN',
        'section1_title': 'Cleaning with Your Guests in Mind',
        'section1_body': [
            'A well-maintained short-term rental creates a welcoming environment for guests. Cleanliness plays a major role in guest satisfaction, influencing reviews and future bookings. Travelers expect spotless spaces, fresh linens, and sanitized surfaces. Any sign of dirt, dust, or clutter can create a negative impression. At Junk Busters LLC, we provide expert AirBnB cleaning services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, helping you get better ratings and increase reservations. Regular cleaning removes dirt, eliminates germs, and keeps rental properties guest ready.',
            'The appearance of each room directly affects guest comfort. A tidy space helps travelers feel comfortable and at home. By choosing us, you can create a more pleasant stay with neatly arranged furniture, dust-free surfaces, and fresh-smelling spaces. We clean kitchens, bathrooms, and living areas to make a positive impact. Our services prevent dirt and clutter from accumulating. By choosing us you create a well-prepared property that increases guest satisfaction and encourages repeat bookings. A spotless property creates a positive impression from the moment guests arrive.',
        ],
        'cards_title': 'Comprehensive Range of AirBnB Cleaning Solutions',
        'yellow_cards': [
            {'title': 'Guest Room Cleaning', 'body': 'A fresh and inviting bedroom makes guests feel comfortable. Clean linens, dust-free surfaces, and vacuumed floors improve the overall appearance of a rental. Any overlooked detail can affect how guests perceive the rental. Our services include changing bedsheets, wiping down surfaces, cleaning door handles, and removing stains from all surfaces.'},
            {'title': 'Bathroom Sanitization', 'body': 'A sparkling bathroom adds to the overall appeal of a rental. Water spots, grime, and soap residue can create an unpleasant appearance. We scrub, disinfect showers, bathtubs, and toilets. All surfaces receive disinfection, including countertops, mirrors, and fixtures. A properly cleaned bathroom enhances guest satisfaction.'},
            {'title': 'Kitchen Cleaning', 'body': 'A spotless kitchen makes a rental feel more inviting. Food spills, grease, and crumbs can make the space look unkempt. We clean and sanitize all kitchen surfaces. Our services include wiping countertops, disinfecting sinks, and cleaning appliances. A well-organized cooking area adds convenience for guests.'},
            {'title': 'Living Area and Common Space Cleaning', 'body': 'A neat and organized living space makes guests feel welcome. Clutter, dust, and dirt can create a negative impression. We vacuum carpets, wipe down coffee tables, and disinfect high-touch areas. Clean surroundings create a more enjoyable stay.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Junk Busters LLC delivers reliable AirBnB cleaning for a better guest experience. We help keep your rental property clean, making sure all areas receive proper care. Our experienced cleaning crew in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, pays attention to every room, making sure all areas receive proper care. Hosts benefit from fast turnovers, allowing new guests to check in without delay. To find out more information about our services and scheduling options, reach out to us today.',
        'local_areas': ['Nashville TN', 'White House', 'Hendersonville', 'Gallatin', 'Goodlettsville', 'Brentwood', 'Franklin TN', 'Murfreesboro', 'Smyrna', 'Spring Hill', 'Mt. Juliet', 'Lebanon'],
    },

    'move-in-move-out-cleaning': {
        'slug': 'move-in-move-out-cleaning',
        'title': 'Move In/Move Out Cleaning',
        'hero_h1': 'Move In/Out (Vacancy) Cleaning Services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green',
        'hero_sub': 'Thorough move-in and move-out cleaning services for homeowners, landlords & property managers.',
        'meta_desc': 'Professional move-in/move-out cleaning services in Nashville, White House & Middle Tennessee. Junk Busters prepares properties for new occupants. Call 615-881-2505.',
        'meta_keywords': 'move in move out cleaning Nashville TN, vacancy cleaning Nashville Tennessee, move out cleaning service Nashville, move in cleaning White House TN, rental property cleaning Nashville Davidson County',
        'section1_title': 'Junk Busters Vacancy, Move-in/out Cleaning Service',
        'section1_body': [
            'At Junk Busters in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, we take pride in offering comprehensive move-in/move-out deep cleaning services tailored to the unique needs of homeowners, property managers, Airbnb hosts, and commercial businesses. With a close relationship with local stakeholders, we understand the importance of leaving properties immaculate for new occupants or guests.',
            'Our process begins with a detailed consultation where we take attentively to our clients\' requirements and preferences. Whether it\'s preparing a property for new tenants, ensuring a fresh start for homeowners, or maintaining high-cleanliness standards for commercial spaces, we customize our approach accordingly.',
            'Once the plan is in place, our dedicated team of professionals meticulously executes the deep-cleaning process. From scrubbing floors and surfaces to sanitizing kitchens and bathrooms, we leave no corner untouched. We utilize industry-leading cleaning products and equipment to ensure exceptional results every time.',
            'We prioritize sustainability by using eco-friendly cleaning solutions and minimizing waste wherever possible. Our process is designed to ensure a seamless experience for all parties involved.',
            'Whether you\'re in need of move-in/move-out deep cleaning services for your home, rental property, or commercial space, trust Junk Busters to deliver top-notch results. Contact us today at 615-881-2505 or schedule online to book your cleaning appointment.',
        ],
        'cards_title': 'How Junk Busters Performs Vacancy Deep Cleans (Step By Step Guide):',
        'yellow_cards': [
            {'title': 'Initial Assessment', 'body': 'At Junk Busters, our experienced team begins by conducting a meticulous assessment of your property, identifying areas that require special attention to ensure a thorough cleaning process.'},
            {'title': 'Decluttering', 'body': 'Before diving into deep cleaning, we prepare the space, removing any debris, unwanted items, and clutter to create a clean and organized environment for the cleaning process.'},
            {'title': 'Surface Cleaning', 'body': 'Using high-quality cleaning agents, our dedicated team meticulously dusts and wipes down all surfaces, including countertops, shelves, and furniture, to ensure they are spotless.'},
            {'title': 'Floor Cleaning', 'body': 'We focus on rejuvenating your floors by vacuuming carpets, sweeping hardwood or tile floors, and mopping to ensure they are spotless and free of dust and stains.'},
            {'title': 'Kitchen Deep Clean', 'body': 'Our attention to detail extends to the kitchen, where we thoroughly scrub and disinfect appliances, cabinets, and countertops to remove grease, food residue, and bacteria.'},
            {'title': 'Bathroom Sanitization', 'body': 'Our team pays special attention to bathrooms, scrubbing and disinfecting showers, tubs, toilets, sinks, and tiles to eliminate mold, mildew, and soap scum, leaving them sparkling clean and hygienic.'},
            {'title': 'Window and Mirror Cleaning', 'body': 'We ensure crystal-clear visibility by cleaning windows, mirrors, and glass surfaces with streak-free solutions, enhancing natural light and overall cleanliness.'},
            {'title': 'Final Touches', 'body': 'Before completing the cleaning process, we perform any final touches, such as polishing fixtures, organizing spaces, and adding air fresheners or deodorizers for a pleasant and inviting atmosphere.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Experience the thoroughness of Junk Busters\' move-in/move-out deep cleaning services. Call 615-881-2505 or book online today to schedule your appointment and enjoy a pristine property.',
        'local_areas': ['White House', 'Nashville TN', 'La Vergne', 'Davidson County', 'Robertson County', 'Williamson County', 'Sumner County', 'Wilson County'],
    },

    'recurring-maid-services': {
        'slug': 'recurring-maid-services',
        'title': 'Recurring Maid Services',
        'hero_h1': 'Recurring Maid Services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green',
        'hero_sub': 'Consistent, reliable recurring cleaning plans — weekly, bi-weekly, or monthly — across Middle TN & Southern KY.',
        'meta_desc': 'Recurring maid services in Nashville, White House & Middle Tennessee. Weekly, bi-weekly & monthly cleaning plans from Junk Busters. Call 615-881-2505 for a free quote.',
        'meta_keywords': 'recurring maid services Nashville TN, maid service Nashville Tennessee, weekly cleaning service Nashville, bi-weekly cleaning Nashville, monthly cleaning service Nashville Davidson County',
        'section1_title': 'Consistent Care for a Spotless Home',
        'section1_body': [
            'Keeping a clean home requires ongoing effort. Dust settles on surfaces daily, and floors collect dirt from constant use. Wiping counters, vacuuming carpets, and disinfecting bathrooms takes time, making it difficult to maintain a consistently tidy space. A structured cleaning routine keeps every room fresh, creating a more comfortable living area. Choosing our weekly, bi-weekly, or monthly cleaning services eliminates the hassle of frequent scrubbing and sweeping. We provide organized cleaning visits that prevent dust accumulation, reduce allergens, and keep surfaces germ free.',
            'Using household cleaning products helps, but skipping scheduled maintenance results in stubborn stains and lingering odors. Floors require frequent attention to remove tracked-in debris, and furniture collects dust that affects air quality. With us, you can create a clean home that promotes healthier living, reducing allergens and bacteria that can cause discomfort.',
        ],
        'cards_title': 'Our Recurring Maid Services',
        'yellow_cards': [
            {'title': 'Cooking Area Cleaning', 'body': 'Food preparation leaves behind spills, grease, and crumbs. Over time, these attract bacteria and pests, creating unpleasant odors. Our cleaning methods remove buildup from countertops, sinks, and appliances. Stovetops, cabinet doors, and backsplashes stay free from sticky residue. We also mop and sweep floors to remove dirt.'},
            {'title': 'Restroom Sanitization', 'body': 'Moisture and daily use lead to mold, soap scum, and lingering odors. Our routine cleaning service stops grime from building up on tiles, tubs, and toilets. Surfaces get disinfected to remove bacteria and stains. Mirrors, glass surfaces, and fixtures stay spotless, enhancing the appearance of the space. Also, floors receive thorough scrubbing to eliminate dust and residue.'},
            {'title': 'Living and Bedroom Maintenance', 'body': 'Daily activities cause dust to settle on furniture, shelves, and electronics. We help keep tables, chairs, and decorative items clean and free from fingerprints. Vacuuming carpets and sweeping floors remove dirt, pet hair, and allergens. Our services include organizing cluttered areas to maintain a neat appearance throughout the home.'},
            {'title': 'Floor and Surface Care', 'body': 'Shoes, spills, and daily movement leave floors dirty. Hard surfaces require frequent mopping, and carpets need vacuuming to stay fresh. With our structured cleaning routine, you can preserve floor quality and prevent damage from dirt buildup. Every visit includes thorough care and maintaining cleanliness throughout the home.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'At Junk Busters LLC we value thorough cleaning methods, keeping homes spotless without unnecessary effort from homeowners. Our professionals follow a detailed process, focusing on essential areas that collect dust and grime. Cleaning routines allow residents to enjoy a tidy home without constant maintenance. Communication remains a priority, with clear scheduling options that fit different lifestyles. If you want to learn more about our recurring maid services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, call now.',
        'local_areas': ['White House', 'Nashville TN', 'Goodlettsville', 'Hendersonville', 'Gallatin', 'Springfield', 'Robertson County', 'Davidson County', 'Sumner County', 'Williamson County'],
    },

    'air-duct-cleaning': {
        'slug': 'air-duct-cleaning',
        'title': 'Air Duct Cleaning',
        'hero_h1': 'Air Duct Cleaning Services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green',
        'hero_sub': 'Improve indoor air quality with professional air duct cleaning across Middle TN & Southern KY.',
        'meta_desc': 'Professional air duct cleaning services in Nashville, White House & Middle Tennessee. Junk Busters improves indoor air quality with industry-grade equipment. Call 615-881-2505.',
        'meta_keywords': 'air duct cleaning Nashville TN, duct cleaning Nashville Tennessee, HVAC cleaning Nashville, air duct cleaning White House TN, air quality improvement Nashville Davidson County',
        'section1_title': 'Air Duct Cleaning Services',
        'section1_body': [
            'Your home\'s air duct system plays a critical role in maintaining indoor air quality and HVAC efficiency. Over time, dust, allergens, pet dander, and debris accumulate in ductwork, reducing airflow and circulating pollutants throughout your home. Junk Busters provides professional air duct cleaning services in Middle TN & Southern KY — including Nashville, Clarksville, and Bowling Green, using industry-grade equipment to remove buildup and improve your home\'s air quality.',
            'Regular air duct cleaning helps reduce respiratory irritants, eliminate musty odors, and improve the efficiency of your heating and cooling system. Homes with pets, allergy sufferers, or recent renovation work particularly benefit from thorough duct cleaning.',
            'Our process includes a complete inspection of your duct system, high-powered vacuum extraction, and a final quality check to ensure clean, clear airflow throughout your home.',
        ],
        'cards_title': 'Benefits of Professional Air Duct Cleaning',
        'yellow_cards': [
            {'title': 'Improved Air Quality', 'body': 'Remove dust, pollen, pet dander, mold spores, and other allergens from your duct system, creating cleaner, healthier air for your family.'},
            {'title': 'Better HVAC Efficiency', 'body': 'Clean ducts allow your heating and cooling system to operate at peak efficiency, potentially reducing energy bills and extending system life.'},
            {'title': 'Odor Elimination', 'body': 'Musty smells from mold, mildew, or accumulated debris are eliminated, leaving your home smelling fresh and clean.'},
            {'title': 'Healthier Home Environment', 'body': 'Especially important for households with allergy sufferers, asthma patients, or young children — clean air ducts mean fewer airborne irritants circulating through your living space.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Breathe easier with Junk Busters. Our professional air duct cleaning service uses industry-grade equipment to thoroughly clean your home\'s duct system. Call 615-881-2505 to schedule your appointment today.',
        'local_areas': ['Nashville TN', 'White House', 'Hendersonville', 'Gallatin', 'Goodlettsville', 'Springfield', 'Brentwood', 'Franklin TN', 'Murfreesboro', 'Smyrna'],
    },

    # ── 6 New Service Pages ───────────────────────────────────────────────────

    'estate-hoarder-cleanout': {
        'slug': 'estate-hoarder-cleanout',
        'title': 'Estate & Hoarder Home Cleanouts',
        'hero_h1': 'Estate & Hoarder Home Cleanouts — Middle TN & Southern KY',
        'hero_sub': 'Compassionate probate assistance, senior downsizing, and hoarder home restoration across Nashville, Clarksville & Bowling Green.',
        'meta_desc': 'Compassionate estate & hoarder cleanouts across Middle TN & Southern KY. Probate, senior downsizing, real estate readiness. Free on-site quote. Call 615-881-2505.',
        'meta_keywords': 'probate cleanout Nashville TN, hoarding help Clarksville TN, estate liquidation assistance Bowling Green, hoarder home cleanup Middle Tennessee, estate cleanout Southern KY, senior downsizing Nashville, probate junk removal Robertson County',
        'section1_title': 'A Compassionate Partner for Life\'s Most Difficult Transitions',
        'section1_body': [
            'Dealing with the contents of an estate — whether after the loss of a loved one, a probate proceeding, or a senior downsizing — is one of the most emotionally taxing tasks a family can face. Junk Busters LLC brings a respectful, discreet, and efficient approach to every estate and hoarder home cleanout across Nashville, Clarksville, Bowling Green, and the surrounding Middle TN and Southern KY region.',
            'Hoarder home cleanouts require a specialized mindset. We understand that behind every accumulated space is a person\'s history. Our crew is trained to work with compassion and without judgment, carefully sorting items into categories — keep, donate, recycle, and dispose — based entirely on your direction. We coordinate with local donation centers, recycling facilities, and specialty disposal sites so that every item is handled responsibly.',
            'For probate and estate situations, timing is often critical. Real estate agents need properties cleared and market-ready quickly. We offer priority scheduling, free on-site assessments, and transparent volume-based pricing so there are no surprises. Whether you need a single bedroom cleared or an entire multi-story home emptied, Junk Busters LLC has the crew, the trucks, and the experience to get the job done right.',
        ],
        'cards_title': 'Our Estate & Hoarder Cleanout Services Include',
        'yellow_cards': [
            {'title': 'Probate & Estate Cleanouts', 'body': 'We work directly with executors, attorneys, and family members to clear estate properties on a schedule that matches your probate timeline. Every item is handled with care, and we can document removal for legal purposes upon request.'},
            {'title': 'Hoarder Home Restoration', 'body': 'Our non-judgmental crew specializes in high-volume hoarding situations — from moderate clutter to severe accumulation. We sort, haul, and leave the space broom-clean, ready for the next step whether that\'s deep cleaning, renovation, or listing.'},
            {'title': 'Senior Downsizing Assistance', 'body': 'Moving a parent or grandparent into a smaller home or assisted living facility is stressful. We take the burden off your family by removing unwanted furniture, appliances, and belongings quickly and carefully, making the transition smoother for everyone.'},
            {'title': 'Real Estate Readiness Cleanouts', 'body': 'Need a property listed fast? We clear properties to listing-ready condition so your agent can get photos taken and a sign in the yard. We serve REO agents, estate attorneys, and private sellers across the Nashville–Clarksville–Bowling Green triangle.'},
        ],
        'section2_title': 'Serving the Nashville–Clarksville–Bowling Green Triangle',
        'section2_body': [
            'Junk Busters LLC operates from our Main Dispatch & Fleet in Orlinda, TN and our Nashville Office, giving us quick access to all communities in Middle TN and Southern KY. No job is too far, too large, or too sensitive for our experienced team.',
        ],
        'step_cards': [],
        'trust_body': 'When life brings you to a moment that requires clearing out a loved one\'s home or restoring a property from years of accumulation, Junk Busters LLC is the team you can trust to handle it with professionalism and genuine care. Call 615-881-2505 for a free on-site estimate — we\'ll come to you, assess the property, and provide a transparent quote with no obligation.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Orlinda, TN', 'White House, TN', 'Springfield, TN', 'Gallatin, TN', 'Hendersonville, TN', 'Franklin, KY', 'Russellville, KY'],
    },

    'property-manager-hub': {
        'slug': 'property-manager-hub',
        'title': 'Property Manager Cleanout Services',
        'hero_h1': 'Property Manager Cleanout Services — Middle TN & Southern KY',
        'hero_sub': 'Fast eviction cleanouts and foreclosure trash-outs for landlords, REO agents, and property management companies across Nashville, Clarksville & Bowling Green.',
        'meta_desc': 'Fast eviction cleanouts & foreclosure trash-outs for property managers and REO agents. Nashville, Clarksville & Bowling Green. Reliable scheduling. Call 615-881-2505.',
        'meta_keywords': 'eviction cleanout Nashville TN, foreclosure trash-out Clarksville TN, property management junk removal Bowling Green, REO property cleanout Middle Tennessee, landlord junk removal Nashville, eviction debris removal Southern KY, property manager cleanout service',
        'section1_title': 'Your Reliable Partner for Fast Property Turnovers',
        'section1_body': [
            'Property managers and REO agents across the Nashville–Clarksville–Bowling Green triangle trust Junk Busters LLC for one reason: we show up, we move fast, and we leave properties broom-clean. Whether you\'re dealing with an eviction that left behind furniture and debris, or a bank-owned foreclosure that needs to be market-ready by Friday, we have the crews and the capacity to meet your deadlines.',
            'We understand that every day a unit sits vacant costs you money. That\'s why we offer priority scheduling for property managers, with same-day and next-day service available in most parts of our service area. Our volume-based, transparent pricing means you always know the cost before we start — no surprise invoices, no hidden fees.',
            'We are fully insured, background-checked, and experienced in coordinating with local law enforcement for post-eviction situations. We handle everything from abandoned furniture, appliances, and personal items to construction debris, hazardous materials, and bio-hazard situations in compliance with local health codes. When the job is done, we provide a completion report so you have documentation for your records.',
        ],
        'cards_title': 'Services We Provide to Property Managers',
        'yellow_cards': [
            {'title': 'Post-Eviction Cleanouts', 'body': 'After a tenant leaves — voluntarily or otherwise — we clear the entire unit: furniture, appliances, personal belongings, trash, and debris. We coordinate with local sheriffs when required and document removal for your property management records.'},
            {'title': 'Foreclosure & REO Trash-Outs', 'body': 'Bank-owned and REO properties need to hit the market fast. We provide comprehensive foreclosure trash-outs — furniture, appliances, debris, and abandoned property removal — with completion reports and before/after photos available upon request.'},
            {'title': 'Bulk Debris & Yard Cleanup', 'body': 'Overgrown yards, bulk trash pileups, and outdoor debris left by previous tenants are no problem. We clear exterior areas to make properties presentable for showings and inspections.'},
            {'title': 'Ongoing Property Management Contracts', 'body': 'Managing multiple properties? Ask about our preferred vendor agreements for property management companies. We offer discounted rates and guaranteed response times for clients with recurring cleanout volume.'},
        ],
        'section2_title': 'Why Property Managers Choose Junk Busters LLC',
        'section2_body': [
            'We serve property managers across Davidson, Robertson, Montgomery, and Sumner Counties in TN, as well as Warren and Simpson Counties in KY. Our dual-location operation — Orlinda dispatch and Nashville office — means faster response times across the full service triangle. We bill per volume, not per hour, so your costs are predictable.',
        ],
        'step_cards': [],
        'trust_body': 'Ready to add Junk Busters LLC to your vendor list? Call 615-881-2505 to discuss your portfolio needs and get a free baseline quote. We offer same-day estimates and can often be on-site within 24 hours of your first call.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Orlinda, TN', 'White House, TN', 'Springfield, TN', 'Gallatin, TN', 'Hendersonville, TN', 'Franklin, KY', 'Goodlettsville, TN'],
    },

    'scrap-metal-pickup': {
        'slug': 'scrap-metal-pickup',
        'custom_template': 'website/scrap_metal.html',
        'title': 'Mobile Scrap Metal Pickup & Buying',
        'hero_h1': 'Mobile Scrap Metal Pickup & Buying — Middle TN & Southern KY',
        'hero_sub': 'We come to you — buying copper wire & tubing, aluminum siding & rims, and brass. On-site weighing, fair market prices, immediate payment.',
        'meta_desc': 'We buy copper, aluminum & brass — we come to you. On-site weighing & cash payment in Nashville, Bowling Green & across Middle TN & Southern KY. Call 615-881-2505.',
        'meta_keywords': 'we buy copper Nashville TN, scrap metal pickup Bowling Green KY, mobile scrap yard Orlinda TN, copper wire buyer Clarksville, aluminum pickup Middle Tennessee, scrap metal buying Southern KY, brass buyer Nashville, mobile scrap metal service',
        'section1_title': 'We Come to You — On-Site Scrap Metal Buying Across the Region',
        'section1_body': [
            'Tired of loading up your truck and driving to a scrap yard? Junk Busters LLC brings the scrap yard to you. Our mobile scrap metal pickup service covers Nashville, Clarksville, Bowling Green, and the 50-mile radius around Orlinda, TN — buying copper, aluminum, and brass directly from your home, job site, or business.',
            'Our process is straightforward: you call, we schedule a visit, we weigh your material on-site with certified scales, and we pay you on the spot at current market rates. No hauling, no waiting in scrap yard lines, no lowball offers. Whether you have a few pounds of copper wire from a renovation or a truckload of aluminum siding from a demo project, we make the process fast and transparent.',
            'We buy a wide range of non-ferrous and ferrous scrap metals. Contractors, HVAC companies, electricians, and homeowners across Middle TN and Southern KY rely on us to pick up and purchase their scrap material at competitive prices. We also haul away the scrap as part of our standard junk removal service if you prefer a flat-rate cleanout over cash-per-pound buying.',
        ],
        'cards_title': 'Materials We Buy & Pick Up',
        'yellow_cards': [
            {'title': 'Copper — Wire, Tubing & Pipe', 'body': 'Copper commands the highest scrap prices. We buy bare bright copper wire, #1 and #2 copper, copper tubing, copper pipe, and copper fittings. Common sources include HVAC systems, plumbing renovations, electrical rewiring, and construction demolition.'},
            {'title': 'Aluminum — Siding, Rims & Extrusions', 'body': 'We purchase aluminum siding, aluminum window frames, cast aluminum, aluminum rims/wheels, extruded aluminum, and aluminum cans in bulk. Aluminum is lightweight, plentiful, and consistently valuable at the scrap market.'},
            {'title': 'Brass — Fittings, Valves & Fixtures', 'body': 'Brass plumbing fittings, valves, faucets, doorknobs, and shell casings are all welcome. Brass typically pays at a solid rate per pound and is commonly found in plumbing and HVAC teardowns.'},
            {'title': 'Other Metals & Mixed Loads', 'body': 'We also purchase stainless steel, cast iron, sheet iron, and mixed metal loads. If you\'re unsure what you have, just call — we\'ll identify the material and give you an honest quote before we arrive.'},
        ],
        'section2_title': 'How Our On-Site Scrap Buying Process Works',
        'section2_body': [
            'Step 1 — Call or text us at 615-881-2505 to describe your material and quantity. Step 2 — We schedule a pickup visit at a time that works for you, usually within 24–48 hours. Step 3 — Our crew arrives, identifies and weighs your material on certified portable scales. Step 4 — We quote you a price based on current market rates. Step 5 — You accept, we load, and you get paid on the spot. No hassle, no hauling.',
        ],
        'step_cards': [],
        'trust_body': 'Stop hauling scrap across town. Junk Busters LLC comes to your location anywhere in Middle TN or Southern KY, weighs your material honestly, and pays you fairly. Call 615-881-2505 today to schedule your mobile scrap pickup and get a free estimate on your load.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Orlinda, TN', 'White House, TN', 'Springfield, TN', 'Russellville, KY', 'Franklin, KY', 'Portland, TN', 'Gallatin, TN'],
    },

    'short-term-rental-turnover': {
        'slug': 'short-term-rental-turnover',
        'title': 'Short-Term Rental Turnover Cleaning',
        'hero_h1': 'Short-Term Rental Turnover Cleaning — Middle TN & Southern KY',
        'hero_sub': 'Hotel-ready Airbnb and vacation rental turnovers in Nashville, Clarksville & Bowling Green — fast scheduling, 5-star results.',
        'meta_desc': 'Hotel-ready AirBnB & vacation rental turnover cleaning in Nashville, Clarksville & Bowling Green. Fast scheduling, 5-star results. Call Junk Busters at 615-881-2505.',
        'meta_keywords': 'airbnb cleaning Nashville TN, short-term rental turnover Clarksville TN, vacation rental maid service Bowling Green KY, Airbnb turnover cleaning Middle Tennessee, short-term rental cleaning Southern KY, VRBO cleaning Nashville, 5-star rental cleaning service',
        'section1_title': 'Turnover Cleaning Built for High-Volume Short-Term Rentals',
        'section1_body': [
            'In the short-term rental market, your cleaning team is your most critical operational partner. A slow or sloppy turnover leads to bad reviews, cancelled bookings, and lost revenue. Junk Busters LLC provides specialized turnover cleaning services for Airbnb hosts, VRBO operators, and vacation rental management companies across Nashville, Clarksville, Bowling Green, and the surrounding region.',
            'Our "Hotel-Ready Standard" protocol means every turnover includes a complete room-by-room cleaning, linen changes, restocking of guest supplies (paper products, soaps, coffee), a full kitchen and bathroom sanitization, and a final walkthrough checklist. We can send before/after photos to your phone when the unit is ready so you can flip your calendar and confirm check-in without being on-site.',
            'We integrate with major short-term rental platforms and can sync with your booking calendar so turnovers are automatically scheduled between checkouts and check-ins. Same-day turnovers are available in most areas of our service triangle. Whether you have one rental property or a managed portfolio of 20, we build a cleaning schedule around your occupancy patterns.',
        ],
        'cards_title': 'What\'s Included in Every Turnover',
        'yellow_cards': [
            {'title': 'Full Kitchen Sanitization', 'body': 'Every dish washed and stored, appliances wiped inside and out, countertops sanitized, sink scrubbed, coffee maker cleaned and reset, and trash removed. Guests expect a kitchen that looks untouched — we deliver that standard every time.'},
            {'title': 'Bathroom Deep Clean & Restock', 'body': 'Toilets, showers, and tubs scrubbed and disinfected. Mirrors and glass streak-free. Floors mopped. Towels replaced, toilet paper restocked, soaps and shampoos replenished per your restock kit. A pristine bathroom is the easiest way to earn that 5-star review.'},
            {'title': 'Bedroom Linen Changeover', 'body': 'All beds stripped, linens laundered or swapped from your clean-linen supply, beds made to hotel standards, and pillows arranged. We also check under beds and in nightstands for forgotten items from previous guests.'},
            {'title': 'Walkthrough Checklist & Photo Report', 'body': 'Before we leave, we complete a room-by-room checklist and can send timestamped photos of the completed turnover to your phone or property management platform. You have full visibility without being on-site.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Your guests deserve a hotel-quality experience. Junk Busters LLC delivers exactly that — every turnover, every time. Call 615-881-2505 to schedule your first turnover cleaning and discuss a recurring plan that matches your booking calendar. Serving Nashville, Clarksville, Bowling Green, and the full Middle TN & Southern KY region.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Brentwood, TN', 'Franklin, TN', 'Hendersonville, TN', 'Gallatin, TN', 'Murfreesboro, TN', 'Spring Hill, TN', 'Franklin, KY'],
    },

    'move-out-deep-cleaning': {
        'slug': 'move-out-deep-cleaning',
        'title': 'Move-In / Move-Out Deep Cleaning',
        'hero_h1': 'Move-In / Move-Out Deep Cleaning — Middle TN & Southern KY',
        'hero_sub': 'Stress-free transition cleaning for homeowners, renters, and landlords — appliances, cabinets, baseboards, and every inch in between.',
        'meta_desc': 'Move-out deep cleaning in Clarksville, Nashville & Bowling Green. Appliances, cabinets, baseboards — every inch cleaned. Free estimate. Call 615-881-2505.',
        'meta_keywords': 'move out cleaning Clarksville TN, deep cleaning Nashville TN, apartment turnover cleaning Bowling Green KY, move in cleaning Middle Tennessee, move out deep clean Southern KY, rental property cleaning Nashville, security deposit cleaning Clarksville',
        'section1_title': 'Leave Nothing Behind — or Walk Into Something Spotless',
        'section1_body': [
            'Moving is already stressful. The last thing you need is to lose your security deposit over cleaning — or to move into a home that the previous occupants left in rough shape. Junk Busters LLC provides thorough move-in and move-out deep cleaning services across Clarksville, Nashville, Bowling Green, and Middle TN & Southern KY, designed to meet even the strictest landlord or property management standards.',
            'Our move-out deep cleans go well beyond standard surface cleaning. We clean inside and behind appliances, scrub cabinet interiors, detail baseboards and door frames, remove soap scum and hard water buildup from showers and tubs, clean oven interiors, and wipe down every surface — including light switches, outlet covers, and ceiling fan blades. We do the things that standard cleaning visits skip.',
            'For move-in cleans, we make sure the property is genuinely ready for your arrival — not just "clean enough." We verify that every drawer, cabinet, and closet is wiped out, every appliance interior is clean, and the bathroom is properly sanitized. You should be able to unpack without cleaning first. That\'s the standard we hold ourselves to on every job.',
        ],
        'cards_title': 'What Our Move-Out Deep Clean Covers',
        'yellow_cards': [
            {'title': 'Kitchen — Inside & Out', 'body': 'Oven interior scrubbed and degreased. Refrigerator emptied, wiped, and deodorized. Microwave cleaned inside and out. All cabinet interiors wiped. Countertops and backsplash sanitized. Sink scrubbed. Floor mopped including corners and under appliances.'},
            {'title': 'Bathrooms — Detail Level', 'body': 'Toilet cleaned inside bowl, under rim, and base. Shower and tub scrubbed free of soap scum and hard water deposits. Tile grout cleaned. Mirrors streak-free. Cabinet interiors wiped. Exhaust fan dusted. Floor mopped and baseboards wiped.'},
            {'title': 'Bedrooms & Living Areas', 'body': 'All surfaces dusted including ceiling fan blades, light fixtures, and window sills. Baseboards and door frames wiped. Closet interiors vacuumed and wiped. Carpets vacuumed or hard floors swept and mopped. Window tracks cleaned.'},
            {'title': 'Final Walkthrough & Checklist', 'body': 'Before we leave, we complete a room-by-room checklist covering every item on a standard landlord inspection list. You\'ll know exactly what was cleaned and to what standard — documentation you can use if your deposit is ever disputed.'},
        ],
        'section2_title': None,
        'section2_body': [],
        'step_cards': [],
        'trust_body': 'Whether you\'re moving out and want your full deposit back, or moving in and want a genuinely clean start, Junk Busters LLC delivers a deep clean that passes inspection. Call 615-881-2505 for a free estimate. We serve Clarksville, Nashville, Bowling Green, and the full Middle TN & Southern KY region.',
        'local_areas': ['Clarksville, TN', 'Nashville, TN', 'Bowling Green, KY', 'Orlinda, TN', 'White House, TN', 'Springfield, TN', 'Gallatin, TN', 'Hendersonville, TN', 'Franklin, KY', 'La Vergne, TN'],
    },

    'light-demolition': {
        'slug': 'light-demolition',
        'title': 'Light Demolition — Sheds, Decks & Fences',
        'hero_h1': 'Light Demolition — Sheds, Decks & Fences — Middle TN & Southern KY',
        'hero_sub': 'Safe teardown and immediate hauling of sheds, decks, fences, and hot tubs across Nashville, Clarksville & Bowling Green.',
        'meta_desc': 'Shed demolition, deck teardown, fence removal & hot tub removal across Middle TN & Southern KY. We tear it down and haul it away. Call 615-881-2505.',
        'meta_keywords': 'shed demolition Nashville TN, hot tub removal Clarksville TN, fence removal Bowling Green KY, deck teardown Middle Tennessee, light demolition Southern KY, shed removal Nashville, structure demolition Robertson County, deck removal Clarksville',
        'section1_title': 'Tear It Down, Haul It Away — All in One Visit',
        'section1_body': [
            'Got a rotting shed taking up yard space? A deck that\'s past its prime? A hot tub that hasn\'t worked in years? Junk Busters LLC provides light demolition and removal services across Nashville, Clarksville, Bowling Green, and the full Middle TN & Southern KY region — we tear down the structure and haul every piece away in the same visit.',
            'Our light demolition crews are experienced in safe, controlled teardowns of wood and metal structures. We use professional-grade reciprocating saws, sledgehammers, and demolition tools to break down structures efficiently without damaging surrounding landscaping, fencing, or structures. All debris is loaded directly onto our trucks and hauled to proper disposal or recycling facilities — you don\'t lift a finger.',
            'Hot tub removal is one of our specialties. We safely disconnect electrical connections (we coordinate with a licensed electrician if hardwired), drain the tub, cut it into manageable sections, and haul every piece away. Most hot tub removals are completed in under two hours. We also offer same-day scheduling in many parts of our service area when our calendar allows.',
        ],
        'cards_title': 'Structures We Demo & Remove',
        'yellow_cards': [
            {'title': 'Shed Demolition & Removal', 'body': 'Wood, metal, and vinyl sheds — any size, any condition. We dismantle the structure from the top down, remove the flooring, and haul everything away including any concrete anchors or blocks. Your yard is left clear and level after every shed demo.'},
            {'title': 'Deck Teardown & Hauling', 'body': 'Rotting or damaged decks are a safety hazard. We safely remove all decking boards, framing, posts, and hardware. Attached or freestanding, we handle both. All wood is sorted for recycling or responsible disposal — nothing left behind.'},
            {'title': 'Fence Removal', 'body': 'Wood, chain-link, metal, and vinyl fencing — we remove the panels, rails, and posts. Posts are pulled from the ground (or cut flush if concrete-footed) and the full run is hauled away. We cover full fencelines on residential, rental, and commercial properties.'},
            {'title': 'Hot Tub & Spa Removal', 'body': 'We are hot tub removal specialists across Middle TN and Southern KY. We drain the tub, safely disconnect or cap utility connections, cut the unit into sections, and load it onto our truck. Decks or enclosures surrounding the tub can also be removed in the same visit.'},
        ],
        'section2_title': 'Other Structures We Handle',
        'section2_body': [
            'In addition to sheds, decks, fences, and hot tubs, we also handle swing set and playset removal, pergola and gazebo teardown, carport removal, above-ground pool removal, trampoline removal, and small outbuilding demolition. If it\'s a residential structure that doesn\'t require a permit to remove, we can likely handle it. Call 615-881-2505 and describe your project — we\'ll give you a straight answer and a free estimate.',
        ],
        'step_cards': [],
        'trust_body': 'Junk Busters LLC combines light demolition expertise with our full-service hauling operation — meaning the same crew that tears it down loads it up and drives it away. No subcontractors, no coordination headaches. Call 615-881-2505 for a free on-site estimate anywhere in Nashville, Clarksville, Bowling Green, or the surrounding Middle TN & Southern KY area.',
        'local_areas': ['Nashville, TN', 'Clarksville, TN', 'Bowling Green, KY', 'Orlinda, TN', 'White House, TN', 'Springfield, TN', 'Gallatin, TN', 'Hendersonville, TN', 'Franklin, KY', 'Portland, TN'],
    },
}

CITY_PAGES = {
    'clarksville': {
        'slug': 'junk-removal-clarksville',
        'city_name': 'Clarksville, TN',
        'region_name': 'Montgomery County & the Fort Campbell Area',
        'meta_title': 'Junk Removal Clarksville TN | Junk Busters LLC',
        'meta_desc': 'Junk Busters LLC serves Clarksville, TN with fast junk removal, eviction cleanouts, move-out cleaning, shed demolition & scrap metal pickup. Fort Campbell area specialists. Call 615-881-2505.',
        'meta_keywords': 'junk removal Clarksville TN, eviction cleanout Clarksville, move out cleaning Clarksville TN, shed demolition Clarksville, hot tub removal Clarksville, foreclosure cleanout Montgomery County, junk hauling Fort Campbell area, estate cleanout Clarksville TN',
        'hero_h1': 'Junk Removal & Cleanup Services in Clarksville, TN',
        'hero_sub': 'Serving Fort Campbell, Oak Grove, Hopkinsville & all of Montgomery County. Background-checked crews. Same-day availability. Call 615-881-2505.',
        'area_served': 'Clarksville TN, Montgomery County TN, Fort Campbell KY, Oak Grove KY',
        'intro': [
            'Junk Busters LLC is your trusted junk removal and cleanout company serving Clarksville, TN and the greater Montgomery County area. With Fort Campbell driving constant military relocation, Clarksville sees more PCS moves, rental turnovers, and eviction cleanouts than almost any other city our size — and we are built for exactly that demand.',
            'Whether you are a property manager who needs a fast eviction trash-out, a homeowner clearing out before a PCS move, or a landlord prepping a rental for the next tenant, our background-checked and insured crews arrive on time, work fast, and haul everything away in one trip. No dump runs for you. No hauling heavy furniture down the stairs. We handle it all.',
        ],
        'services': [
            {'name': 'Junk Removal', 'desc': 'Full-service haul-away for furniture, appliances, yard debris, and more. Upfront pricing, no hidden fees.', 'slug': 'junk-removal'},
            {'name': 'Eviction Clean-Out', 'desc': 'Rapid eviction trash-outs for Clarksville landlords and property managers. We clear the unit and haul everything away.', 'slug': 'eviction-clean-out'},
            {'name': 'Foreclosure Clean-Out', 'desc': 'Get foreclosed and bank-owned properties market-ready fast. REO and asset management specialists.', 'slug': 'foreclosure-clean-out'},
            {'name': 'Hot Tub Removal', 'desc': 'Safe disassembly and full removal of hot tubs and spas from any backyard or deck location.', 'slug': 'hot-tub-removal'},
            {'name': 'Light Demolition', 'desc': 'Shed teardown, deck removal, fence demo — we knock it down and haul it away in one visit.', 'slug': 'light-demolition'},
            {'name': 'Move-Out Deep Cleaning', 'desc': 'Security-deposit-ready move-out cleaning for Clarksville apartments, homes, and rental properties.', 'slug': 'move-out-deep-cleaning'},
            {'name': 'Mobile Scrap Metal Pickup', 'desc': 'We come to you and pay cash on the spot for copper, aluminum, and brass. No trips to the yard.', 'slug': 'scrap-metal-pickup'},
            {'name': 'Estate Clean-Out', 'desc': 'Compassionate full-estate clearing for probate, senior downsizing, and real estate readiness in Clarksville.', 'slug': 'estate-clean-out'},
        ],
        'trust_body': "Junk Busters LLC is Middle TN & Southern KY's dependable cleanout crew. We've served hundreds of Clarksville homeowners, landlords, and property managers with fast turnarounds and upfront pricing. Military families, real estate agents, and property management companies trust us to get the job done right the first time. Give us a call and we'll have a crew out to you in no time.",
        'local_areas': ['Clarksville, TN', 'Fort Campbell, KY', 'Oak Grove, KY', 'Hopkinsville, KY', 'Cunningham, TN', 'Pembroke, KY', 'Southside, TN', 'Woodlawn, TN', 'Adams, TN', 'Erin, TN', 'Sango, TN', 'Pleasant View, TN'],
    },
    'bowling-green': {
        'slug': 'junk-removal-bowling-green',
        'city_name': 'Bowling Green, KY',
        'region_name': 'Warren County & Southern Kentucky',
        'meta_title': 'Junk Removal Bowling Green KY | Junk Busters LLC',
        'meta_desc': 'Junk Busters LLC serves Bowling Green, KY with professional junk removal, estate cleanouts, eviction cleanouts, hot tub removal & scrap metal buying. Warren County specialists. Call 615-881-2505.',
        'meta_keywords': 'junk removal Bowling Green KY, estate cleanout Bowling Green, eviction cleanout Warren County KY, hot tub removal Bowling Green, scrap metal pickup Bowling Green KY, junk hauling Southern Kentucky, garage cleanout Bowling Green',
        'hero_h1': 'Junk Removal & Cleanout Services in Bowling Green, KY',
        'hero_sub': "Serving Warren County, Franklin KY, Scottsville & all of Southern Kentucky. Fast, reliable, fully insured. Call 615-881-2505.",
        'area_served': 'Bowling Green KY, Warren County KY, Simpson County KY, Logan County KY',
        'intro': [
            "Junk Busters LLC brings professional junk removal and cleanout services to Bowling Green, KY and the entire Southern Kentucky region. As one of the few regional companies actively serving Warren County with a dedicated presence, we offer Bowling Green residents and businesses something the big national franchises can't: a local crew that knows the area, arrives on time, and charges a fair flat rate.",
            "Bowling Green's growing rental market, Western Kentucky University's student housing turnover, and an active real estate scene create consistent demand for fast, reliable cleanout services. Whether you're clearing an estate in Alvaton, hauling junk from a storage unit on Scottsville Road, or need a move-out deep clean before handing back the keys, Junk Busters is your crew.",
        ],
        'services': [
            {'name': 'Junk Removal', 'desc': 'Full-service junk haul-away for Bowling Green homes, businesses, and rental properties. Upfront pricing.', 'slug': 'junk-removal'},
            {'name': 'Estate Clean-Out', 'desc': 'Compassionate estate clearing for probate, senior downsizing, and real estate readiness in Warren County.', 'slug': 'estate-clean-out'},
            {'name': 'Eviction Clean-Out', 'desc': 'Rapid eviction trash-outs for Bowling Green landlords and property managers. We turn units over fast.', 'slug': 'eviction-clean-out'},
            {'name': 'Garage Clean-Out', 'desc': 'Reclaim your garage or storage space — we remove everything you no longer need, quickly and cleanly.', 'slug': 'garage-clean-out'},
            {'name': 'Hot Tub Removal', 'desc': 'Safe disassembly and disposal of hot tubs and spas anywhere in Warren County and beyond.', 'slug': 'hot-tub-removal'},
            {'name': 'Mobile Scrap Metal Pickup', 'desc': 'We buy copper, aluminum & brass — we come to your Bowling Green location and pay cash on site.', 'slug': 'scrap-metal-pickup'},
            {'name': 'Move-Out Deep Cleaning', 'desc': 'Security-deposit-ready move-out cleaning for Bowling Green apartments, houses, and student rentals.', 'slug': 'move-out-deep-cleaning'},
            {'name': 'Light Demolition', 'desc': 'Shed teardown, deck removal, fence demo in the Bowling Green area — we haul it away in one trip.', 'slug': 'light-demolition'},
        ],
        'trust_body': "Junk Busters LLC is proud to be one of the few regional hauling companies that genuinely serves Bowling Green and Southern Kentucky — not just lists it as a service area. Our crews make the drive. Our pricing is upfront. And our work speaks for itself. Call 615-881-2505 for a free estimate and we'll get a crew out to you fast.",
        'local_areas': ['Bowling Green, KY', 'Franklin, KY', 'Scottsville, KY', 'Russellville, KY', 'Alvaton, KY', 'Oakland, KY', 'Smiths Grove, KY', 'Lewisburg, KY', 'Auburn, KY', 'Rockfield, KY', 'Plano, KY', 'Woodburn, KY'],
    },
    'kentucky': {
        'slug': 'kentucky',
        'city_name': 'Southern Kentucky',
        'region_name': 'Southern Kentucky — Warren, Simpson, Logan & Allen Counties',
        'meta_title': 'Junk Removal Southern Kentucky | Junk Busters LLC',
        'meta_desc': 'Junk Busters LLC serves all of Southern Kentucky — Bowling Green, Franklin, Russellville, Scottsville & beyond. Junk removal, estate cleanouts, scrap metal buying & more. Call 615-881-2505.',
        'meta_keywords': 'junk removal Kentucky, junk removal Southern KY, junk removal Warren County KY, junk removal Simpson County KY, cleanout services Logan County KY, junk hauling Allen County KY, estate cleanout Bowling Green, scrap metal pickup Kentucky',
        'hero_h1': "Junk Busters Kentucky — Southern KY's Junk Removal & Cleanout Company",
        'hero_sub': 'Serving Warren, Simpson, Logan & Allen Counties — Bowling Green, Franklin, Russellville & beyond. Fully insured. Call 615-881-2505.',
        'area_served': 'Southern Kentucky — Warren County, Simpson County, Logan County, Allen County',
        'intro': [
            "Junk Busters LLC is the Nashville–Clarksville–Bowling Green triangle's most versatile junk removal and cleanout company, and we actively serve all of Southern Kentucky. From Bowling Green in Warren County to Franklin in Simpson County, Russellville in Logan County, and Scottsville in Allen County — our crews make the drive so you don't have to haul it yourself.",
            "Southern Kentucky has historically been underserved by professional junk removal and property cleanout companies. The big national franchises rarely travel this far. Junk Busters was built differently. Headquartered in Orlinda, TN — just south of the Kentucky state line — we've been serving KY customers since day one. We know the roads, we know the communities, and we're committed to showing up.",
        ],
        'services': [
            {'name': 'Junk Removal', 'desc': 'We haul it all — furniture, appliances, yard debris, mattresses & more. Flat-rate pricing, no hidden fees.', 'slug': 'junk-removal'},
            {'name': 'Estate Clean-Out', 'desc': 'Full estate clearing for probate, senior downsizing, and real estate readiness across Southern KY.', 'slug': 'estate-clean-out'},
            {'name': 'Eviction Clean-Out', 'desc': 'Fast eviction trash-outs for Kentucky landlords and property managers. We turn units over quickly.', 'slug': 'eviction-clean-out'},
            {'name': 'Foreclosure Clean-Out', 'desc': 'REO and bank-owned property cleanouts across Warren, Simpson, Logan & Allen Counties.', 'slug': 'foreclosure-clean-out'},
            {'name': 'Hot Tub Removal', 'desc': 'Safe hot tub and spa disassembly and removal anywhere in Southern Kentucky.', 'slug': 'hot-tub-removal'},
            {'name': 'Mobile Scrap Metal Pickup', 'desc': 'We buy copper, aluminum & brass — we come to your Kentucky location and pay cash on site.', 'slug': 'scrap-metal-pickup'},
            {'name': 'Light Demolition', 'desc': 'Shed demolition, deck teardown, fence removal across Southern KY. We haul it away in one trip.', 'slug': 'light-demolition'},
            {'name': 'Garage Clean-Out', 'desc': 'Garage and storage unit cleanouts for Southern KY homeowners. Fast scheduling, flat-rate pricing.', 'slug': 'garage-clean-out'},
        ],
        'trust_body': "Junk Busters LLC is based right at the Tennessee–Kentucky border in Orlinda, TN — which makes us genuinely local to Southern Kentucky in a way that Nashville-based companies simply aren't. We serve Warren, Simpson, Logan, and Allen Counties with the same professionalism, speed, and fair pricing we bring to every job across Middle TN. Call 615-881-2505 for a free estimate.",
        'local_areas': ['Bowling Green, KY', 'Franklin, KY', 'Russellville, KY', 'Scottsville, KY', 'Adairville, KY', 'Auburn, KY', 'Lewisburg, KY', 'Smiths Grove, KY', 'Oakland, KY', 'Alvaton, KY', 'Morgantown, KY', 'Woodburn, KY'],
    },
}

ADDITIONAL_SERVICES = [
    {'name': 'Move In/Move Out Cleaning', 'desc': 'Thorough cleaning for new or vacated homes, making every space spotless.', 'icon': '🏠'},
    {'name': 'Recurring Maid Services', 'desc': 'Weekly, bi-weekly, or monthly cleaning plans tailored to your schedule.', 'icon': '🧹'},
    {'name': 'Fence Removal', 'desc': 'We dismantle and haul away old wood, chain-link, or metal fencing.', 'icon': '🔧'},
    {'name': 'Estate Clean-Out', 'desc': "Full estate clearing done with care and respect during life's big transitions.", 'icon': '🏡'},
    {'name': 'Eviction Clean-Out', 'desc': 'Rapid property cleanouts for landlords needing units turned around fast.', 'icon': '🔑'},
    {'name': 'Foreclosure Clean-Out', 'desc': 'Professional clean-out service to get foreclosed properties market-ready.', 'icon': '📋'},
    {'name': 'Bulk Cardboard Removal', 'desc': 'Eco-friendly cardboard pickup and recycling for businesses and homes.', 'icon': '📦'},
    {'name': 'Garage Clean-Out', 'desc': 'Reclaim your garage — we haul away everything you no longer need.', 'icon': '🚗'},
    {'name': 'Storage Unit Clean-Out', 'desc': 'Help clearing storage units efficiently to save you time and money.', 'icon': '🗄️'},
    {'name': 'Hot Tub Removal', 'desc': 'Safe disassembly and removal of old hot tubs and spas.', 'icon': '♨️'},
]

ALL_SERVICES = [
    {'name': 'Junk Removal', 'desc': 'We haul away furniture, appliances, yard debris, mattresses, and more. Upfront pricing with no hidden fees.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>', 'slug': 'junk-removal'},
    {'name': 'Residential Cleaning', 'desc': 'Deep cleaning for homes of all sizes. We leave every room spotless and fresh.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>', 'slug': 'residential-cleaning'},
    {'name': 'Move In/Move Out Cleaning', 'desc': 'Thorough move-in or move-out cleaning so your property is ready for its next chapter.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M5 12H3l9-9 9 9h-2"/><path d="M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/><path d="M10 22v-6h4v6"/></svg>', 'slug': 'move-in-move-out-cleaning'},
    {'name': 'Recurring Maid Services', 'desc': 'Flexible weekly, bi-weekly, or monthly cleaning plans to keep your home in top shape.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01z"/></svg>', 'slug': 'recurring-maid-services'},
    {'name': 'Air BnB Cleaning', 'desc': 'Keep your short-term rental spotless and guest-ready between every booking.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M2 7h20v13a2 2 0 01-2 2H4a2 2 0 01-2-2V7z"/><path d="M2 7a5 5 0 015-5h10a5 5 0 015 5"/><line x1="12" y1="12" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>', 'slug': 'air-bnb-cleaning'},
    {'name': 'Fence Removal', 'desc': 'Old wood, chain-link, or metal fencing — we dismantle and haul it all away.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><line x1="4" y1="4" x2="4" y2="20"/><line x1="12" y1="4" x2="12" y2="20"/><line x1="20" y1="4" x2="20" y2="20"/><line x1="2" y1="8" x2="22" y2="8"/><line x1="2" y1="16" x2="22" y2="16"/></svg>', 'slug': 'fence-removal'},
    {'name': 'Estate Clean-Out', 'desc': "Complete estate clearing done with care and efficiency during life's big transitions.", 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>', 'slug': 'estate-clean-out'},
    {'name': 'Eviction Clean-Out', 'desc': 'Rapid clean-outs for landlords needing units turned over quickly and professionally.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 11-7.778 7.778 5.5 5.5 0 017.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>', 'slug': 'eviction-clean-out'},
    {'name': 'Foreclosure Clean-Out', 'desc': 'Get foreclosed properties market-ready with our efficient, thorough clean-out service.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>', 'slug': 'foreclosure-clean-out'},
    {'name': 'Bulk Cardboard Removal', 'desc': 'We pick up and recycle bulk cardboard for businesses and homes — eco-friendly disposal.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>', 'slug': 'bulk-cardboard-removal'},
    {'name': 'Garage Clean-Out', 'desc': 'Reclaim your garage space — we remove everything you no longer need, quickly and cleanly.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><rect x="1" y="3" width="15" height="13" rx="1"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>', 'slug': 'garage-clean-out'},
    {'name': 'Storage Unit Clean-Out', 'desc': 'Clear out storage units efficiently, saving you time and avoiding extra rental fees.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><rect x="2" y="7" width="20" height="14" rx="1"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/><line x1="12" y1="12" x2="12" y2="16"/><line x1="10" y1="14" x2="14" y2="14"/></svg>', 'slug': 'storage-unit-clean-out'},
    {'name': 'Hot Tub Removal', 'desc': 'Safe disassembly and full removal of old hot tubs and spas from any location.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M9 6c0-1.1.9-2 2-2h2a2 2 0 012 2v1H9V6z"/><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M7 12c1-1.5 3-1.5 4 0s3 1.5 4 0"/></svg>', 'slug': 'hot-tub-removal'},
    {'name': 'Estate & Hoarder Cleanouts', 'desc': 'Compassionate probate assistance, senior downsizing, and hoarder home restoration. Real estate readiness included.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>', 'slug': 'estate-hoarder-cleanout'},
    {'name': 'Property Manager Hub', 'desc': 'Fast eviction cleanouts and foreclosure trash-outs for landlords, REO agents, and property management companies.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>', 'slug': 'property-manager-hub'},
    {'name': 'Mobile Scrap Metal Buying', 'desc': 'We come to you — buying copper, aluminum, and brass with on-site weighing and immediate payment.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>', 'slug': 'scrap-metal-pickup'},
    {'name': 'Short-Term Rental Turnover', 'desc': 'Hotel-ready Airbnb and vacation rental turnovers with photo reports and calendar-synced scheduling.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M2 7h20v13a2 2 0 01-2 2H4a2 2 0 01-2-2V7z"/><path d="M2 7a5 5 0 015-5h10a5 5 0 015 5"/><line x1="12" y1="12" x2="12" y2="17"/><line x1="9" y1="14" x2="15" y2="14"/></svg>', 'slug': 'short-term-rental-turnover'},
    {'name': 'Move-Out Deep Cleaning', 'desc': 'Thorough move-in/move-out cleaning — appliances, cabinets, baseboards, and every inch. Security-deposit ready.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><path d="M5 12H3l9-9 9 9h-2"/><path d="M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/><path d="M10 22v-6h4v6"/></svg>', 'slug': 'move-out-deep-cleaning'},
    {'name': 'Light Demolition', 'desc': 'Shed demolition, deck teardown, fence removal, and hot tub removal — we tear it down and haul it away in one visit.', 'icon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="44" height="44"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>', 'slug': 'light-demolition'},
]

SERVICE_AREAS = [
    'White House, TN', 'Nashville, TN', 'Gallatin, TN', 'Hendersonville, TN',
    'Goodlettsville, TN', 'Springfield, TN', 'Greenbrier, TN', 'Millersville, TN',
    'Cottontown, TN', 'Portland, TN', 'Orlinda, TN',
]


# ── Views ─────────────────────────────────────────────────────────────────────

def home(request):
    return render(request, 'website/home.html', {
        'additional_services': ADDITIONAL_SERVICES,
        'service_areas': SERVICE_AREAS,
        'reviews': REVIEWS,
    })


def services(request):
    return render(request, 'website/services.html', {'all_services': ALL_SERVICES})


def service_page(request, slug):
    svc = SERVICES.get(slug)
    if not svc:
        raise Http404
    template = svc.get('custom_template', 'website/service_detail.html')
    return render(request, template, {'svc': svc})


def city_clarksville(request):
    return render(request, 'website/city_landing.html', {'city': CITY_PAGES['clarksville']})


def city_bowling_green(request):
    return render(request, 'website/city_landing.html', {'city': CITY_PAGES['bowling-green']})


def city_kentucky(request):
    return render(request, 'website/city_landing.html', {'city': CITY_PAGES['kentucky']})


@require_http_methods(['GET', 'POST'])
def quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            try:

                BookingRequest.objects.create(
                    first_name=d['first_name'],
                    last_name=d.get('last_name') or '.',
                    email=d['email'],
                    phone=d['phone'],
                    service_requested=d['service_type'] + ((' — ' + d['description']) if d.get('description') else ''),
                    address=d.get('address', ''),
                    city=d.get('city', ''),
                    state=d.get('state', ''),
                    zip_code=d.get('zip_code', ''),
                    notes=d.get('description', ''),
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
            return redirect('website:quote_success')
    else:
        service_pre = request.GET.get('service', '')
        form = QuoteForm(initial={'service_type': service_pre} if service_pre else {})
    return render(request, 'website/quote.html', {'form': form})


def quote_success(request):
    return render(request, 'website/success.html', {
        'title': 'Quote Request Received!',
        'message': "Thanks! We'll review your request and reach out within 1 business day.",
        'cta_text': 'Back to Home',
        'cta_url': '/',
    })


@require_http_methods(['GET', 'POST'])
def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            try:

                BookingRequest.objects.create(
                    first_name=d['first_name'],
                    last_name=d['last_name'],
                    email=d['email'],
                    phone=d['phone'],
                    service_requested=d['service_type'],
                    address=d.get('address', ''),
                    city=d.get('city', ''),
                    state=d.get('state', ''),
                    zip_code=d.get('zip_code', ''),
                    preferred_date=d.get('preferred_date'),
                    preferred_time=d.get('preferred_time', ''),
                    notes=d.get('notes', ''),
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
            return redirect('website:booking_success')
    else:
        form = BookingForm()
    return render(request, 'website/booking.html', {'form': form})


def booking_success(request):
    return render(request, 'website/success.html', {
        'title': 'Booking Request Submitted!',
        'message': "We've received your booking request. Our team will confirm your appointment shortly.",
        'cta_text': 'Back to Home',
        'cta_url': '/',
    })


def areas(request):
    all_areas = [
        {'county': 'Davidson County', 'cities': ['Nashville', 'Antioch', 'Bellevue', 'Donelson', 'Hermitage', 'Madison', 'Goodlettsville']},
        {'county': 'Robertson County', 'cities': ['Springfield', 'White House', 'Greenbrier', 'Orlinda', 'Millersville', 'Cottontown', 'Cedar Hill']},
        {'county': 'Sumner County', 'cities': ['Gallatin', 'Hendersonville', 'Portland', 'Westmoreland', 'White House', 'Bethpage', 'Cottontown']},
        {'county': 'Williamson County', 'cities': ['Franklin', 'Brentwood', 'Spring Hill', 'Nolensville', 'Thompson\'s Station', 'Fairview', 'College Grove']},
        {'county': 'Wilson County', 'cities': ['Lebanon', 'Mt. Juliet', 'Watertown', 'Gladeville', 'La Vergne (border)']},
        {'county': 'Rutherford County', 'cities': ['Murfreesboro', 'Smyrna', 'La Vergne', 'Eagleville', 'Lavergne']},
        {'county': 'Cheatham County', 'cities': ['Ashland City', 'Kingston Springs', 'Pegram', 'Pleasant View', 'Chapmansboro']},
        {'county': 'Montgomery County', 'cities': ['Clarksville', 'Oak Grove KY', 'Cunningham', 'Pembroke', 'Southside']},
    ]
    return render(request, 'website/areas.html', {
        'all_areas': all_areas,
        'primary_areas': SERVICE_AREAS_PRIMARY,
        'secondary_areas': SERVICE_AREAS_SECONDARY,
    })


def gallery(request):
    gallery_items = [
        {'icon': '🚛'}, {'icon': '🗑️'}, {'icon': '🏠'},
        {'icon': '🔧'}, {'icon': '📦'}, {'icon': '🧹'},
        {'icon': '🏡'}, {'icon': '🚗'}, {'icon': '🗄️'},
        {'icon': '♨️'}, {'icon': '🌿'}, {'icon': '📋'},
        {'icon': '🛋️'}, {'icon': '🔑'}, {'icon': '💨'},
    ]
    return render(request, 'website/gallery.html', {'gallery_items': gallery_items})


def contact(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and (phone or email):
            try:

                parts = name.split(' ', 1)
                BookingRequest.objects.create(
                    first_name=parts[0],
                    last_name=parts[1] if len(parts) > 1 else '.',
                    email=email or 'noemail@provided.com',
                    phone=phone or '',
                    service_requested='Contact form inquiry',
                    notes=message,
                    ip_address=request.META.get('REMOTE_ADDR'),
                )
            except Exception:
                pass
            success = True
    return render(request, 'website/contact.html', {'success': success})


def sitemap(request):
    slugs = list(SERVICES.keys())
    city_slugs = [p['slug'] for p in CITY_PAGES.values()]
    return render(request, 'website/sitemap.xml', {'slugs': slugs, 'city_slugs': city_slugs}, content_type='application/xml')


def robots(request):
    content = "User-agent: *\nAllow: /\nSitemap: https://www.junkbustershauling.com/sitemap.xml\n"
    return HttpResponse(content, content_type='text/plain')
