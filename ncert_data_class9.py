"""
NCERT Class 9 chapter-level grounding data for Padhai Bot.
Covers: Science, Mathematics, Social Science, English.
(Hindi Class 9 is handled separately in ncert_data.py)

Each subject dict contains one entry per chapter with:
  - chapter_name  : official NCERT chapter name
  - topics        : 3-5 key concepts / topics
  - ncert_fact    : 1-2 key facts / definitions / central themes from NCERT
  - sel_dimension : one of growth_mindset | persistence | self_awareness |
                    emotional_regulation | social_awareness
  - sel_connection: 1 sentence linking chapter content to that SEL dimension
"""

# ─────────────────────────────────────────────────────────────────────────────
# SCIENCE
# ─────────────────────────────────────────────────────────────────────────────

SCIENCE9_DATA = [
    {
        "chapter_name": "Matter in Our Surroundings",
        "topics": [
            "States of matter (solid, liquid, gas)",
            "Interconversion of states",
            "Evaporation and latent heat",
            "Effect of temperature and pressure on states",
        ],
        "ncert_fact": (
            "Matter exists in three states — solid, liquid, and gas — determined by the "
            "arrangement and energy of particles. Evaporation is a surface phenomenon that "
            "causes cooling; latent heat of vaporisation is the heat absorbed during "
            "liquid-to-gas change at constant temperature."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Just as matter transforms between states under the right conditions, students "
            "can transform their abilities through effort and the right environment — a "
            "core idea of the growth mindset."
        ),
    },
    {
        "chapter_name": "Is Matter Around Us Pure",
        "topics": [
            "Pure substances vs. mixtures",
            "Homogeneous and heterogeneous mixtures",
            "Solutions, colloids, and suspensions",
            "Separation techniques (distillation, chromatography, crystallisation)",
            "Elements and compounds",
        ],
        "ncert_fact": (
            "A pure substance has a fixed composition and properties; mixtures can be "
            "separated by physical methods. Solutions are homogeneous mixtures where the "
            "solute particle size is less than 1 nm; colloids have particles between 1–100 nm "
            "and show the Tyndall effect."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Recognising what is 'pure' and what is 'mixed' in matter mirrors the "
            "self-awareness skill of distinguishing one's genuine values from external "
            "influences and distractions."
        ),
    },
    {
        "chapter_name": "Atoms and Molecules",
        "topics": [
            "Laws of chemical combination",
            "Dalton's atomic theory",
            "Atoms and atomic mass",
            "Molecules and molecular mass",
            "Mole concept and Avogadro's number",
        ],
        "ncert_fact": (
            "The Law of Conservation of Mass states that mass is neither created nor "
            "destroyed in a chemical reaction. The mole is the SI unit for amount of "
            "substance; 1 mole = 6.022 × 10²³ particles (Avogadro's number)."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Dalton's atomic theory was built through decades of careful observation and "
            "reasoning — modelling for students how persistent, methodical effort leads to "
            "breakthrough understanding."
        ),
    },
    {
        "chapter_name": "Structure of the Atom",
        "topics": [
            "Thomson's and Rutherford's atomic models",
            "Bohr's model of the atom",
            "Electrons, protons, and neutrons",
            "Atomic number and mass number",
            "Isotopes and isobars",
        ],
        "ncert_fact": (
            "Rutherford's gold-foil experiment established that an atom has a tiny, dense, "
            "positively charged nucleus surrounded by electrons. Bohr proposed that electrons "
            "revolve in fixed orbits (shells) and energy is emitted or absorbed when electrons "
            "jump between shells."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Each successive atomic model (Thomson → Rutherford → Bohr) improved on the "
            "previous one through curiosity and openness to revision — showing students that "
            "updating one's understanding is a sign of scientific and personal growth."
        ),
    },
    {
        "chapter_name": "The Fundamental Unit of Life",
        "topics": [
            "Cell as the basic unit of life",
            "Prokaryotic vs. eukaryotic cells",
            "Cell organelles and their functions",
            "Cell membrane, cell wall, and nucleus",
            "Osmosis and diffusion",
        ],
        "ncert_fact": (
            "All living organisms are composed of cells — the basic structural and functional "
            "unit of life. The nucleus contains the cell's genetic material (DNA) and controls "
            "cellular activities. Osmosis is the movement of water through a selectively "
            "permeable membrane from a region of higher water concentration to lower."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Understanding that every large organism is built from individual, specialised "
            "cells encourages students to recognise their own unique role and contribution "
            "within a larger community."
        ),
    },
    {
        "chapter_name": "Tissues",
        "topics": [
            "Plant tissues (meristematic and permanent)",
            "Animal tissues (epithelial, connective, muscular, nervous)",
            "Structure-function relationship in tissues",
            "Simple and complex permanent tissues in plants",
        ],
        "ncert_fact": (
            "Tissues are groups of similar cells performing a specific function. In plants, "
            "meristematic tissue contains dividing cells found at growing tips. In animals, "
            "nervous tissue is composed of neurons — specialised cells that transmit electrical "
            "impulses for rapid communication."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Just as different tissues work together to keep an organism healthy, students "
            "develop social awareness by recognising how cooperation among diverse groups "
            "sustains a healthy community."
        ),
    },
    {
        "chapter_name": "Diversity in Living Organisms",
        "topics": [
            "Basis and hierarchy of classification (Kingdom to Species)",
            "Five-kingdom classification (Monera, Protista, Fungi, Plantae, Animalia)",
            "Major plant divisions (Thallophyta to Angiospermae)",
            "Major animal phyla (Porifera to Chordata)",
            "Binomial nomenclature",
        ],
        "ncert_fact": (
            "Classification is based on evolutionary relationships and shared characteristics. "
            "Whittaker's five-kingdom system organises life into Monera, Protista, Fungi, "
            "Plantae, and Animalia. Binomial nomenclature (genus + species) was devised by "
            "Carolus Linnaeus."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Appreciating the enormous diversity of life — and that all organisms have a "
            "place in the ecosystem — builds social awareness about respecting diversity "
            "in human communities as well."
        ),
    },
    {
        "chapter_name": "Motion",
        "topics": [
            "Distance vs. displacement",
            "Speed vs. velocity",
            "Acceleration",
            "Equations of uniformly accelerated motion",
            "Distance-time and velocity-time graphs",
        ],
        "ncert_fact": (
            "Distance is the total path length (scalar); displacement is the shortest "
            "distance from initial to final position with direction (vector). The three "
            "equations of motion for uniform acceleration are: v = u + at, "
            "s = ut + ½at², and v² = u² + 2as."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Solving multi-step kinematics problems requires students to persist through "
            "complexity — selecting the right equation, substituting carefully, and checking "
            "units — mirroring persistence in real-life goal pursuit."
        ),
    },
    {
        "chapter_name": "Force and Laws of Motion",
        "topics": [
            "Newton's three laws of motion",
            "Inertia and mass",
            "Momentum and conservation of momentum",
            "Action-reaction pairs",
        ],
        "ncert_fact": (
            "Newton's First Law: a body continues in its state of rest or uniform motion "
            "unless acted upon by an external force (inertia). Newton's Second Law: "
            "F = ma. Newton's Third Law: every action has an equal and opposite reaction. "
            "Momentum p = mv is conserved in a closed system."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "Newton's First Law of inertia — that objects resist change — is a useful "
            "metaphor for understanding emotional habits; just as a force is needed to "
            "change motion, deliberate effort is needed to shift emotional patterns."
        ),
    },
    {
        "chapter_name": "Gravitation",
        "topics": [
            "Universal Law of Gravitation (F = Gm₁m₂/r²)",
            "Acceleration due to gravity (g = 9.8 m/s²)",
            "Mass vs. weight",
            "Archimedes' Principle and buoyancy",
            "Relative density",
        ],
        "ncert_fact": (
            "Newton's Universal Law of Gravitation states that every object attracts every "
            "other object with a force F = Gm₁m₂/r², where G = 6.674 × 10⁻¹¹ N m²/kg². "
            "Weight W = mg varies with location; mass remains constant everywhere."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "The same gravitational force that causes objects to fall also keeps planets in "
            "orbit — showing students that constraints can be the foundation of larger "
            "systems, encouraging a growth mindset about working within limitations."
        ),
    },
    {
        "chapter_name": "Work and Energy",
        "topics": [
            "Scientific definition of work (W = F × d × cosθ)",
            "Kinetic energy (KE = ½mv²)",
            "Potential energy (PE = mgh)",
            "Law of conservation of energy",
            "Power (P = W/t)",
        ],
        "ncert_fact": (
            "Work is done only when a force causes displacement in its direction; "
            "W = Fs cosθ (SI unit: joule). The Law of Conservation of Energy states that "
            "energy can neither be created nor destroyed, only converted from one form to "
            "another; total mechanical energy (KE + PE) is conserved in the absence of "
            "friction."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "The concept that energy invested (work done) is always conserved and "
            "transforms rather than disappears encourages students to see their persistent "
            "efforts as energy that never goes to waste."
        ),
    },
    {
        "chapter_name": "Sound",
        "topics": [
            "Sound as a longitudinal mechanical wave",
            "Characteristics: frequency, amplitude, speed",
            "Audible range, ultrasound, and infrasound",
            "Reflection of sound, echo, and reverberation",
            "SONAR and applications of ultrasound",
        ],
        "ncert_fact": (
            "Sound is a longitudinal wave that requires a medium to travel; it cannot "
            "travel through vacuum. The human audible range is 20 Hz to 20,000 Hz. An "
            "echo is heard when reflected sound reaches the ear at least 0.1 s after the "
            "original sound, requiring a minimum distance of 17.2 m from the reflector."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Sound requires a medium to travel — communication depends on connection; "
            "this parallels the idea that social awareness is built by actively listening "
            "and staying attuned to the 'medium' of one's community and relationships."
        ),
    },
    {
        "chapter_name": "Why Do We Fall Ill",
        "topics": [
            "Health vs. disease",
            "Causes of disease (immediate and contributory)",
            "Infectious vs. non-infectious diseases",
            "Modes of transmission of infectious diseases",
            "Prevention and treatment principles",
        ],
        "ncert_fact": (
            "Health is a state of physical, mental, and social well-being — not merely the "
            "absence of disease. Infectious diseases are caused by pathogens (bacteria, "
            "viruses, fungi, protozoa, worms) and can spread through air, water, food, "
            "contact, or vectors. Vaccines prevent infectious diseases by building immunity."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Recognising that health encompasses mental and social well-being — not just "
            "physical condition — encourages students to develop self-awareness about "
            "their emotional and social health alongside the physical."
        ),
    },
    {
        "chapter_name": "Natural Resources",
        "topics": [
            "Air, water, and soil as natural resources",
            "Biogeochemical cycles (water, nitrogen, carbon, oxygen)",
            "Soil formation and soil erosion",
            "Ozone layer and its importance",
            "Pollution and conservation",
        ],
        "ncert_fact": (
            "Air sustains life and moderates temperature through the greenhouse effect. "
            "The nitrogen cycle involves nitrogen fixation, nitrification, and "
            "denitrification — bacteria play a crucial role. The ozone layer in the "
            "stratosphere absorbs harmful UV radiation from the sun."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding that natural resources are shared and finite builds the social "
            "awareness needed to appreciate collective responsibility toward the environment "
            "and future generations."
        ),
    },
    {
        "chapter_name": "Improvement in Food Resources",
        "topics": [
            "Crop variety improvement (hybridisation, genetic modification)",
            "Crop production management (irrigation, manure, fertilisers, crop rotation)",
            "Crop protection (pest control, storage)",
            "Animal husbandry (cattle, poultry, fish)",
            "Green Revolution and its impact",
        ],
        "ncert_fact": (
            "Crop improvement aims for higher yield, better quality, and disease resistance "
            "through methods like hybridisation and introduction of high-yielding varieties "
            "(HYV). Mixed farming — cultivating crops alongside raising livestock — "
            "improves soil fertility and diversifies farmer income."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "The Green Revolution exemplifies a growth mindset at scale: applying "
            "scientific knowledge and effort to transform agricultural productivity, "
            "showing students that challenges like food security can be overcome "
            "through sustained innovation."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# MATHEMATICS
# ─────────────────────────────────────────────────────────────────────────────

MATH9_DATA = [
    {
        "chapter_name": "Number Systems",
        "topics": [
            "Natural numbers, integers, rational and irrational numbers",
            "Real numbers and the number line",
            "Representing irrational numbers on the number line",
            "Operations on real numbers",
            "Laws of exponents for real numbers",
        ],
        "ncert_fact": (
            "A rational number can be expressed as p/q where p, q are integers and q ≠ 0; "
            "its decimal expansion is either terminating or non-terminating recurring. "
            "An irrational number (e.g., √2, π) has a non-terminating, non-recurring "
            "decimal expansion. Together, rational and irrational numbers form the set of "
            "real numbers."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Discovering that numbers extend beyond familiar rationals to irrationals — "
            "and that the number system keeps expanding — models the growth mindset idea "
            "that knowledge and capability are never truly fixed or complete."
        ),
    },
    {
        "chapter_name": "Polynomials",
        "topics": [
            "Polynomials in one variable, degree, and coefficients",
            "Zeroes of a polynomial",
            "Remainder theorem",
            "Factor theorem",
            "Algebraic identities",
        ],
        "ncert_fact": (
            "A polynomial p(x) of degree n has at most n zeroes. The Remainder Theorem "
            "states that when p(x) is divided by (x − a), the remainder is p(a). "
            "The Factor Theorem states that (x − a) is a factor of p(x) if and only if "
            "p(a) = 0."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Factorising complex polynomials through systematic trial and application of "
            "theorems develops the persistence of working step-by-step until a solution "
            "is found — a habit that transfers to persisting through life challenges."
        ),
    },
    {
        "chapter_name": "Coordinate Geometry",
        "topics": [
            "Cartesian plane and axes",
            "Coordinates of a point (x, y)",
            "Quadrants and signs of coordinates",
            "Plotting points in the Cartesian plane",
        ],
        "ncert_fact": (
            "The Cartesian plane is formed by two perpendicular number lines (x-axis and "
            "y-axis) intersecting at the origin (0, 0). The plane is divided into four "
            "quadrants; the coordinates (x, y) give the position of any point as its "
            "signed horizontal and vertical distances from the origin."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Learning to locate any point precisely using two coordinates is a metaphor "
            "for self-awareness — knowing exactly 'where you are' on multiple dimensions "
            "of your life helps you navigate with intention."
        ),
    },
    {
        "chapter_name": "Linear Equations in Two Variables",
        "topics": [
            "Linear equation ax + by + c = 0",
            "Solutions as ordered pairs",
            "Graph of a linear equation — a straight line",
            "Equations of lines parallel to axes",
        ],
        "ncert_fact": (
            "A linear equation in two variables has infinitely many solutions, each "
            "representable as an ordered pair (x, y). The graph of every linear equation "
            "in two variables is a straight line, and every point on the line is a "
            "solution of the equation."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "The infinite solutions of a linear equation show students that most problems "
            "have multiple valid approaches — fostering the growth mindset belief that "
            "there is always another way forward."
        ),
    },
    {
        "chapter_name": "Introduction to Euclid's Geometry",
        "topics": [
            "Euclid's definitions, axioms, and postulates",
            "Euclid's five postulates",
            "Equivalent versions of the fifth postulate",
            "Relationship between axioms and theorems",
        ],
        "ncert_fact": (
            "Euclid's Elements established geometry on a small set of self-evident axioms "
            "and postulates from which all other theorems are logically derived. Euclid's "
            "fifth postulate (the parallel postulate) is the foundation of Euclidean "
            "geometry; its rejection gives rise to non-Euclidean geometries."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Euclid's work demonstrates that building a vast edifice of knowledge from "
            "a few basic truths takes patience and rigorous, persistent reasoning — "
            "a model for students developing long-term thinking habits."
        ),
    },
    {
        "chapter_name": "Lines and Angles",
        "topics": [
            "Types of angles (acute, obtuse, right, reflex, complementary, supplementary)",
            "Transversal and pairs of angles (alternate, corresponding, co-interior)",
            "Parallel lines and a transversal",
            "Angle sum property of a triangle",
        ],
        "ncert_fact": (
            "If a transversal intersects two parallel lines, then alternate interior angles "
            "are equal and co-interior (same-side interior) angles are supplementary (sum "
            "= 180°). The sum of the three interior angles of any triangle is 180°."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Just as every angle has a precise measure and relationship with others, "
            "self-awareness involves understanding our own positions, boundaries, and "
            "how we relate to the people around us."
        ),
    },
    {
        "chapter_name": "Triangles",
        "topics": [
            "Congruence of triangles and congruence criteria (SSS, SAS, ASA, AAS, RHS)",
            "Properties of isosceles triangles",
            "Inequalities in a triangle",
            "CPCT (Corresponding Parts of Congruent Triangles)",
        ],
        "ncert_fact": (
            "Two triangles are congruent if one can be superimposed exactly on the other. "
            "The main congruence criteria are SSS, SAS, ASA, AAS, and RHS. CPCT states "
            "that once congruence is established, all corresponding parts (sides and "
            "angles) are equal."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Congruence — two triangles being identical in structure — is a powerful "
            "metaphor for empathy and social awareness: truly understanding another person "
            "means finding the points of exact correspondence with their experience."
        ),
    },
    {
        "chapter_name": "Quadrilaterals",
        "topics": [
            "Angle sum property of quadrilaterals (sum = 360°)",
            "Types of quadrilaterals and their properties",
            "Parallelogram and its properties",
            "Mid-point theorem",
        ],
        "ncert_fact": (
            "The sum of the interior angles of any quadrilateral is 360°. In a "
            "parallelogram, opposite sides are equal and parallel, opposite angles are "
            "equal, and the diagonals bisect each other. The Mid-Point Theorem states "
            "that the line segment joining the mid-points of two sides of a triangle is "
            "parallel to the third side and half its length."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The properties of a parallelogram — where opposite sides support each other "
            "equally — illustrate how balanced, reciprocal relationships strengthen any "
            "social structure or team."
        ),
    },
    {
        "chapter_name": "Areas of Parallelograms and Triangles",
        "topics": [
            "Figures on the same base and between the same parallels",
            "Area of a parallelogram = base × height",
            "Area of a triangle = ½ × base × height",
            "Relationship between areas of triangles and parallelograms on the same base",
        ],
        "ncert_fact": (
            "Parallelograms on the same base and between the same parallels are equal in "
            "area. A triangle on the same base and between the same parallels as a "
            "parallelogram has area equal to half of that parallelogram."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Discovering that very different-looking shapes can have the same area teaches "
            "students not to judge by appearance alone — a growth mindset insight that "
            "potential comes in many forms."
        ),
    },
    {
        "chapter_name": "Circles",
        "topics": [
            "Circle, chord, diameter, arc, sector, segment",
            "Angle subtended by a chord at the centre and on the circle",
            "Perpendicular from the centre to a chord bisects it",
            "Cyclic quadrilaterals and their properties",
            "Equal chords and their distances from the centre",
        ],
        "ncert_fact": (
            "The angle subtended by an arc at the centre is double the angle subtended by "
            "it at any point on the remaining part of the circle. Angles in the same "
            "segment of a circle are equal. The opposite angles of a cyclic quadrilateral "
            "are supplementary (sum = 180°)."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "A circle's centre — equidistant from all points on the circumference — "
            "is a metaphor for emotional regulation: maintaining a calm, balanced centre "
            "allows one to respond evenly to the full range of life's events."
        ),
    },
    {
        "chapter_name": "Constructions",
        "topics": [
            "Construction of bisectors (angle bisector, perpendicular bisector)",
            "Construction of triangles given various conditions",
            "Division of a line segment in a given ratio",
            "Use of compass and straightedge",
        ],
        "ncert_fact": (
            "Geometric constructions using only a compass and straightedge follow Euclid's "
            "postulates. Key constructions include bisecting an angle, drawing a "
            "perpendicular bisector of a line segment, and constructing a triangle given "
            "two sides and the included angle (SAS) or two angles and a side (ASA)."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Geometric construction requires patient, precise, step-by-step work with no "
            "shortcuts — directly developing the persistence and attention to detail that "
            "lead to accurate, lasting results in any endeavour."
        ),
    },
    {
        "chapter_name": "Heron's Formula",
        "topics": [
            "Area of a triangle using Heron's Formula",
            "Semi-perimeter (s)",
            "Application to quadrilaterals by dividing into triangles",
        ],
        "ncert_fact": (
            "Heron's Formula gives the area of a triangle with sides a, b, c as: "
            "Area = √[s(s−a)(s−b)(s−c)], where s = (a+b+c)/2 is the semi-perimeter. "
            "It is especially useful when the height of the triangle is not known."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Heron's Formula provides a powerful alternative route to finding area when "
            "the standard formula seems inapplicable, teaching students that a growth "
            "mindset means always looking for another approach when the obvious one fails."
        ),
    },
    {
        "chapter_name": "Surface Areas and Volumes",
        "topics": [
            "Surface area of cuboid, cube, cylinder, cone, sphere",
            "Volume of cuboid, cube, cylinder, cone, sphere",
            "Conversion of units",
            "Combination of solids",
        ],
        "ncert_fact": (
            "Lateral surface area of a cylinder = 2πrh; total surface area = 2πr(r+h). "
            "Volume of a cone = ⅓πr²h; volume of a sphere = (4/3)πr³. "
            "The curved surface area of a cone = πrl, where l = slant height = √(r²+h²)."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Working through multi-step surface area and volume problems — identifying "
            "the right formula, substituting carefully, and checking units — builds "
            "the systematic persistence needed to tackle complex, layered challenges."
        ),
    },
    {
        "chapter_name": "Statistics",
        "topics": [
            "Collection, presentation, and organisation of data",
            "Ungrouped and grouped frequency distributions",
            "Graphical representation (bar graphs, histograms, frequency polygons)",
            "Measures of central tendency: mean, median, mode",
        ],
        "ncert_fact": (
            "Data can be represented graphically using bar graphs, histograms (for "
            "continuous data), and frequency polygons. For ungrouped data, "
            "Mean = (Sum of all observations) / (Number of observations). Median is the "
            "middle value when data is arranged in order; mode is the most frequently "
            "occurring value."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Statistics is fundamentally about making sense of many individual data "
            "points together — a process that builds social awareness by revealing "
            "patterns, inequalities, and shared experiences within a population."
        ),
    },
    {
        "chapter_name": "Probability",
        "topics": [
            "Experimental (empirical) probability",
            "Equally likely outcomes",
            "Probability of an event P(E) = favourable outcomes / total outcomes",
            "Impossible and certain events",
        ],
        "ncert_fact": (
            "The probability of an event E is P(E) = (Number of favourable outcomes) / "
            "(Total number of equally likely outcomes), and 0 ≤ P(E) ≤ 1. "
            "Experimental probability is found by performing an experiment; as the number "
            "of trials increases, experimental probability approaches theoretical probability."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "Understanding probability teaches students to accept uncertainty rationally "
            "rather than reacting with anxiety — a direct emotional regulation skill of "
            "responding to unpredictable outcomes with calm, reasoned thinking."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# SOCIAL SCIENCE  (4 books: History, Geography, Economics, Political Science)
# ─────────────────────────────────────────────────────────────────────────────

SOCIAL9_DATA = [
    # ── HISTORY: India and the Contemporary World I ───────────────────────────
    {
        "chapter_name": "The French Revolution",
        "book": "History",
        "topics": [
            "Causes of the French Revolution (social inequality, financial crisis, Enlightenment ideas)",
            "Three Estates and Tennis Court Oath",
            "Key events: Bastille, Declaration of Rights of Man, Reign of Terror",
            "Rise of Napoleon Bonaparte",
            "Abolition of slavery and role of women",
        ],
        "ncert_fact": (
            "The French Revolution (1789) abolished the privileges of the First and Second "
            "Estates and proclaimed the ideals of Liberté, Égalité, Fraternité. The "
            "storming of the Bastille on 14 July 1789 symbolised the end of royal tyranny. "
            "The Reign of Terror (1793–94) under Robespierre saw mass executions before "
            "Napoleon Bonaparte eventually rose to power."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The French Revolution's central demand for equality across social estates "
            "is a historical lesson in social awareness — understanding how systemic "
            "inequality affects entire communities and drives collective action."
        ),
    },
    {
        "chapter_name": "Socialism in Europe and the Russian Revolution",
        "book": "History",
        "topics": [
            "Ideas of socialism and Marxism",
            "Russian society under the Tsar",
            "1905 and 1917 Revolutions",
            "Lenin and the Bolsheviks",
            "Stalinist collectivisation and its consequences",
        ],
        "ncert_fact": (
            "The October Revolution of 1917 brought the Bolsheviks under Lenin to power "
            "in Russia, leading to the world's first socialist state. The Bolsheviks "
            "nationalised land and industry, withdrew from World War I, and formed the "
            "Soviet Union (USSR) in 1922."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Studying how workers and peasants organised collectively to challenge "
            "inequality builds social awareness about the conditions that lead communities "
            "to demand systemic change."
        ),
    },
    {
        "chapter_name": "Nazism and the Rise of Hitler",
        "book": "History",
        "topics": [
            "Impact of World War I and the Great Depression on Germany",
            "Rise of the Nazi Party and Hitler",
            "Nazi ideology, propaganda, and the Holocaust",
            "World War II and its consequences",
            "The Nuremberg Trials",
        ],
        "ncert_fact": (
            "Adolf Hitler and the Nazi Party exploited Germany's post-WWI humiliation "
            "(Treaty of Versailles) and economic depression to gain power in 1933. "
            "The Holocaust — the systematic genocide of six million Jews along with "
            "Roma, disabled people, and others — remains one of history's greatest "
            "crimes against humanity."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "Understanding how unchecked fear, hatred, and propaganda fuelled one of "
            "history's worst atrocities teaches students the critical importance of "
            "emotional regulation — particularly the skills of empathy and resisting "
            "manipulation by dehumanising rhetoric."
        ),
    },
    {
        "chapter_name": "Forest Society and Colonialism",
        "book": "History",
        "topics": [
            "Changes in forests under colonial rule",
            "Forest Acts and their impact on communities",
            "Rebellion in the forests (Bastar and Java)",
            "Scientific forestry vs. community rights",
        ],
        "ncert_fact": (
            "Colonial forest laws in India reserved large forest areas for timber "
            "extraction, restricting the rights of forest-dwelling communities to graze, "
            "cultivate, and collect forest produce. The Bastar rebellion of 1910 and "
            "similar revolts in Java were direct responses to loss of forest rights."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Examining how colonial policies displaced forest communities develops "
            "social awareness about how environmental and policy decisions can "
            "disproportionately harm marginalised groups."
        ),
    },
    {
        "chapter_name": "Pastoralists in the Modern World",
        "book": "History",
        "topics": [
            "Pastoral communities in Africa and India (Maasai, Gujjars, Raikas)",
            "Impact of colonial land laws on pastoralists",
            "Seasonal migration patterns",
            "Challenges faced by modern pastoralists",
        ],
        "ncert_fact": (
            "Pastoral communities depend on seasonal movement of livestock in search of "
            "pasture. Colonial governments in India and Africa enclosed common lands, "
            "imposed grazing taxes, and restricted movement — disrupting age-old "
            "pastoral ways of life and forcing many into settled agriculture."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding the disruption faced by pastoral communities builds empathy "
            "for groups whose livelihoods depend on ecological and social systems that "
            "are often invisible to dominant policymakers."
        ),
    },
    # ── GEOGRAPHY: Contemporary India I ──────────────────────────────────────
    {
        "chapter_name": "India – Size and Location",
        "book": "Geography",
        "topics": [
            "India's latitudinal and longitudinal extent",
            "Standard Meridian and Indian Standard Time",
            "Land and sea boundaries",
            "India's position in South Asia",
            "Neighbouring countries",
        ],
        "ncert_fact": (
            "India extends from 8°4'N to 37°6'N latitude and 68°7'E to 97°25'E longitude, "
            "covering 3.28 million km² (7th largest country). The Standard Meridian "
            "82°30'E passes through Mirzapur, Uttar Pradesh, giving India's time as "
            "IST = UTC + 5:30. The Tropic of Cancer (23°30'N) divides India roughly in half."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Knowing India's exact position in the world — its coordinates, borders, and "
            "neighbours — mirrors self-awareness: understanding where you are situated "
            "geographically, culturally, and relationally is the starting point for "
            "meaningful engagement with the wider world."
        ),
    },
    {
        "chapter_name": "Physical Features of India",
        "book": "Geography",
        "topics": [
            "Major physiographic divisions (Himalayas, Northern Plains, Peninsular Plateau, Coastal Plains, Islands)",
            "Formation of the Himalayas (Tethys Sea, plate tectonics)",
            "Northern Plains — alluvial deposits",
            "Peninsular Plateau — oldest landmass",
            "Lakshadweep and Andaman & Nicobar Islands",
        ],
        "ncert_fact": (
            "India has five major physiographic divisions. The Himalayas are geologically "
            "young, fold mountains formed by the collision of the Indo-Australian and "
            "Eurasian plates. The Northern Plains are formed by alluvial deposits from the "
            "Indus, Ganga, and Brahmaputra rivers. The Peninsular Plateau is composed of "
            "old crystalline, igneous, and metamorphic rocks."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "India's physical diversity — from the highest mountains to flat plains to "
            "island ecosystems — illustrates how varied origins and environments produce "
            "unique strengths, encouraging students to value diverse backgrounds and "
            "capabilities in a growth mindset spirit."
        ),
    },
    {
        "chapter_name": "Drainage",
        "book": "Geography",
        "topics": [
            "Drainage patterns and drainage basins",
            "Himalayan and Peninsular river systems",
            "Major rivers: Ganga, Indus, Brahmaputra, Godavari, Krishna",
            "Lakes and their importance",
            "Role of rivers in India's economy",
        ],
        "ncert_fact": (
            "India's rivers are classified into two groups: Himalayan rivers (perennial — "
            "fed by snow melt and rain) and Peninsular rivers (seasonal — fed mainly by "
            "rain). The Ganga is the largest river system in India; the Brahmaputra has "
            "one of the world's largest drainage basins."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Rivers persistently carve their way from mountains to sea, overcoming all "
            "obstacles and nourishing everything in their path — a powerful metaphor for "
            "the persistence and consistent effort that leads to long-term impact."
        ),
    },
    {
        "chapter_name": "Climate",
        "book": "Geography",
        "topics": [
            "Factors influencing India's climate (latitude, altitude, distance from sea, pressure, winds)",
            "Indian monsoon mechanism",
            "Seasons: cold weather, hot weather, advancing monsoon, retreating monsoon",
            "Distribution of rainfall in India",
            "El Niño effect",
        ],
        "ncert_fact": (
            "India has a monsoon type of climate. The southwest monsoon — which brings "
            "75–90% of India's annual rainfall — is caused by the differential heating "
            "of land and sea. The monsoon arrives over Kerala around June 1 and advances "
            "northward. The Western Ghats receive heavy orographic rainfall; the rain "
            "shadow areas (e.g., Deccan Plateau) receive very little."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The monsoon's seasonal rhythm — periods of intense activity followed by "
            "retreat and renewal — mirrors emotional regulation: learning to work with "
            "natural cycles of intensity and rest rather than fighting them."
        ),
    },
    {
        "chapter_name": "Natural Vegetation and Wildlife",
        "book": "Geography",
        "topics": [
            "Types of natural vegetation (tropical rainforest, deciduous, thorn, mangrove, alpine)",
            "Factors determining vegetation type",
            "Wildlife and biodiversity",
            "Biosphere reserves, national parks, and wildlife sanctuaries",
            "Endangered species and conservation",
        ],
        "ncert_fact": (
            "India has five major types of natural vegetation: tropical evergreen, tropical "
            "deciduous (the most widespread), tropical thorn, montane, and mangrove forests. "
            "The mangrove forests of the Sundarbans in the Ganga-Brahmaputra delta are the "
            "world's largest. India has over 90 national parks and 500+ wildlife sanctuaries."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Recognising that biodiversity loss affects every community — particularly "
            "those who depend directly on forests and wildlife — builds social awareness "
            "about shared ecological responsibility."
        ),
    },
    {
        "chapter_name": "Population",
        "book": "Geography",
        "topics": [
            "Population size, distribution, and density",
            "Population growth and processes (birth rate, death rate, migration)",
            "Age-sex composition and population pyramid",
            "Literacy, health, and occupational structure",
            "National Population Policy",
        ],
        "ncert_fact": (
            "India is the second most populous country in the world (Census 2011: ~1.21 "
            "billion; now surpassing China). Population density in 2011 was 382 persons/km². "
            "The Uttar Pradesh is the most populous state; Sikkim is the least populous. "
            "Population growth rate is measured using the Natural Growth Rate = Birth Rate "
            "minus Death Rate."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding population distribution and the challenges of rapid growth "
            "builds social awareness about the pressures on resources, infrastructure, "
            "and opportunities that shape the lives of millions of fellow citizens."
        ),
    },
    # ── ECONOMICS ────────────────────────────────────────────────────────────
    {
        "chapter_name": "The Story of Village Palampur",
        "book": "Economics",
        "topics": [
            "Organisation of production: land, labour, capital, enterprise",
            "Farming as the main activity",
            "Non-farm activities in a village",
            "Capital — physical, human, working",
            "Multiple cropping and HYV seeds",
        ],
        "ncert_fact": (
            "Palampur is a hypothetical Indian village used to illustrate the basics of "
            "economic organisation. Production requires four factors: land, labour, "
            "physical capital (tools, machines), and human capital (knowledge, skills). "
            "Multiple cropping (growing more than one crop in a year on the same land) "
            "and HYV seeds were key outcomes of the Green Revolution."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Palampur's farmers who adopted new seeds and irrigation to increase yields "
            "exemplify the growth mindset — embracing new knowledge and taking calculated "
            "risks to improve outcomes for themselves and their families."
        ),
    },
    {
        "chapter_name": "People as Resource",
        "book": "Economics",
        "topics": [
            "Human capital formation",
            "Role of education and health in economic development",
            "Unemployment: types and consequences",
            "Quality of population",
            "Women and economic development",
        ],
        "ncert_fact": (
            "People are considered a 'resource' because their education, health, and "
            "skills contribute to economic production — this investment is called human "
            "capital formation. India has a large working-age population, which can be a "
            "demographic dividend if adequately educated and healthy."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "The concept that people become a resource through education and skill "
            "development is the economic argument for the growth mindset: investing in "
            "one's abilities creates value not just personally but for society as a whole."
        ),
    },
    {
        "chapter_name": "Poverty as a Challenge",
        "book": "Economics",
        "topics": [
            "Poverty line and measurement of poverty",
            "Causes of poverty in India",
            "Vulnerable groups",
            "Anti-poverty measures and government programmes",
            "Global poverty comparisons",
        ],
        "ncert_fact": (
            "India uses a poverty line defined by a monthly per-capita expenditure that "
            "meets a minimum calorie requirement (2400 kcal/day rural; 2100 kcal/day "
            "urban). Despite significant reduction since 1973, poverty remains widespread, "
            "with SC/ST communities, agricultural labourers, and female-headed households "
            "being most vulnerable."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Studying poverty through data and real lives cultivates social awareness — "
            "moving students beyond abstract statistics to understand the human dimensions "
            "of economic inequality and the structural barriers people face."
        ),
    },
    {
        "chapter_name": "Food Security in India",
        "book": "Economics",
        "topics": [
            "Dimensions of food security (availability, access, absorption)",
            "Who is food insecure?",
            "Public Distribution System (PDS)",
            "Buffer stock and the Food Corporation of India",
            "Programmes for food security",
        ],
        "ncert_fact": (
            "Food security means ensuring that all people at all times have access to "
            "sufficient, safe, and nutritious food. The Public Distribution System (PDS) "
            "distributes food grains (wheat, rice) through Fair Price Shops to below-poverty-"
            "line households. The Food Corporation of India (FCI) manages buffer stocks of "
            "food grains to stabilise prices."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding that millions of Indians still face food insecurity despite "
            "national food surpluses sharpens social awareness about systemic gaps between "
            "policy intent and ground-level realities."
        ),
    },
    # ── POLITICAL SCIENCE: Democratic Politics I ──────────────────────────────
    {
        "chapter_name": "What is Democracy? Why Democracy?",
        "book": "Political Science",
        "topics": [
            "Definition and features of democracy",
            "Arguments for and against democracy",
            "Democracy vs. other forms of government",
            "Democratic and non-democratic examples",
        ],
        "ncert_fact": (
            "Democracy is a form of government in which rulers are elected by the people "
            "through free and fair elections, there is rule of law, and every citizen has "
            "equal rights. Key features include accountability, responsiveness, and "
            "protection of minority rights. Democracy is preferred because it promotes "
            "dignity and equality."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding democracy's core principle — that every citizen's voice matters "
            "equally — is a direct expression of social awareness, recognising the dignity "
            "and worth of all members of the community."
        ),
    },
    {
        "chapter_name": "Constitutional Design",
        "book": "Political Science",
        "topics": [
            "Constituent Assembly of India",
            "Key features of the Indian Constitution",
            "Fundamental Rights and Directive Principles",
            "Constitutional values: liberty, equality, fraternity, justice",
            "South Africa's constitutional transition as a comparative example",
        ],
        "ncert_fact": (
            "The Constituent Assembly (1946–49), chaired by Dr B.R. Ambedkar as Chair of "
            "the Drafting Committee, created the Indian Constitution — the longest written "
            "constitution in the world, adopted on 26 November 1949 and effective from "
            "26 January 1950. It guarantees Fundamental Rights to all citizens."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The Constitution's founding commitment to equality, justice, and fraternity "
            "reflects the highest level of social awareness — designing institutions that "
            "protect every citizen, especially the most marginalised."
        ),
    },
    {
        "chapter_name": "Electoral Politics",
        "book": "Political Science",
        "topics": [
            "Why elections are necessary",
            "Types of electoral systems",
            "Indian election process (Election Commission, constituencies, voting)",
            "Free and fair elections",
            "Role of political parties and candidates",
        ],
        "ncert_fact": (
            "India follows the First Past the Post (FPTP) electoral system for Lok Sabha "
            "and State Assembly elections. The Election Commission of India (an independent "
            "constitutional body) oversees all elections. The minimum voting age is 18 "
            "years. India's general elections are the largest democratic exercise in the world."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Learning how elections work — and why participation matters — builds the "
            "social awareness that individual civic choices collectively shape the "
            "governance experienced by an entire society."
        ),
    },
    {
        "chapter_name": "Working of Institutions",
        "book": "Political Science",
        "topics": [
            "Parliament: Lok Sabha and Rajya Sabha",
            "Role of the Prime Minister and Council of Ministers",
            "President of India and powers",
            "Supreme Court and Judiciary",
            "How major policy decisions are made",
        ],
        "ncert_fact": (
            "The Parliament of India consists of two Houses: Lok Sabha (House of the People, "
            "directly elected, 543 seats) and Rajya Sabha (Council of States, indirectly "
            "elected). The Prime Minister is the head of government and must maintain the "
            "confidence of the Lok Sabha. The Supreme Court is the final interpreter of "
            "the Constitution."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Understanding how government institutions check and balance each other "
            "develops students' social awareness about the systems designed to protect "
            "collective interests from individual or group power."
        ),
    },
    {
        "chapter_name": "Democratic Rights",
        "book": "Political Science",
        "topics": [
            "Six Fundamental Rights in the Indian Constitution",
            "Right to Constitutional Remedies and the role of courts",
            "Rights in a democracy",
            "Expanding scope of rights (human rights, environmental rights)",
            "Rights as protections against state power",
        ],
        "ncert_fact": (
            "The Indian Constitution guarantees six Fundamental Rights: Right to Equality "
            "(Articles 14–18), Right to Freedom (Articles 19–22), Right against "
            "Exploitation (Articles 23–24), Right to Freedom of Religion (Articles 25–28), "
            "Cultural and Educational Rights (Articles 29–30), and Right to Constitutional "
            "Remedies (Article 32 — the 'Heart and Soul' of the Constitution per Ambedkar)."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Knowing one's rights is an act of self-awareness — understanding the "
            "protections and freedoms one is entitled to is the foundation for both "
            "personal dignity and informed civic participation."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# ENGLISH  (Beehive prose + poems, Moments supplementary reader)
# ─────────────────────────────────────────────────────────────────────────────

ENGLISH9_DATA = [
    # ── BEEHIVE — Prose ───────────────────────────────────────────────────────
    {
        "chapter_name": "The Fun They Had",
        "book": "Beehive (Prose)",
        "author": "Isaac Asimov",
        "topics": [
            "Future schooling vs. traditional schools",
            "Role of technology in education",
            "Isolation and the need for human connection",
            "Children's curiosity about the past",
        ],
        "ncert_fact": (
            "Set in 2157, Margie and Tommy find an old printed book and learn about "
            "traditional schools where children sat together with a human teacher. Margie, "
            "who is taught at home by a mechanical teacher, feels wistful about the fun "
            "children in the past must have had learning together."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Margie's longing for the communal classroom experience illustrates social "
            "awareness — recognising that human connection and shared learning are "
            "irreplaceable dimensions of a meaningful education."
        ),
    },
    {
        "chapter_name": "The Sound of Music",
        "book": "Beehive (Prose)",
        "topics": [
            "Evelyn Glennie — overcoming deafness to become a percussionist",
            "Bismillah Khan and the shehnai",
            "Music as passion and identity",
            "Perseverance in the face of disability",
        ],
        "ncert_fact": (
            "Part I features Evelyn Glennie, a profoundly deaf Scottish musician who "
            "learned to sense sound through vibrations and became a world-renowned "
            "percussionist. Part II covers Ustad Bismillah Khan, who is credited with "
            "popularising the shehnai on the international stage and was awarded the "
            "Bharat Ratna in 2001."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Evelyn Glennie's refusal to accept that deafness meant the end of her musical "
            "dreams — and Bismillah Khan's lifelong dedication to the shehnai — are among "
            "the most vivid examples of persistence in the NCERT curriculum."
        ),
    },
    {
        "chapter_name": "The Little Girl",
        "book": "Beehive (Prose)",
        "author": "Katherine Mansfield",
        "topics": [
            "Father-daughter relationship",
            "Fear evolving into love and understanding",
            "Changing perceptions through empathy",
        ],
        "ncert_fact": (
            "Kezia is terrified of her stern father and finds him cold and intimidating. "
            "After an incident where she accidentally destroys his speech papers, she sees "
            "a different side of him when he comforts her during a nightmare — helping "
            "her understand that adults, including authority figures, have their own "
            "vulnerabilities."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "Kezia's journey from fear to empathy — learning to see her father as a "
            "whole, tired human being — demonstrates emotional regulation through "
            "perspective-taking and managing strong fear responses."
        ),
    },
    {
        "chapter_name": "A Truly Beautiful Mind",
        "book": "Beehive (Prose)",
        "topics": [
            "Albert Einstein's early life and education",
            "Theory of Relativity",
            "Einstein's pacifism and advocacy for peace",
            "Genius, persistence, and social responsibility",
        ],
        "ncert_fact": (
            "Einstein struggled in school initially but developed a passionate interest "
            "in mathematics and physics on his own. He published the Special Theory of "
            "Relativity in 1905 and won the Nobel Prize in Physics in 1921. Later in "
            "life he was deeply committed to peace and nuclear disarmament, co-signing "
            "the Russell-Einstein Manifesto in 1955."
        ),
        "sel_dimension": "growth_mindset",
        "sel_connection": (
            "Einstein's story — from a child who spoke late and was considered slow to "
            "one of history's greatest scientists — is one of the most powerful growth "
            "mindset narratives: believing in one's own capacity despite early difficulty."
        ),
    },
    {
        "chapter_name": "The Snake and the Mirror",
        "book": "Beehive (Prose)",
        "author": "Vaikom Muhammad Basheer",
        "topics": [
            "Vanity and humility",
            "Humour and self-deprecation",
            "Confronting fear and life's unpredictability",
        ],
        "ncert_fact": (
            "A homeopathic doctor narrates the terrifying night when a cobra wrapped itself "
            "around his arm while he sat admiring himself in a mirror. The story uses dark "
            "humour — the doctor's vanity is punctured by the snake — and ends safely when "
            "the snake is distracted and slithers away."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The doctor's ability to stay calm in the face of mortal danger — while "
            "also recognising his own earlier vanity — illustrates how self-awareness "
            "and emotional regulation can co-exist even in moments of extreme fear."
        ),
    },
    {
        "chapter_name": "My Childhood",
        "book": "Beehive (Prose)",
        "author": "A.P.J. Abdul Kalam",
        "topics": [
            "Kalam's early life in Rameswaram",
            "Communal harmony and friendship",
            "Influence of teachers and family on ambition",
            "Determination to overcome socio-economic barriers",
        ],
        "ncert_fact": (
            "Abdul Kalam grew up in a modest Muslim family in Rameswaram, Tamil Nadu, "
            "in an atmosphere of religious harmony — his close friends were Hindu, and "
            "his science teacher Sivasubramania Iyer actively broke social barriers. "
            "Kalam credits his father's wisdom and his teachers' encouragement for "
            "nurturing his dream of becoming a scientist."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Kalam's reflections on the values, relationships, and experiences that shaped "
            "his character model self-awareness — the practice of understanding the "
            "formative influences on who we are and who we want to become."
        ),
    },
    {
        "chapter_name": "Reach for the Top",
        "book": "Beehive (Prose)",
        "topics": [
            "Santosh Yadav — first woman to scale Everest twice",
            "Maria Sharapova — determination to become a tennis champion",
            "Sacrifice, hard work, and focus",
            "Breaking gender and social barriers",
        ],
        "ncert_fact": (
            "Part I profiles Santosh Yadav, who defied family resistance to become a "
            "mountaineer and the first woman in the world to scale Mount Everest twice. "
            "Part II covers Maria Sharapova, who left Russia at age nine for tennis "
            "training in the USA, endured years of separation from her parents, and became "
            "the world's top-ranked women's tennis player."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Both Santosh Yadav and Maria Sharapova demonstrate extraordinary persistence "
            "— sacrificing comfort, family, and certainty in relentless pursuit of their "
            "goals, showing students what sustained commitment looks like in practice."
        ),
    },
    {
        "chapter_name": "Kathmandu",
        "book": "Beehive (Prose)",
        "author": "Vikram Seth",
        "topics": [
            "Travel writing and observation",
            "Pashupatinath Temple and Baudhnath Stupa",
            "Chaos and serenity in Kathmandu",
            "Contrasts between sacred and commercial spaces",
        ],
        "ncert_fact": (
            "Vikram Seth's travel essay describes a day in Kathmandu, Nepal, visiting the "
            "sacred Pashupatinath Temple (a major Hindu shrine on the Bagmati river) and "
            "the serene Buddhist Baudhnath Stupa. The essay contrasts the commercial "
            "bustle of Kathmandu's streets with the spiritual atmosphere of its temples."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Observing how people navigate sacred and commercial spaces side by side "
            "invites students to reflect on their own inner contrasts — the busy, "
            "'commercial' mind versus the quieter, reflective self."
        ),
    },
    {
        "chapter_name": "If I Were You",
        "book": "Beehive (Prose)",
        "author": "Douglas James",
        "topics": [
            "One-act play format",
            "Wit and presence of mind overcoming threat",
            "Identity and role reversal",
            "Humour in a tense situation",
        ],
        "ncert_fact": (
            "A playwright (Gerrard) is held at gunpoint by an intruder who plans to kill "
            "him and assume his identity. Using quick thinking and wit, Gerrard convinces "
            "the intruder that his own life is in danger as a wanted fugitive, luring "
            "him into a cupboard and trapping him. The play explores themes of identity "
            "and quick-wittedness."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "Gerrard's calm, sharp thinking under extreme threat demonstrates how "
            "emotional regulation — keeping a cool head in crisis — is more powerful "
            "than panic or force."
        ),
    },
    # ── BEEHIVE — Poems ───────────────────────────────────────────────────────
    {
        "chapter_name": "The Road Not Taken",
        "book": "Beehive (Poem)",
        "author": "Robert Frost",
        "topics": [
            "Decision-making and diverging paths",
            "Individuality and non-conformity",
            "Reflection and regret vs. acceptance",
            "Symbolism of a fork in the road",
        ],
        "ncert_fact": (
            "The speaker stands at a fork in a yellow wood and chooses the road that seems "
            "less travelled. The poem's famous closing lines — 'I shall be telling this with "
            "a sigh / Somewhere ages and ages hence' — suggest that choices define us, and "
            "we tend to rationalise them as having made 'all the difference'."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "The poem is a meditation on self-awareness in the moment of choice: "
            "being conscious of the paths available, the values guiding the decision, "
            "and the responsibility of owning the consequences."
        ),
    },
    {
        "chapter_name": "Wind",
        "book": "Beehive (Poem)",
        "author": "Subramania Bharati",
        "topics": [
            "Wind as a symbol of challenges and adversity",
            "Strength and resilience",
            "Friendship with the wind through inner strength",
            "Call to be firm and strong",
        ],
        "ncert_fact": (
            "The poem addresses the wind directly, challenging it for destroying the weak "
            "while praising the strong. The poet urges people to build strong bodies and "
            "minds so that the wind (adversity) becomes a friend rather than an enemy. "
            "Originally written in Tamil by Subramania Bharati, translated into English."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "The poem's central message — strengthen yourself so that challenges become "
            "your allies — is a direct call for the persistence and resilience needed "
            "to convert adversity into growth."
        ),
    },
    {
        "chapter_name": "Rain on the Roof",
        "book": "Beehive (Poem)",
        "author": "Coates Kinney",
        "topics": [
            "Sensory imagery of rain",
            "Nostalgia and memory",
            "Comfort of home and mother's presence",
            "Effect of rain on the mind",
        ],
        "ncert_fact": (
            "As rain patters on the shingles at night, the poet lies snugly in bed and "
            "is carried into reverie — recalling his mother's loving face and childhood "
            "memories. The poem uses rich sensory imagery (the 'patter', 'darkness' of "
            "the cottage, 'humid shadows') to evoke the comfort of a rainy night."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The poem illustrates how a sensory anchor — the sound of rain — can "
            "soothe the mind and bring comforting memories to the surface, a natural "
            "example of emotional regulation through mindful attention to one's "
            "environment."
        ),
    },
    {
        "chapter_name": "A Legend of the Northland",
        "book": "Beehive (Poem)",
        "author": "Phoebe Cary",
        "topics": [
            "Ballad form and storytelling",
            "Selfishness and its consequences",
            "Saint Peter and the stingy woman",
            "Transformation as moral lesson",
        ],
        "ncert_fact": (
            "This narrative ballad tells of Saint Peter visiting a selfish old woman who "
            "refuses to give him even a small piece of bread from her baking. As "
            "punishment, she is transformed into a woodpecker (pecker bird), doomed to "
            "bore through hard, dry wood for food — a moral fable about greed and "
            "generosity."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The fable's sharp moral — that selfishness isolates and diminishes us — "
            "develops social awareness about generosity, empathy, and the social "
            "bonds that sustain communities."
        ),
    },
    {
        "chapter_name": "No Men Are Foreign",
        "book": "Beehive (Poem)",
        "author": "James Kirkup",
        "topics": [
            "Universal brotherhood and common humanity",
            "War and its futility",
            "Shared human experience across borders",
            "Hatred as self-destruction",
        ],
        "ncert_fact": (
            "The poem argues that no human being is truly foreign — all people share the "
            "same body, breathe the same air, experience the same sun, and are united "
            "by love of land and life. The final stanza warns that those who hate and "
            "wage war against other humans ultimately betray and destroy themselves."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The poem's core insight — that our shared humanity makes every person "
            "our neighbour — is the foundation of social awareness and intercultural "
            "empathy."
        ),
    },
    {
        "chapter_name": "On Killing a Tree",
        "book": "Beehive (Poem)",
        "author": "Gieve Patel",
        "topics": [
            "Resilience of nature",
            "Environmental awareness",
            "Extended metaphor — tree as symbol of human will",
            "What it truly takes to 'kill' something rooted",
        ],
        "ncert_fact": (
            "The poem describes how difficult it is to kill a tree — a simple jab will "
            "not do it; even a hacked tree grows back. Only by uprooting the tree — "
            "exposing and destroying the root, the 'source of life' in the earth — can "
            "it be killed. The poem is also read as an extended metaphor for deeply "
            "rooted habits, beliefs, or institutions."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "The tree's stubborn return after every blow is a metaphor for persistence "
            "and resilience — the deeper the roots of effort, habit, and character, "
            "the harder they are to uproot, even by adversity."
        ),
    },
    {
        "chapter_name": "The Snake Trying",
        "book": "Beehive (Poem)",
        "author": "W.W.E. Ross",
        "topics": [
            "Empathy for a misunderstood creature",
            "Non-violence and co-existence",
            "Fear vs. understanding in nature",
        ],
        "ncert_fact": (
            "A snake glides through water trying to escape a man with a stick. The poet "
            "urges the man to let it go — the snake is harmless and beautiful. The poem "
            "pleads for co-existence and challenges the human impulse to destroy what "
            "it fears."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Empathising with a creature typically feared and destroyed develops "
            "social awareness by challenging students to extend understanding and "
            "compassion even to those (or things) perceived as threatening."
        ),
    },
    {
        "chapter_name": "A Slumber Did My Spirit Seal",
        "book": "Beehive (Poem)",
        "author": "William Wordsworth",
        "topics": [
            "Death and grief",
            "Loss of a loved one",
            "Nature's indifference vs. human mourning",
            "Simplicity and depth in short verse",
        ],
        "ncert_fact": (
            "This two-stanza poem mourns the death of a beloved. In the first stanza the "
            "poet, in a 'slumber', thought the beloved was immortal; in the second he "
            "confronts the reality of her death — she is now part of the earth, rolled "
            "round by rocks and stones. The poem explores the tension between imagined "
            "immortality and the finality of death."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The poem's quiet confrontation with grief — moving from denial ('slumber') "
            "to acceptance of loss — models how acknowledging and processing difficult "
            "emotions is a key emotional regulation skill."
        ),
    },
    # ── MOMENTS — Supplementary Reader ───────────────────────────────────────
    {
        "chapter_name": "The Lost Child",
        "book": "Moments (Supplementary)",
        "author": "Mulk Raj Anand",
        "topics": [
            "A child's desires and distractions at a fair",
            "Parental attachment and the panic of separation",
            "Emotional shift from joy to fear to grief",
        ],
        "ncert_fact": (
            "A young boy accompanies his parents to a village fair. Distracted by toys, "
            "sweets, garlands, and a roundabout, he keeps drifting, only to suddenly "
            "realise he is lost. Overcome with grief, he refuses all consolation from "
            "a kind stranger — he wants only his parents. The story shows how security "
            "transforms our desires."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The lost child's emotional arc — from excitement to terror to inconsolable "
            "grief — illustrates how separation anxiety overwhelms cognitive function, "
            "helping students recognise the power of attachment and the importance of "
            "emotional safety."
        ),
    },
    {
        "chapter_name": "The Adventures of Toto",
        "book": "Moments (Supplementary)",
        "author": "Ruskin Bond",
        "topics": [
            "Pet ownership and responsibility",
            "Mischief and consequences",
            "Compassion for animals",
        ],
        "ncert_fact": (
            "The narrator's grandfather buys Toto, a mischievous little monkey, from a "
            "tonga driver. Toto's antics — tearing wallpaper, upsetting grandmother, "
            "and most famously scalding himself by climbing into a kettle of hot water "
            "— make him too expensive and disruptive to keep, so he is eventually returned."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Toto's story encourages empathy for animals and awareness of the "
            "responsibilities that come with relationships — lessons in social awareness "
            "about the impact one's choices have on others."
        ),
    },
    {
        "chapter_name": "Iswaran the Storyteller",
        "book": "Moments (Supplementary)",
        "author": "R.K. Laxman",
        "topics": [
            "Power of storytelling and imagination",
            "Loyalty and companionship",
            "The thin line between story and belief",
        ],
        "ncert_fact": (
            "Iswaran is an extraordinarily devoted cook who follows his employer Mahendra "
            "everywhere. He can spin a mundane event into an enthralling tale with "
            "dramatic pauses and vivid details. His terrifying ghost story about a "
            "female apparition eventually so unnerves Mahendra that he quits his job "
            "and moves away."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Iswaran's ability to shape Mahendra's reality through storytelling prompts "
            "self-awareness about how the narratives we tell ourselves and others "
            "powerfully influence our emotions and decisions."
        ),
    },
    {
        "chapter_name": "In the Kingdom of Fools",
        "book": "Moments (Supplementary)",
        "topics": [
            "Foolish rulers and arbitrary justice",
            "Wisdom vs. power",
            "Injustice and its consequences",
            "Guru-shishya relationship",
        ],
        "ncert_fact": (
            "A king and minister in the Kingdom of Fools reverse day and night — work "
            "at night, sleep during day. A guru and disciple visit; the disciple decides "
            "to stay for cheap food. A series of absurd chain-of-blame reasoning leads "
            "the king to condemn an innocent man, but through the guru's wisdom, justice "
            "is unexpectedly served."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The story's satire on arbitrary power and foolish governance develops "
            "social awareness about how justice systems can perpetuate injustice, and "
            "how wisdom and moral courage are needed to protect the innocent."
        ),
    },
    {
        "chapter_name": "The Happy Prince",
        "book": "Moments (Supplementary)",
        "author": "Oscar Wilde",
        "topics": [
            "Compassion and self-sacrifice",
            "Social inequality and poverty",
            "Friendship between the Prince and the swallow",
            "True value — love over material beauty",
        ],
        "ncert_fact": (
            "The statue of the Happy Prince, covered in gold and jewels, asks a migrating "
            "swallow to distribute his riches to the city's poor — his ruby eyes, gold "
            "leaf, and sapphire sword-hilt. The swallow delays migration and eventually "
            "dies of cold. God declares both the dead swallow and the Prince's lead heart "
            "the most precious things in the city."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "The Prince's compassionate gaze — from his pedestal he sees the suffering "
            "hidden from the comfortable — is the essence of social awareness: truly "
            "seeing others' pain and being moved to act, at personal cost."
        ),
    },
    {
        "chapter_name": "Weathering the Storm in Ersama",
        "book": "Moments (Supplementary)",
        "author": "Harsh Mander",
        "topics": [
            "Super cyclone of 1999 in Odisha",
            "Survival and community resilience",
            "Leadership and courage in disaster",
            "Relief efforts and human solidarity",
        ],
        "ncert_fact": (
            "Prashant, a young man caught in the 1999 Odisha super cyclone, survives "
            "by clinging to a tree for two days. He returns to his devastated village "
            "and transforms personal grief into community action — organising rescue, "
            "food distribution, and relief with remarkable leadership."
        ),
        "sel_dimension": "persistence",
        "sel_connection": (
            "Prashant's transformation from a frightened survivor into a community "
            "leader — channelling grief into organised action — is a vivid example of "
            "persistence fuelled by a sense of responsibility to others."
        ),
    },
    {
        "chapter_name": "The Last Leaf",
        "book": "Moments (Supplementary)",
        "author": "O. Henry",
        "topics": [
            "Hope and the will to live",
            "Friendship and self-sacrifice",
            "Art as an act of love",
            "Irony in the story's resolution",
        ],
        "ncert_fact": (
            "Johnsy, ill with pneumonia, believes she will die when the last ivy leaf on "
            "the wall falls. Old Behrman, a failed artist, secretly paints a masterpiece "
            "leaf on the wall on a stormy night to save her will to live. He dies of "
            "pneumonia, but Johnsy recovers — his final painting is his greatest work "
            "and his greatest act of love."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Behrman's ultimate self-sacrifice — giving his life so that a stranger "
            "might find the hope to live — is one of the curriculum's most moving "
            "examples of social awareness expressed through selfless love."
        ),
    },
    {
        "chapter_name": "A House Is Not a Home",
        "book": "Moments (Supplementary)",
        "author": "Zan Gaudioso",
        "topics": [
            "Loss and starting over",
            "The meaning of home and belonging",
            "Teenage identity and social adjustment",
            "Role of pets in emotional well-being",
        ],
        "ncert_fact": (
            "A teenage boy's house burns down, destroying all his possessions including "
            "his beloved cat. He struggles to fit into a new school and feels utterly "
            "lost. When his cat is miraculously found and returned by a kind neighbour, "
            "his sense of belonging is restored — showing that 'home' is about love "
            "and connection more than physical space."
        ),
        "sel_dimension": "emotional_regulation",
        "sel_connection": (
            "The boy's emotional journey — grief, isolation, and eventual healing — "
            "illustrates how emotional regulation involves tolerating loss and gradually "
            "rebuilding connection rather than suppressing pain."
        ),
    },
    {
        "chapter_name": "The Accidental Tourist",
        "book": "Moments (Supplementary)",
        "author": "Bill Bryson",
        "topics": [
            "Humour and self-deprecation",
            "Travel mishaps and clumsiness",
            "Observational comedy",
        ],
        "ncert_fact": (
            "Bill Bryson humorously recounts his many travel disasters — spilling drinks "
            "on fellow passengers, getting tangled in headphone wires, struggling with "
            "luggage systems — with warm self-deprecating wit. The essay celebrates "
            "the comedy of ordinary incompetence and the human ability to laugh at oneself."
        ),
        "sel_dimension": "self_awareness",
        "sel_connection": (
            "Bryson's cheerful self-mockery is an example of healthy self-awareness — "
            "acknowledging one's own flaws and limitations with humour rather than "
            "defensiveness or shame."
        ),
    },
    {
        "chapter_name": "The Beggar",
        "book": "Moments (Supplementary)",
        "author": "Anton Chekhov",
        "topics": [
            "Transformation through work and dignity",
            "Compassion and rehabilitation",
            "Honesty vs. pretence",
            "Role of human kindness in changing lives",
        ],
        "ncert_fact": (
            "Lushkoff, a beggar who makes up false stories to get alms, is caught by a "
            "lawyer named Skvortsov who puts him to work chopping wood. Later, Lushkoff "
            "becomes a notary — and confesses that it was not Skvortsov but his cook "
            "Olga, who chopped his wood for him out of pity, whose tears and kindness "
            "truly transformed him."
        ),
        "sel_dimension": "social_awareness",
        "sel_connection": (
            "Olga's silent compassion — working on behalf of a stranger without credit "
            "or reward — highlights the deepest form of social awareness: seeing the "
            "humanity in someone others have dismissed and acting on that recognition."
        ),
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Helper: simple keyword overlap scorer
# ─────────────────────────────────────────────────────────────────────────────

def _score(chapter: dict, topic_lower: str) -> int:
    """
    Return a match score between a topic string and a chapter dict.
    Higher is better.
    """
    score = 0
    name_lower = chapter["chapter_name"].lower()
    # Direct substring match on chapter name is strongest signal
    if topic_lower in name_lower:
        score += 10
    # Partial word overlap on chapter name
    for word in topic_lower.split():
        if len(word) > 3 and word in name_lower:
            score += 4
    # Match against topics list
    for t in chapter.get("topics", []):
        t_lower = t.lower()
        if topic_lower in t_lower:
            score += 5
        for word in topic_lower.split():
            if len(word) > 3 and word in t_lower:
                score += 2
    # Match against ncert_fact
    fact_lower = chapter.get("ncert_fact", "").lower()
    for word in topic_lower.split():
        if len(word) > 4 and word in fact_lower:
            score += 1
    return score


# ─────────────────────────────────────────────────────────────────────────────
# Per-subject context builders
# ─────────────────────────────────────────────────────────────────────────────

def _format_chapter(ch: dict) -> str:
    """Render a single chapter dict as a grounding block."""
    lines = [
        f"Chapter: {ch['chapter_name']}",
        f"Topics: {'; '.join(ch['topics'])}",
        f"NCERT Fact: {ch['ncert_fact']}",
        f"SEL Dimension: {ch['sel_dimension']}",
        f"SEL Connection: {ch['sel_connection']}",
    ]
    return "\n".join(lines)


def get_science9_context(topic: str) -> str:
    """
    Fuzzy-match topic against SCIENCE9_DATA chapter names/topics.
    Returns a formatted grounding string for injection into generation prompts.
    """
    t = topic.lower()
    scored = sorted(SCIENCE9_DATA, key=lambda ch: _score(ch, t), reverse=True)
    best = scored[0]
    second = scored[1] if len(scored) > 1 else None

    lines = [
        "=== NCERT Class 9 Science — Chapter Reference ===",
        f"Teacher topic: \"{topic}\"",
        "",
        "BEST MATCH:",
        _format_chapter(best),
    ]

    # Include a second match only if it scores meaningfully
    if second and _score(second, t) >= 3:
        lines += ["", "ALSO RELEVANT:", _format_chapter(second)]

    lines += [
        "",
        "All Class 9 Science chapters for reference:",
        " | ".join(ch["chapter_name"] for ch in SCIENCE9_DATA),
        "",
        "=== END Science Reference ===",
    ]
    return "\n".join(lines)


def get_math9_context(topic: str) -> str:
    """
    Fuzzy-match topic against MATH9_DATA chapter names/topics.
    Returns a formatted grounding string.
    """
    t = topic.lower()
    scored = sorted(MATH9_DATA, key=lambda ch: _score(ch, t), reverse=True)
    best = scored[0]
    second = scored[1] if len(scored) > 1 else None

    lines = [
        "=== NCERT Class 9 Mathematics — Chapter Reference ===",
        f"Teacher topic: \"{topic}\"",
        "",
        "BEST MATCH:",
        _format_chapter(best),
    ]

    if second and _score(second, t) >= 3:
        lines += ["", "ALSO RELEVANT:", _format_chapter(second)]

    lines += [
        "",
        "All Class 9 Mathematics chapters for reference:",
        " | ".join(ch["chapter_name"] for ch in MATH9_DATA),
        "",
        "=== END Mathematics Reference ===",
    ]
    return "\n".join(lines)


def get_social9_context(topic: str) -> str:
    """
    Fuzzy-match topic against SOCIAL9_DATA (all 4 books combined).
    Returns a formatted grounding string.
    """
    t = topic.lower()
    scored = sorted(SOCIAL9_DATA, key=lambda ch: _score(ch, t), reverse=True)
    best = scored[0]
    second = scored[1] if len(scored) > 1 else None

    lines = [
        "=== NCERT Class 9 Social Science — Chapter Reference ===",
        "(Books: History 'India and the Contemporary World I' | Geography 'Contemporary India I'"
        " | Economics | Political Science 'Democratic Politics I')",
        f"Teacher topic: \"{topic}\"",
        "",
        "BEST MATCH:",
        f"Book: {best.get('book', 'Social Science')}",
        _format_chapter(best),
    ]

    if second and _score(second, t) >= 3:
        lines += [
            "",
            "ALSO RELEVANT:",
            f"Book: {second.get('book', 'Social Science')}",
            _format_chapter(second),
        ]

    lines += [
        "",
        "All Class 9 Social Science chapters for reference:",
    ]
    for book in ["History", "Geography", "Economics", "Political Science"]:
        book_chs = [ch["chapter_name"] for ch in SOCIAL9_DATA if ch.get("book") == book]
        if book_chs:
            lines.append(f"  {book}: {' | '.join(book_chs)}")

    lines += ["", "=== END Social Science Reference ==="]
    return "\n".join(lines)


def get_english9_context(topic: str) -> str:
    """
    Fuzzy-match topic against ENGLISH9_DATA chapter names/topics.
    Returns a formatted grounding string.
    """
    t = topic.lower()
    scored = sorted(ENGLISH9_DATA, key=lambda ch: _score(ch, t), reverse=True)
    best = scored[0]
    second = scored[1] if len(scored) > 1 else None

    lines = [
        "=== NCERT Class 9 English — Chapter Reference ===",
        "(Beehive: Prose + Poems | Moments: Supplementary Reader)",
        f"Teacher topic: \"{topic}\"",
        "",
        "BEST MATCH:",
        f"Book: {best.get('book', 'Beehive/Moments')}",
    ]
    if "author" in best:
        lines.append(f"Author: {best['author']}")
    lines.append(_format_chapter(best))

    if second and _score(second, t) >= 3:
        lines += [
            "",
            "ALSO RELEVANT:",
            f"Book: {second.get('book', 'Beehive/Moments')}",
        ]
        if "author" in second:
            lines.append(f"Author: {second['author']}")
        lines.append(_format_chapter(second))

    lines += [
        "",
        "All Class 9 English chapters for reference:",
    ]
    for book_label in ["Beehive (Prose)", "Beehive (Poem)", "Moments (Supplementary)"]:
        chs = [ch["chapter_name"] for ch in ENGLISH9_DATA if ch.get("book") == book_label]
        if chs:
            lines.append(f"  {book_label}: {' | '.join(chs)}")

    lines += ["", "=== END English Reference ==="]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# Master router
# ─────────────────────────────────────────────────────────────────────────────

def get_class9_context(subject: str, topic: str) -> str:
    """
    Route to the correct subject context builder for Class 9.

    Parameters
    ----------
    subject : str
        One of 'science', 'math' / 'maths' / 'mathematics',
        'social' / 'social science' / 'history' / 'geography' /
        'economics' / 'political science' / 'civics',
        'english', or 'hindi'.
    topic : str
        The chapter name, concept, or query string from the teacher.

    Returns
    -------
    str
        A formatted grounding block ready for prompt injection.
    """
    s = subject.lower().strip()

    if any(kw in s for kw in ["science", "physics", "chemistry", "biology",
                               "विज्ञान", "साइंस"]):
        return get_science9_context(topic)

    if any(kw in s for kw in ["math", "maths", "mathematics", "गणित"]):
        return get_math9_context(topic)

    if any(kw in s for kw in ["social", "history", "geography", "economics",
                               "political", "civics", "sst",
                               "इतिहास", "भूगोल", "अर्थशास्त्र", "राजनीति"]):
        return get_social9_context(topic)

    if any(kw in s for kw in ["english", "beehive", "moments", "अंग्रेजी"]):
        return get_english9_context(topic)

    if any(kw in s for kw in ["hindi", "हिंदी", "हिन्दी", "kshitij", "kritika"]):
        # Delegate to the existing detailed Hindi 9 module
        try:
            from ncert_data import get_hindi9_context
            return get_hindi9_context(topic)
        except ImportError:
            import os
            import sys
            sys.path.insert(0, os.path.dirname(__file__))
            from ncert_data import get_hindi9_context
            return get_hindi9_context(topic)

    # Fallback: try all subjects and return the best scoring one
    all_results = {
        "Science":        get_science9_context(topic),
        "Mathematics":    get_math9_context(topic),
        "Social Science": get_social9_context(topic),
        "English":        get_english9_context(topic),
    }
    # Return science as default safe fallback
    return (
        f"=== NCERT Class 9 — Subject could not be determined from '{subject}' ===\n"
        "Please specify one of: Science, Mathematics, Social Science, English, Hindi.\n\n"
        + "\n\n---\n\n".join(all_results.values())
    )
