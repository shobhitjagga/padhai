"""
Broad NCERT curriculum knowledge bank for LLM judge context injection.
Covers grades 3-12 for the subjects that appear in the evaluation dataset.
"""

# ── Class 9 Science ───────────────────────────────────────────────────────────────

SCIENCE_9 = {
    "chapters": [
        "Ch1: Matter in Our Surroundings",
        "Ch2: Is Matter Around Us Pure?",
        "Ch3: Atoms and Molecules",
        "Ch4: Structure of the Atom",
        "Ch5: The Fundamental Unit of Life (Cell)",
        "Ch6: Tissues",
        "Ch7: Diversity in Living Organisms",
        "Ch8: Motion",
        "Ch9: Force and Laws of Motion",
        "Ch10: Gravitation",
        "Ch11: Work and Energy",
        "Ch12: Sound",
        "Ch13: Why Do We Fall Ill?",
        "Ch14: Natural Resources",
        "Ch15: Improvement in Food Resources",
    ],
    "motion": {
        "chapter": "Ch8: Motion",
        "definitions": [
            "Distance: total path length covered (scalar quantity)",
            "Displacement: shortest distance from initial to final position with direction (vector)",
            "Speed = Distance / Time (scalar, SI unit: m/s)",
            "Velocity = Displacement / Time (vector, SI unit: m/s)",
            "Acceleration = Change in velocity / Time taken (m/s², vector)",
            "Uniform motion: equal distances in equal intervals of time",
            "Non-uniform motion: unequal distances in equal intervals of time",
        ],
        "equations_of_motion": [
            "1st: v = u + at",
            "2nd: s = ut + ½at²",
            "3rd: v² = u² + 2as",
            "(u = initial velocity, v = final velocity, a = acceleration, s = displacement, t = time)",
        ],
        "graphs": [
            "Distance-time graph: slope = speed; straight line = uniform motion",
            "Velocity-time graph: slope = acceleration; area under curve = displacement",
        ],
        "critical_flags": [
            "Distance ≠ displacement — displacement can be zero or negative",
            "Speed ≠ velocity — velocity has direction",
            "Equations of motion ONLY valid for uniform (constant) acceleration",
            "A body moving in a circle at constant speed has non-uniform velocity (direction changes)",
        ],
    },
    "gravitation": {
        "chapter": "Ch10: Gravitation",
        "definitions": [
            "Universal Law of Gravitation: F = Gm₁m₂/r² (every object attracts every other object)",
            "G (Universal Gravitational Constant) = 6.674 × 10⁻¹¹ N m²/kg²",
            "g (acceleration due to gravity on Earth's surface) = 9.8 m/s²",
            "Weight W = mg (unit: Newton N) — varies with location/planet",
            "Mass (unit: kg) — constant everywhere in the universe",
            "Free fall: object falling under gravity alone; acceleration = g downward",
            "Buoyancy: upward force exerted by a fluid on a submerged object",
            "Archimedes' Principle: buoyant force = weight of fluid displaced by object",
            "Relative density = density of substance / density of water (dimensionless)",
        ],
        "critical_flags": [
            "Mass and weight are NOT the same — mass is constant, weight varies",
            "On Moon: g ≈ 1.63 m/s² (1/6 of Earth's); weight on Moon = 1/6 of Earth weight",
            "Buoyant force = weight of displaced FLUID, not weight of the object",
            "G is universal constant; g depends on planet/location",
        ],
    },
    "sound": {
        "chapter": "Ch12: Sound",
        "definitions": [
            "Sound is a mechanical wave — requires a medium to travel (cannot travel in vacuum)",
            "Sound is a LONGITUDINAL wave (particles vibrate parallel to wave direction)",
            "Compressions: regions of high pressure; Rarefactions: regions of low pressure",
            "Speed of sound in air at 25°C ≈ 346 m/s; speed: solids > liquids > gases",
            "Frequency (Hz): number of oscillations per second; determines pitch",
            "Amplitude: maximum displacement from equilibrium; determines loudness",
            "Audible range for humans: 20 Hz to 20,000 Hz",
            "Infrasonic: below 20 Hz (cannot be heard by humans)",
            "Ultrasonic: above 20,000 Hz (used in SONAR, medical imaging)",
            "Echo: reflected sound heard after 0.1 s; minimum distance = 17.2 m",
            "SONAR: Sound Navigation And Ranging — uses ultrasonic waves underwater",
            "Reverberation: persistence of sound due to multiple reflections",
        ],
        "critical_flags": [
            "Sound is LONGITUDINAL, NOT transverse — 'transverse sound wave' is WRONG",
            "Sound CANNOT travel in vacuum — it needs a medium",
            "Echo requires minimum 17.2 m distance from reflector (not 10 m or 20 m)",
            "Speed of sound in air ≈ 346 m/s (NOT the speed of light 3×10⁸ m/s)",
            "Ultrasonic > 20,000 Hz; infrasonic < 20 Hz",
        ],
    },
}

# ── Class 9 Social Science ────────────────────────────────────────────────────────

