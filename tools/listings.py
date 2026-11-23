# ============================================================================
#  LISTINGS — edit this file to add, change or remove homes.
# ============================================================================
#  Each listing is one { ... } block. Copy a block to add a new home.
#
#  slug        web address of the listing page (lowercase, dashes, unique)
#  status      "For Sale", "Pending", "Sold" or "Coming Soon"
#  sample      True = demonstration listing (shows a "Sample listing" label and is
#              hidden from Google). Set to False ONLY for real homes you represent.
#  price       number, no $ or commas
#  type        "Single-family", "Condo", "Townhome", "Patio home", "Cottage"
#  single_level  True if all main living (bedroom, bath, kitchen) is on one floor
#  community_55  True only if the home is in a qualified 55+ community (HOPA)
#  hoa         monthly HOA fee in dollars (0 if none)
#  photos      list of photos. Either an Unsplash photo ID (the part after "photo-"
#              in an images.unsplash.com address) or a file you saved in
#              site/assets/img/listings/, written as "local:filename.jpg"
#  mls         MLS number (leave "" for sample listings)
# ============================================================================

LISTINGS = [
  {
    "slug": "single-level-ranch-3-bed",
    "status": "For Sale", "sample": True,
    "title": "Single-Level Ranch with Main-Floor Primary Suite",
    "street": "100 Sample Lane", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Sample neighborhood",
    "price": 389000, "beds": 3, "baths": 2, "sqft": 1650, "lot": "0.24 acre", "year": 1998, "garage": "2-car attached",
    "type": "Single-family", "single_level": True, "community_55": False, "hoa": 0,
    "photos": ["1568605114967-8130f3a36994", "1556912173-3bb406ef7e77", "1502672260266-1c1ef2d93688"],
    "summary": "Everything on one level: an open living area, a bright kitchen, and a primary suite with a walk-in shower, all with a no-step entry from the garage.",
    "description": [
      "This sample listing shows how a home is presented on the site. Replace this text with the real description from the listing agent.",
      "Picture a comfortable ranch home with all main living on one floor. The open living and dining area flows into a kitchen with plenty of counter space, and sliding doors open to a covered patio overlooking a level backyard.",
      "The primary suite sits on the quiet side of the home, with a walk-in closet and a bathroom with a low-threshold shower. Two more bedrooms are perfect for guests, a hobby room, or a home office.",
    ],
    "features": ["No-step entry from the garage", "Primary suite on the main level", "Walk-in shower with grab bar", "Wide hallways and doorways", "Covered back patio", "Level, low-maintenance yard", "Laundry on the main floor", "2-car attached garage"],
    "mls": "",
  },
  {
    "slug": "elevator-condo-2-bed",
    "status": "For Sale", "sample": True,
    "title": "Two-Bedroom Condo in an Elevator Building",
    "street": "200 Sample Avenue, Unit 4B", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Downtown",
    "price": 259000, "beds": 2, "baths": 2, "sqft": 1180, "lot": "N/A", "year": 2006, "garage": "1 assigned covered space",
    "type": "Condo", "single_level": True, "community_55": False, "hoa": 385,
    "photos": ["1522708323590-d24dbb6b0267", "1502672260266-1c1ef2d93688", "1556912173-3bb406ef7e77"],
    "summary": "Lock-and-leave living near shops and restaurants, with an elevator, secured entry, and exterior maintenance covered by the HOA.",
    "description": [
      "This sample listing shows how a condo is presented on the site. Replace this text with the real description from the listing agent.",
      "Imagine coming home to a bright fourth-floor condo with an elevator from the parking level to your door. The open living room and kitchen share large windows, and a private balcony is just right for morning coffee.",
      "Two bedrooms each have their own bathroom, and an in-unit laundry closet means no carrying baskets down the hall. The HOA covers exterior maintenance, landscaping, water, and trash, so you can travel with peace of mind.",
    ],
    "features": ["Elevator access from parking", "Secured building entry", "In-unit washer and dryer", "Private balcony", "Two full bathrooms", "HOA covers exterior, water and trash", "Walk to shops and dining", "Assigned covered parking"],
    "mls": "",
  },
  {
    "slug": "55-plus-patio-home",
    "status": "For Sale", "sample": True,
    "title": "Patio Home in a 55+ Community",
    "street": "300 Sample Court", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Sample 55+ community",
    "price": 315000, "beds": 2, "baths": 2, "sqft": 1420, "lot": "0.12 acre", "year": 2012, "garage": "2-car attached",
    "type": "Patio home", "single_level": True, "community_55": True, "hoa": 210,
    "photos": ["1570129477492-45c003edd2be", "1600607687939-ce8a6c25118c", "1556912173-3bb406ef7e77"],
    "summary": "Low-maintenance living in an age-qualified community, with lawn care included and a clubhouse, pool, and walking paths nearby.",
    "description": [
      "This sample listing shows how a home in a 55+ community is presented on the site. Replace this text with the real description from the listing agent.",
      "Patio homes offer the privacy of a detached home with the ease of a maintained community. This one has an open floor plan, a sunroom that fills with morning light, and a kitchen with a breakfast bar.",
      "The community HOA takes care of lawn mowing and snow removal, and residents enjoy a clubhouse, heated pool, and miles of walking paths. Community age requirements and rules apply; ask the agent for the HOA documents.",
    ],
    "features": ["Age-qualified 55+ community", "Lawn care and snow removal included", "Clubhouse, pool and walking paths", "Sunroom", "Single-level floor plan", "Zero-threshold front entry", "Comfort-height toilets", "2-car attached garage"],
    "mls": "",
  },
  {
    "slug": "townhome-first-floor-primary",
    "status": "Pending", "sample": True,
    "title": "Townhome with First-Floor Primary Bedroom",
    "street": "400 Sample Way", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Sample neighborhood",
    "price": 349000, "beds": 3, "baths": 2.5, "sqft": 1890, "lot": "0.06 acre", "year": 2015, "garage": "2-car attached",
    "type": "Townhome", "single_level": False, "community_55": False, "hoa": 165,
    "photos": ["1600585154340-be6161a56a0c", "1600607687939-ce8a6c25118c", "1522708323590-d24dbb6b0267"],
    "summary": "Main-floor living with the primary bedroom downstairs, plus two upstairs bedrooms for visiting family.",
    "description": [
      "This sample listing shows how a pending sale is presented on the site. Replace this text with the real description from the listing agent.",
      "This townhome keeps daily life on the first floor: the kitchen, living room, laundry, and primary bedroom with its own bathroom are all on the main level. Upstairs, two bedrooms and a full bath are ready for grandchildren and guests.",
      "The HOA handles exterior maintenance and landscaping, and a small private patio is perfect for container gardening.",
    ],
    "features": ["Primary bedroom on the first floor", "Main-floor laundry", "Two guest bedrooms upstairs", "Private patio", "HOA covers exterior and landscaping", "2-car attached garage"],
    "mls": "",
  },
  {
    "slug": "cottage-bungalow-2-bed",
    "status": "For Sale", "sample": True,
    "title": "Charming Cottage Bungalow Close to Town",
    "street": "500 Sample Street", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Historic district",
    "price": 229000, "beds": 2, "baths": 1, "sqft": 980, "lot": "0.15 acre", "year": 1948, "garage": "Detached 1-car",
    "type": "Cottage", "single_level": True, "community_55": False, "hoa": 0,
    "photos": ["1580587771525-78b9dba3b914", "1502672260266-1c1ef2d93688", "1556912173-3bb406ef7e77"],
    "summary": "A cozy, right-sized home with a front porch, hardwood floors, and a garden, within walking distance of the library and coffee shops.",
    "description": [
      "This sample listing shows how a smaller home is presented on the site. Replace this text with the real description from the listing agent.",
      "Downsizing does not have to mean giving up character. This cottage has a classic front porch, original hardwood floors, and built-in shelves in the living room.",
      "The updated kitchen has a sunny breakfast nook, and the fenced backyard has raised garden beds. Everything you need is on one floor.",
    ],
    "features": ["Front porch", "Hardwood floors", "Updated kitchen", "Raised garden beds", "Fenced backyard", "Single-level living", "Walk to town"],
    "mls": "",
  },
  {
    "slug": "family-home-4-bed-sold",
    "status": "Sold", "sample": True,
    "title": "Four-Bedroom Family Home (Sold)",
    "street": "600 Sample Drive", "city": "Your City", "state": "ST", "zip": "00000", "neighborhood": "Sample neighborhood",
    "price": 529000, "beds": 4, "baths": 3, "sqft": 2650, "lot": "0.31 acre", "year": 1994, "garage": "3-car attached",
    "type": "Single-family", "single_level": False, "community_55": False, "hoa": 0,
    "photos": ["1512917774080-9991f1c4c750", "1600607687939-ce8a6c25118c", "1556912173-3bb406ef7e77"],
    "summary": "An example of a sold listing: the family home our sellers raised their children in, sold so they could move closer to their grandchildren.",
    "description": [
      "This sample listing shows how a sold home is presented on the site. Replace this text with a real past sale, with the seller’s permission.",
      "Sold listings show visitors that you help people at every stage, including selling the larger family home before moving to something smaller.",
    ],
    "features": ["Four bedrooms", "Large backyard", "3-car garage", "Finished basement"],
    "mls": "",
  },
]