SOCIAL_9 = {
    "history_chapters": [
        "Ch1: The French Revolution",
        "Ch2: Socialism in Europe and the Russian Revolution",
        "Ch3: Nazism and the Rise of Hitler",
        "Ch4: Forest Society and Colonialism",
        "Ch5: Pastoralists in the Modern World",
    ],
    "geography_chapters": [
        "Ch1: India – Size and Location",
        "Ch2: Physical Features of India",
        "Ch3: Drainage",
        "Ch4: Climate",
        "Ch5: Natural Vegetation and Wildlife",
        "Ch6: Population",
    ],
    "civics_chapters": [
        "Ch1: What is Democracy? Why Democracy?",
        "Ch2: Constitutional Design",
        "Ch3: Electoral Politics",
        "Ch4: Working of Institutions",
        "Ch5: Democratic Rights",
    ],
    "economics_chapters": [
        "Ch1: The Story of Village Palampur",
        "Ch2: People as Resource",
        "Ch3: Poverty as a Challenge",
        "Ch4: Food Security in India",
    ],
    "french_revolution": {
        "chapter": "Ch1: The French Revolution (History)",
        "key_facts": [
            "Year: 1789",
            "France had 3 Estates: First (clergy), Second (nobility), Third (commoners — bourgeoisie + peasants)",
            "Third Estate paid nearly all taxes; First and Second Estates were largely exempt",
            "Financial crisis due to: American War of Independence debts, lavish court spending under Louis XVI",
            "Estates General convened May 1789 — Third Estate demanded voting by head (not by estate)",
            "Tennis Court Oath: Third Estate formed National Assembly, pledged not to disperse until constitution framed",
            "Bastille stormed: July 14, 1789 — symbol of royal tyranny; now France's national day",
            "Declaration of Rights of Man and Citizen (1789): liberty, equality, fraternity",
            "Women's March on Versailles: women demanded bread, forced royal family to Paris",
            "Reign of Terror (1793–94): Robespierre and Committee of Public Safety executed thousands",
            "Napoleon Bonaparte rose to power; declared Emperor 1804; spread revolutionary ideals across Europe",
            "Key slogan: Liberté, Égalité, Fraternité",
            "Guillotine: instrument of execution during the Revolution",
        ],
    },
    "india_size_location": {
        "chapter": "Ch1: India – Size and Location (Geography)",
        "key_facts": [
            "Latitudinal extent: 8°4'N to 37°6'N",
            "Longitudinal extent: 68°7'E to 97°25'E",
            "Total area: 3.28 million sq km — 7th largest country in the world",
            "Land boundary: approximately 15,200 km",
            "Coastline (mainland + islands): 7,516.6 km",
            "Standard Meridian: 82°30'E passes through Mirzapur (UP) — IST = UTC+5:30",
            "Tropic of Cancer (23°30'N) passes through the middle of India",
            "India shares land borders with: Pakistan, Afghanistan, China, Nepal, Bhutan, Myanmar, Bangladesh",
            "Southernmost point of mainland: Kanyakumari; of India overall: Indira Point (Andaman & Nicobar)",
        ],
    },
    "social_science_ch5_s2": {
        "note": "Class 9 Social Science Chapter 5 varies by book: in Civics it is 'Democratic Rights'; in History it is 'Pastoralists in the Modern World'. The query 'section 2' likely refers to a sub-section of a chapter.",
    },
}

# ── Class 10 Mathematics ──────────────────────────────────────────────────────────

MATH_10 = {
    "chapters": [
        "Ch1: Real Numbers",
        "Ch2: Polynomials",
        "Ch3: Pair of Linear Equations in Two Variables",
        "Ch4: Quadratic Equations",
        "Ch5: Arithmetic Progressions",
        "Ch6: Triangles",
        "Ch7: Coordinate Geometry",
        "Ch8: Introduction to Trigonometry",
        "Ch9: Some Applications of Trigonometry",
        "Ch10: Circles",
        "Ch11: Areas Related to Circles",
        "Ch12: Surface Areas and Volumes",
        "Ch13: Statistics",
        "Ch14: Probability",
    ],
    "quadratic_equations": {
        "chapter": "Ch4: Quadratic Equations",
        "standard_form": "ax² + bx + c = 0, where a ≠ 0",
        "methods": [
            "Factorisation (splitting the middle term)",
            "Completing the square",
            "Quadratic formula: x = [−b ± √(b²−4ac)] / 2a",
        ],
        "discriminant": {
            "formula": "D = b² − 4ac",
            "D_gt_0": "Two distinct real roots",
            "D_eq_0": "Two equal real roots (one repeated root); x = −b/2a",
            "D_lt_0": "No real roots (imaginary/complex roots)",
        },
        "critical_flags": [
            "Formula is (−b ± √D) / 2a — denominator is 2a, NOT a",
            "D = b² − 4ac (minus, not plus)",
            "When D < 0 the equation has NO real solutions",
        ],
    },
}

# ── Class 10 Science ──────────────────────────────────────────────────────────────

SCIENCE_10 = {
    "chapters": [
        "Ch1: Chemical Reactions and Equations",
        "Ch2: Acids, Bases and Salts",
        "Ch3: Metals and Non-Metals",
        "Ch4: Carbon and Its Compounds",
        "Ch5: Periodic Classification of Elements",
        "Ch6: Life Processes",
        "Ch7: Control and Coordination",
        "Ch8: How do Organisms Reproduce?",
        "Ch9: Heredity and Evolution",
        "Ch10: Light – Reflection and Refraction",
        "Ch11: Human Eye and the Colourful World",
        "Ch12: Electricity",
        "Ch13: Magnetic Effects of Electric Current",
        "Ch14: Sources of Energy",
        "Ch15: Our Environment",
        "Ch16: Management of Natural Resources",
    ],
    "acids_bases_salts": {
        "chapter": "Ch2: Acids, Bases and Salts",
        "acids": [
            "pH < 7; sour taste; turn blue litmus paper red",
            "Release H⁺ ions in solution",
            "Common: HCl (hydrochloric), H₂SO₄ (sulphuric), HNO₃ (nitric), CH₃COOH (acetic/vinegar)",
            "Strong acids: HCl, H₂SO₄, HNO₃ (fully dissociate)",
            "Weak acids: CH₃COOH, H₂CO₃ (partially dissociate)",
        ],
        "bases": [
            "pH > 7; bitter taste; soapy/slippery feel; turn red litmus blue",
            "Release OH⁻ ions; alkalis are soluble bases",
            "Common: NaOH (caustic soda), Ca(OH)₂ (slaked lime), Mg(OH)₂, NH₄OH",
        ],
        "salts": [
            "Common salt: NaCl — neutral (pH 7)",
            "Baking soda: NaHCO₃ (sodium bicarbonate) — weakly alkaline; used in cooking, antacids",
            "Washing soda: Na₂CO₃·10H₂O — alkaline; used in glass, soap, paper making",
            "Bleaching powder: Ca(OCl)Cl — disinfectant, whitening agent",
            "Plaster of Paris: CaSO₄·½H₂O — sets hard when mixed with water",
        ],
        "ph_scale": "pH 0–14; pH 7 = neutral; pH < 7 = acidic; pH > 7 = basic/alkaline",
        "indicators": "Litmus (red in acid, blue in base), phenolphthalein, methyl orange, universal indicator",
        "neutralisation": "Acid + Base → Salt + Water; H⁺ + OH⁻ → H₂O",
        "critical_flags": [
            "Acids turn BLUE litmus RED (not the other way)",
            "Bases turn RED litmus BLUE",
            "NaHCO₃ is baking soda; Na₂CO₃ is washing soda — they are different",
            "pH scale is 0–14; below 0 or above 14 is outside the standard scale",
        ],
    },
    "nutrition_note": (
        "NCERT Class 10 Science covers Life Processes (Ch6) which includes nutrition modes "
        "(autotrophic/heterotrophic, photosynthesis, respiration), NOT a standalone 'Nutrition' chapter. "
        "A lesson plan titled just 'Nutrition' for Class 10 without specifying Life Processes may not be "
        "fully NCERT-aligned. Physical development is not a Ch10 Science chapter — it may be in CBSE "
        "Health/Physical Education, which is separate from NCERT Science."
    ),
}

# ── Class 10 Hindi ────────────────────────────────────────────────────────────────

HINDI_10 = {
    "kshitij_chapters": [
        "Ch1: Surdas ke Pad — Surdas [kavya; bhakti, Gopis' message to Krishna via Uddhav]",
        "Ch2: Ram-Lakshman-Parshuram Samvad — Tulsidas [kavya; from Ramcharitmanas]",
        "Ch3: Savaiye aur Kavitt — Dev [kavya]",
        "Ch4: Aatmkatha — Jaishankar Prasad [kavya; poem about NOT wanting to write an autobiography]",
        "Ch5: Utshav — Suryakant Tripathi Nirala [kavya]",
        "Ch6: Yah Danturit Muskan aur Phawdiyaan — Nagarjun [kavya]",
        "Ch7: Fasal — Girija Kumar Mathur [kavya]",
        "Ch8: Kanat — Rituraj [kavya]",
        "Ch9: Sangatkaar — Manglesh Dabral [kavya]",
        "Ch10: Netaji ka Chashma — Swayam Prakash [gadya; Subhash Chandra Bose, national pride]",
        "Ch11: Balgobin Bhagat — Ram Vriksha Benipuri [gadya; character sketch]",
        "Ch12: Lakhnawi Andaz — Yashpal [gadya; humour, nawabi culture]",
        "Ch13: Manviy Karunaiki Divya Chamak — Sarveshwar Dayal Saksena [gadya; Mother Teresa]",
        "Ch14: Ek Kahani Yeh Bhi — Manu Bhandari [gadya; autobiographical, women's issues]",
        "Ch15: Stri Shiksha ke Virodhi Kutarkon ka Khandan — Mahavir Prasad Dwivedi [gadya; essay]",
        "Ch16: Naubatkhane Mein Ibadat — Yatindra Mishra [gadya; Bismillah Khan, shehnai]",
        "Ch17: Sanskriti — Bhagwan Das Morwal [gadya; essay]",
    ],
    "kritika_chapters": [
        "Ch1: Mata ka Aanchal — Bhola Pant (Shivratan Yatri) [gadya; childhood, father-son bond]",
        "Ch2: George Pancham ki Naak — Kamleshwar [gadya; satire on colonial legacy]",
        "Ch3: Sana Sana Haath Jodi — Mridula Garg [gadya; travel essay, Sikkim/Gangtok]",
        "Ch4: Ehi Thaiyan Jhuluni Herani Ho Rama — Shivanath [gadya]",
        "Ch5: Main Kyon Likhta Hoon — Bhagwat Rawal [gadya]",
    ],
    "surdas_pad": {
        "chapter": "Ch1: Surdas ke Pad (Kshitij)",
        "key_facts": [
            "Surdas: 15th–16th century bhakti poet, disciple of Vallabhacharya; traditionally said to be blind",
            "Language: Brajbhasha",
            "The NCERT pads are from Bhramar Geet tradition: Gopies lamenting to Uddhav (Krishna's messenger)",
            "Uddhav brings message of Nirgun (formless) Brahman / Yoga; Gopies reject it for Sagun (Krishna with form)",
            "Gopies compare Uddhav to a bee (bhramar) — beautiful but sipping nectar without care",
            "Themes: Viyog (separation), Vatsalya bhav, Bhakti through love",
            "NOT about Krishna's childhood (bal leela) in these specific NCERT pads",
        ],
    },
    "aatmkatha": {
        "chapter": "Ch4: Aatmkatha — Jaishankar Prasad (Kshitij)",
        "key_facts": [
            "Jaishankar Prasad: Chhayavad poet; also wrote Kamayani (epic poem)",
            "This is a POEM about refusing to write an autobiography — not an actual autobiography",
            "Theme: The poet's suffering and memories are personal — he does not wish to expose them",
            "He says his life story would only bring tears and sadness to the listener",
            "Key mood: introspective, dignified, restrained pain",
            "If a lesson plan treats Aatmkatha as an actual autobiography of Prasad, that is WRONG",
        ],
    },
    "sana_sana": {
        "chapter": "Ch3: Sana Sana Haath Jodi — Mridula Garg (Kritika)",
        "key_facts": [
            "Genre: Yatra Vrittant (travel essay/memoir)",
            "Location: Sikkim — Gangtok, Yumthang Valley, Kavi Longchuk area",
            "Author travels by jeep through mountain roads",
            "Sights: prayer flags (lungdur), prayer wheels, Buddhist monasteries",
            "Natural beauty: waterfalls, hot springs, rhododendron forests, snow peaks",
            "Title meaning: 'Sana Sana Haath Jodi' = small small hands joined in prayer (Nepali/local phrase)",
            "Themes: spiritual peace, ecological sensitivity, cultural plurality, natural beauty",
            "A 'pathar-chatti' (road-side stop) is mentioned",
            "If lesson plan is about a different location or topic, it is not NCERT-aligned",
        ],
    },
}

# ── Class 10 English ──────────────────────────────────────────────────────────────

ENGLISH_10 = {
    "first_flight_chapters": [
        "Ch1: A Letter to God — G.L. Fuentes (prose)",
        "Ch2: Nelson Mandela – Long Walk to Freedom (prose)",
        "Ch3: Two Stories About Flying — His First Flight + Black Aeroplane (prose)",
        "Ch4: From the Diary of Anne Frank (prose)",
        "Ch5: Glimpses of India — A Baker from Goa + Coorg + Tea from Assam (prose)",
        "Ch6: Mijbil the Otter — Gavin Maxwell (prose)",
        "Ch7: Madam Rides the Bus — Vallikanni (prose)",
        "Ch8: The Sermon at Benares (prose)",
        "Ch9: The Proposal — Anton Chekhov (play)",
    ],
    "letter_to_god": {
        "chapter": "Ch1: A Letter to God — G.L. Fuentes, translated by Donald Yates",
        "key_facts": [
            "Author: G.L. Fuentes (Mexican author); English translation by Donald Yates",
            "Character: Lencho — a hardworking, religious farmer",
            "Plot: Lencho's crops destroyed by hailstorm; he writes a letter to God asking for 100 pesos",
            "Postmaster intercepts the letter; moved by Lencho's faith, collects money from postal employees",
            "Postmaster sends only 70 pesos (could not collect the full amount)",
            "Lencho writes a second letter to God complaining the remaining 30 pesos were stolen by 'crooks'",
            "Irony: Lencho trusts God completely but is suspicious of the very people who helped him",
            "Theme: Faith vs. human cynicism; irony; simple faith of a common man",
        ],
    },
}

# ── Class 7 Hindi ─────────────────────────────────────────────────────────────────

HINDI_7 = {
    "vasant_chapters": [
        "Ch1: Hum Panchi Unmukt Gagan Ke — Shivmangal Singh 'Suman' [kavya; birds want freedom]",
        "Ch2: Dadi Maa — Shivprasad Singh [gadya; grandmother's love]",
        "Ch3: Himmatwala [gadya]",
        "Ch4: Kathputali — Bhawani Prasad Mishra [kavya; puppet wanting freedom]",
        "Ch5: Mittan — Rahi Masoom Raza [gadya]",
        "Ch6: Rakhi ki Chaaon Mein [gadya]",
        "Ch7: Papaa Kho Gaye — Vijay Tendulkar [gadya/ekankee]",
        "Ch8: Shaam — Ek Kisan — Sarveshwar Dayal Saksena [kavya]",
        "Ch9: Ek Tinka — Ayodhya Singh Upadhyay 'Hariaudh' [kavya; ego and humility]",
        "Ch10: Khaan Pan ki Badlati Tasveerein [gadya]",
        "Ch11: Neelkanth — Mahadevi Verma [gadya; peacock as pet]",
        "Ch12: Bhoor Bhuiyan [kavya]",
        "Ch13: Ek Ting [gadya]",
        "Ch14: Khanabadosh [gadya]",
        "Ch15: Neem ki Daatun [gadya]",
        "Ch16: Bhor Aur Barkha [kavya]",
        "Ch17: Veer Kunwar Singh [gadya]",
        "Ch18: Sangharsh ke Kaaran Main Tunak Mizaaj Ho Gaya Dhruv Mitra [gadya]",
        "Ch19: Aashram ka Anumaanit Vyay [gadya]",
        "Ch20: Vijayi Vishv Tiranga Pyara [patriotic song]",
    ],
    "not_in_ncert": [
        "'Chutti Ka Din' (Chapter 9 Chutti Ka Din) — NOT in NCERT Class 7 Vasant; mark ncert_aligned FALSE",
        "'Bhasanjali' / 'Bhasaanjl' — NOT an NCERT textbook; it is a supplementary/state-level reader; mark ncert_aligned FALSE",
        "'Veer Tum Badhe Chalo, Dheer Tum Badhe Chalo' by Dwarkaprasad Mishra — NOT a standard chapter in NCERT Class 7 Vasant",
    ],
    "hum_panchi": {
        "chapter": "Ch1: Hum Panchi Unmukt Gagan Ke (Vasant)",
        "key_facts": [
            "Poet: Shivmangal Singh 'Suman'",
            "Theme: Birds in a cage long for freedom and open sky (unmukt gagan = free/open sky)",
            "Birds say they prefer bitter wild berries in freedom over sweet food in captivity",
            "They want to fly high, touch the clouds, drink the water of flowing rivers",
            "Symbolic meaning: human desire for freedom; restriction vs natural liberty",
            "Poetic devices: imagery of sky, rivers, birds; personification",
        ],
    },
}

# ── Class 12 Mathematics ──────────────────────────────────────────────────────────

MATH_12 = {
    "chapters": [
        "Ch1: Relations and Functions",
        "Ch2: Inverse Trigonometric Functions",
        "Ch3: Matrices",
        "Ch4: Determinants",
        "Ch5: Continuity and Differentiability",
        "Ch6: Application of Derivatives",
        "Ch7: Integrals",
        "Ch8: Application of Integrals",
        "Ch9: Differential Equations",
        "Ch10: Vector Algebra",
        "Ch11: Three-Dimensional Geometry",
        "Ch12: Linear Programming",
        "Ch13: Probability",
    ],
    "differentiation": {
        "chapter": "Ch5: Continuity and Differentiability (main) + Ch6: Application of Derivatives",
        "key_concepts": [
            "Derivative: f'(x) = lim[h→0] [f(x+h) − f(x)] / h",
            "Power rule: d/dx(xⁿ) = nxⁿ⁻¹",
            "Chain rule: d/dx[f(g(x))] = f'(g(x)) · g'(x)",
            "Product rule: d/dx[uv] = u'v + uv'",
            "Quotient rule: d/dx[u/v] = (u'v − uv') / v²",
            "Common derivatives: d/dx(sin x) = cos x; d/dx(cos x) = −sin x; d/dx(eˣ) = eˣ; d/dx(ln x) = 1/x",
            "Logarithmic differentiation for products/quotients of complicated functions",
            "Implicit differentiation",
            "Rolle's theorem; Lagrange's Mean Value Theorem (LMVT)",
            "Application of Derivatives (Ch6): maxima/minima, increasing/decreasing functions, tangents/normals",
        ],
    },
}

# ── Class 12 Geography ────────────────────────────────────────────────────────────

GEOGRAPHY_12 = {
    "fundamentals_chapters": [
        "Ch1: Human Geography – Nature and Scope",
        "Ch2: World Population – Distribution, Density and Growth",
        "Ch3: Population Composition",
        "Ch4: Human Development",
        "Ch5: Primary Activities",
        "Ch6: Secondary Activities",
        "Ch7: Tertiary and Quaternary Activities",
        "Ch8: Transport and Communication",
        "Ch9: International Trade",
        "Ch10: Human Settlements",
    ],
    "india_chapters": [
        "Ch1: Population: Distribution, Density, Growth and Composition",
        "Ch2: Migration: Types, Causes and Consequences",
        "Ch3: Human Development",
        "Ch4: Human Settlements",
        "Ch5: Land Resources and Agriculture",
        "Ch6: Water Resources",
        "Ch7: Mineral and Energy Resources",
        "Ch8: Manufacturing Industries",
        "Ch9: Planning and Sustainable Development in Indian Context",
        "Ch10: Transport and Communication",
        "Ch11: International Trade",
        "Ch12: Geographical Perspective on Selected Issues and Problems",
    ],
    "population_distribution": {
        "chapter": "Ch2 World Population (Fundamentals) and Ch1 India Population",
        "key_facts": [
            "Population density = Population / Area (persons per km²)",
            "Factors of dense population: fertile land (river valleys), moderate climate, water availability, industrialisation",
            "Factors of sparse population: extreme climate (deserts, polar), rugged terrain, poor soils",
            "Densely populated regions: South Asia, East Asia, North-West Europe, Eastern USA",
            "World population distribution: uneven; about 90% live on 10% of land",
            "India's population density (2011 census): 382 persons/km²",
            "Push factors: poverty, unemployment, drought, war",
            "Pull factors: better employment, education, amenities",
        ],
    },
}

# ── Class 12 Economics ────────────────────────────────────────────────────────────

ECONOMICS_12 = {
    "macro_chapters": [
        "Ch1: Introduction to Macroeconomics",
        "Ch2: National Income Accounting",
        "Ch3: Money and Banking",
        "Ch4: Determination of Income and Employment",
        "Ch5: Government Budget and the Economy",
        "Ch6: Open Economy Macroeconomics",
    ],
    "micro_chapters": [
        "Ch1: Introduction",
        "Ch2: Theory of Consumer Behaviour",
        "Ch3: Production and Costs",
        "Ch4: Theory of the Firm under Perfect Competition",
        "Ch5: Market Equilibrium",
        "Ch6: Non-Competitive Markets",
    ],
    "national_income": {
        "chapter": "Ch2: National Income Accounting (Macroeconomics)",
        "key_concepts": [
            "GDP (Gross Domestic Product): market value of all final goods and services produced within a country in a year",
            "GNP = GDP + Net Factor Income from Abroad (NFIA)",
            "NDP (Net Domestic Product) = GDP − Depreciation",
            "NNP (Net National Product) = GNP − Depreciation",
            "National Income = NNP at Factor Cost = NNP at Market Price − Net Indirect Taxes",
            "Personal Income: income actually received by households (includes transfer payments)",
            "Disposable Personal Income = Personal Income − Direct Taxes",
            "Three methods: Value Added (Product) Method, Income Method, Expenditure Method",
            "Double counting avoided by using Value Added or counting only FINAL goods",
            "Transfer payments (pensions, subsidies, scholarships) NOT included in GDP",
            "GDP does NOT capture distribution of income or non-market activities",
        ],
    },
}

# ── Class 5 Hindi ─────────────────────────────────────────────────────────────────

HINDI_5 = {
    "notes": (
        "NCERT Class 5 Hindi textbook is 'Rimjhim'. "
        "'Doha Ekadas' and 'Chawal ki Rotiyaan' are NOT standard chapters in NCERT Class 5 Hindi Rimjhim. "
        "If a teacher asks for content on these topics, ncert_aligned should be marked FALSE unless the "
        "output clearly connects to actual NCERT content."
    ),
    "not_in_ncert": [
        "'Doha Ekadas' — NOT a chapter in NCERT Class 5 Hindi Rimjhim",
        "'Chawal ki Rotiyaan' (चावल की रोटियाँ) — NOT a chapter in NCERT Class 5 Hindi Rimjhim",
    ],
}

# ── Class 8 Mathematics ───────────────────────────────────────────────────────────

MATH_8 = {
    "chapters": [
        "Ch1: Rational Numbers",
        "Ch2: Linear Equations in One Variable",
        "Ch3: Understanding Quadrilaterals",
        "Ch4: Practical Geometry",
        "Ch5: Data Handling",
        "Ch6: Squares and Square Roots",
        "Ch7: Cubes and Cube Roots",
        "Ch8: Comparing Quantities",
        "Ch9: Algebraic Expressions and Identities",
        "Ch10: Visualising Solid Shapes",
        "Ch11: Mensuration",
        "Ch12: Exponents and Powers",
        "Ch13: Direct and Inverse Proportions",
        "Ch14: Factorisation",
        "Ch15: Introduction to Graphs",
        "Ch16: Playing with Numbers",
    ],
    "grade_note": (
        "Class 8 Math covers rational numbers, linear equations, quadrilaterals, mensuration, "
        "basic algebra. No calculus, no quadratic equations (those are Class 10), no differentiation."
    ),
}

# ── Class 3 EVS ───────────────────────────────────────────────────────────────────

EVS_3 = {
    "textbook": "NCERT 'Aas Paas' (Looking Around)",
    "notes": (
        "Class 3 EVS covers very basic topics: family, community helpers, plants, animals, food, "
        "water, transport, shelter. Content must be age-appropriate for 8-year-old children. "
        "No complex scientific terminology; activity-based, visual learning."
    ),
    "grade_note": "Class 3 = 8-year-olds. Any content too abstract or text-heavy is grade-inappropriate.",
}

# ── Context builder ───────────────────────────────────────────────────────────────

def get_ncert_context_for_query(query: str) -> str:
    """
    Detect grade and subject from a teacher query and return NCERT curriculum
    context for injection into the judge prompt.
    Returns empty string if no relevant data available.
    """
    q = query.lower().replace("\n", " ")

    # ── Grade detection ───────────────────────────────────────────────────────────
    grade = None
    for g in ["12", "11", "10", "9", "8", "7", "6", "5", "4", "3"]:
        if (f"class {g}" in q or f"class-{g}" in q or f"class{g}" in q
                or f"कक्षा {g}" in q or f"क्लास {g}" in q
                or f"klass {g}" in q or f"{g}th" in q or f"{g}वीं" in q
                or f"claas {g}" in q):
            grade = g
            break

    # Subject flags
    is_sci  = any(w in q for w in ["science", "physics", "chemistry", "biology", "विज्ञान", "साइंस", "साउन"])
    is_math = any(w in q for w in ["math", "maths", "mathematics", "गणित"])
    is_hin  = any(w in q for w in ["hindi", "हिंदी", "हिन्दी", "kshitij", "kritika", "vasant", "rimjhim",
                                    "do bailo", "do bail", "kabir", "sakhiyan", "surdas", "aatmkatha",
                                    "sana sana", "साना", "pothi", "बैलों", "बालों"])
    is_hist = any(w in q for w in ["history", "इतिहास", "french", "revolution", "kranti", "farasisi", "bastille"])
    is_geo  = any(w in q for w in ["geography", "भूगोल", "aakar", "sthiti", "bharat", "population",
                                    "जनसंख्या", "वितरण"])
    is_eco  = any(w in q for w in ["economics", "economy", "अर्थशास्त्र", "national income",
                                    "gdp", "gnp", "राष्ट्रीय आय"])
    is_eng  = any(w in q for w in ["english", "letter to god", "lencho", "first flight"])
    is_evs  = any(w in q for w in ["evs", "environmental", "पर्यावरण", "पर्यावरण अध्ययन"])
    is_soc  = any(w in q for w in ["social science", "sst", "social"])

    lines = []

    # ── Class 9 ───────────────────────────────────────────────────────────────────
    if grade == "9":
        if is_hin:
            # Delegate to existing detailed Hindi 9 data
            import sys, os
            sys.path.insert(0, os.path.dirname(__file__))
            from ncert_data import get_hindi9_context
            return get_hindi9_context(query)

        if is_sci or any(w in q for w in ["motion", "gravitation", "gravity", "sound", "wave",
                                           "गति", "गुरुत्व", "ध्वनि", "echo", "sonar"]):
            lines += ["=== NCERT Class 9 Science — Chapter Reference ===",
                      "Chapters: " + " | ".join(SCIENCE_9["chapters"]), ""]

            for topic_key, kw_list in [
                ("motion",      ["motion", "गति", "velocity", "displacement", "acceleration", "distance"]),
                ("gravitation", ["gravitation", "gravity", "गुरुत्व", "weight", "mass", "buoy", "archimedes"]),
                ("sound",       ["sound", "ध्वनि", "साउन", "wave", "echo", "sonar", "frequency", "amplitude",
                                  "ultrasonic", "infrasonic", "longitudinal", "transverse"]),
            ]:
                if any(w in q for w in kw_list):
                    td = SCIENCE_9[topic_key]
                    lines.append(f"RELEVANT: {td['chapter']}")
                    if "definitions" in td:
                        lines.append("Key definitions:")
                        lines += [f"  • {d}" for d in td["definitions"]]
                    if "equations_of_motion" in td:
                        lines.append("Equations of motion:")
                        lines += [f"  • {e}" for e in td["equations_of_motion"]]
                    lines.append("Critical errors to flag:")
                    lines += [f"  !! {e}" for e in td["critical_flags"]]
                    lines.append("")

        if is_hist:
            lines += ["=== NCERT Class 9 History Chapters ===",
                      " | ".join(SOCIAL_9["history_chapters"]), ""]
            if any(w in q for w in ["french", "revolution", "kranti", "farasisi", "bastille", "liberty"]):
                fr = SOCIAL_9["french_revolution"]
                lines.append(f"RELEVANT: {fr['chapter']}")
                lines.append("Key facts:")
                lines += [f"  • {f}" for f in fr["key_facts"]]
                lines.append("")

        if is_geo:
            lines += ["=== NCERT Class 9 Geography Chapters ===",
                      " | ".join(SOCIAL_9["geography_chapters"]), ""]
            if any(w in q for w in ["india", "bharat", "aakar", "sthiti", "location", "size"]):
                ig = SOCIAL_9["india_size_location"]
                lines.append(f"RELEVANT: {ig['chapter']}")
                lines += [f"  • {f}" for f in ig["key_facts"]]
                lines.append("")

        if is_soc and not is_hist and not is_geo:
            lines += ["=== NCERT Class 9 Social Science ===",
                      "History: " + " | ".join(SOCIAL_9["history_chapters"]),
                      "Geography: " + " | ".join(SOCIAL_9["geography_chapters"]),
                      "Civics: " + " | ".join(SOCIAL_9["civics_chapters"]),
                      "Economics: " + " | ".join(SOCIAL_9["economics_chapters"]), ""]

    # ── Class 10 ──────────────────────────────────────────────────────────────────
    elif grade == "10":
        if is_math:
            lines += ["=== NCERT Class 10 Mathematics Chapters ===",
                      " | ".join(MATH_10["chapters"]), ""]
            if any(w in q for w in ["quadratic", "द्विघात", "discriminant"]):
                qt = MATH_10["quadratic_equations"]
                lines.append(f"RELEVANT: {qt['chapter']}")
                lines.append(f"Standard form: {qt['standard_form']}")
                lines.append("Solution methods: " + "; ".join(qt["methods"]))
                d = qt["discriminant"]
                lines += [f"Discriminant D = {d['formula']}",
                          f"  D > 0 → {d['D_gt_0']}",
                          f"  D = 0 → {d['D_eq_0']}",
                          f"  D < 0 → {d['D_lt_0']}"]
                lines.append("Critical errors:")
                lines += [f"  !! {e}" for e in qt["critical_flags"]]
                lines.append("")

        if is_sci or any(w in q for w in ["acid", "base", "salt", "ph", "अम्ल", "क्षार",
                                           "lavan", "लवण", "chemistry", "रसायन"]):
            lines += ["=== NCERT Class 10 Science Chapters ===",
                      " | ".join(SCIENCE_10["chapters"]), ""]
            if any(w in q for w in ["acid", "base", "salt", "अम्ल", "क्षार", "lavan", "ph"]):
                ab = SCIENCE_10["acids_bases_salts"]
                lines.append(f"RELEVANT: {ab['chapter']}")
                lines.append("Acids: " + "; ".join(ab["acids"]))
                lines.append("Bases: " + "; ".join(ab["bases"]))
                lines.append("Salts: " + "; ".join(ab["salts"]))
                lines.append(f"pH scale: {ab['ph_scale']}")
                lines.append(f"Indicators: {ab['indicators']}")
                lines.append("Critical errors:")
                lines += [f"  !! {e}" for e in ab["critical_flags"]]
                lines.append("")
            if any(w in q for w in ["nutrition", "पोषण", "physical", "शारीरिक"]):
                lines.append(f"NOTE: {SCIENCE_10['nutrition_note']}")
                lines.append("")

        if is_hin:
            lines += ["=== NCERT Class 10 Hindi Chapters ===",
                      "KSHITIJ (क्षितिज):"]
            lines += [f"  {ch}" for ch in HINDI_10["kshitij_chapters"]]
            lines += ["KRITIKA (कृतिका):"]
            lines += [f"  {ch}" for ch in HINDI_10["kritika_chapters"]]
            lines.append("")
            for kw_list, td in [
                (["surdas", "सूरदास", "pad", "gopi", "uddhav"], HINDI_10["surdas_pad"]),
                (["aatmkatha", "आत्मकथा", "prasad", "jaishankar"], HINDI_10["aatmkatha"]),
                (["sana sana", "साना", "sikkim", "gangtok", "mridula"], HINDI_10["sana_sana"]),
            ]:
                if any(w in q for w in kw_list):
                    lines.append(f"RELEVANT: {td['chapter']}")
                    lines += [f"  • {f}" for f in td["key_facts"]]
                    lines.append("")

        if is_eng:
            lines += ["=== NCERT Class 10 English First Flight Chapters ===",
                      " | ".join(ENGLISH_10["first_flight_chapters"]), ""]
            if any(w in q for w in ["letter to god", "lencho", "letter"]):
                lt = ENGLISH_10["letter_to_god"]
                lines.append(f"RELEVANT: {lt['chapter']}")
                lines += [f"  • {f}" for f in lt["key_facts"]]
                lines.append("")

    # ── Class 7 ───────────────────────────────────────────────────────────────────
    elif grade == "7":
        if is_hin:
            lines += ["=== NCERT Class 7 Hindi Vasant Chapters ==="]
            lines += [f"  {ch}" for ch in HINDI_7["vasant_chapters"]]
            lines += ["", "NOT IN NCERT Class 7 Hindi:"]
            lines += [f"  !! {n}" for n in HINDI_7["not_in_ncert"]]
            lines.append("")
            if any(w in q for w in ["hm panchi", "panchi", "unmukt", "पंछी", "birds", "suman"]):
                hp = HINDI_7["hum_panchi"]
                lines.append(f"RELEVANT: {hp['chapter']}")
                lines += [f"  • {f}" for f in hp["key_facts"]]
                lines.append("")

    # ── Class 12 ──────────────────────────────────────────────────────────────────
    elif grade == "12":
        if is_math:
            lines += ["=== NCERT Class 12 Mathematics Chapters ===",
                      " | ".join(MATH_12["chapters"]), ""]
            if any(w in q for w in ["differentiation", "derivative", "differential", "calculus"]):
                dt = MATH_12["differentiation"]
                lines.append(f"RELEVANT: {dt['chapter']}")
                lines.append("Key concepts:")
                lines += [f"  • {c}" for c in dt["key_concepts"]]
                lines.append("")

        if is_geo:
            lines += ["=== NCERT Class 12 Geography Chapters ===",
                      "Fundamentals of Human Geography:",
                      "  " + " | ".join(GEOGRAPHY_12["fundamentals_chapters"]),
                      "India – People and Economy:",
                      "  " + " | ".join(GEOGRAPHY_12["india_chapters"]), ""]
            if any(w in q for w in ["population", "distribution", "density", "जनसंख्या", "वितरण"]):
                pd = GEOGRAPHY_12["population_distribution"]
                lines.append(f"RELEVANT: {pd['chapter']}")
                lines += [f"  • {f}" for f in pd["key_facts"]]
                lines.append("")

        if is_eco:
            lines += ["=== NCERT Class 12 Economics Chapters ===",
                      "Macroeconomics: " + " | ".join(ECONOMICS_12["macro_chapters"]),
                      "Microeconomics: " + " | ".join(ECONOMICS_12["micro_chapters"]), ""]
            if any(w in q for w in ["national income", "gdp", "gnp", "राष्ट्रीय आय", "nnp", "ndp"]):
                ni = ECONOMICS_12["national_income"]
                lines.append(f"RELEVANT: {ni['chapter']}")
                lines.append("Key concepts:")
                lines += [f"  • {c}" for c in ni["key_concepts"]]
                lines.append("")

    # ── Class 5 ───────────────────────────────────────────────────────────────────
    elif grade == "5":
        if is_hin:
            lines += ["=== NCERT Class 5 Hindi Rimjhim — Notes ===",
                      HINDI_5["notes"], "",
                      "NOT in NCERT Class 5 Hindi:"]
            lines += [f"  !! {n}" for n in HINDI_5["not_in_ncert"]]
            lines.append("")

    # ── Class 8 ───────────────────────────────────────────────────────────────────
    elif grade == "8":
        if is_math:
            lines += ["=== NCERT Class 8 Mathematics Chapters ===",
                      " | ".join(MATH_8["chapters"]), "",
                      f"Grade note: {MATH_8['grade_note']}", ""]

    # ── Class 3 ───────────────────────────────────────────────────────────────────
    elif grade == "3":
        if is_evs or not (is_math or is_sci or is_hin):
            lines += ["=== NCERT Class 3 EVS (Aas Paas) — Notes ===",
                      EVS_3["notes"], "",
                      f"Grade note: {EVS_3['grade_note']}", ""]

    if not lines:
        return ""

    lines.append("=== END NCERT REFERENCE ===")
    return "\n".join(lines)
