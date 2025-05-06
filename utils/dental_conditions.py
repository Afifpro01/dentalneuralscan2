def get_dental_conditions(language):
    """
    Get a list of dental conditions in the specified language.
    
    Args:
        language: The language code ('en' for English, 'id' for Indonesian)
        
    Returns:
        A list of dictionaries containing dental condition information
    """
    # English condition definitions
    conditions_en = [
        {
            "id": 0,
            "name": "Enamel Damage (Early Stage)",
            "symptoms": [
                "No pain",
                "White spots on tooth surface (White spot lesions)",
                "If untreated: will worsen with small indentations or rough surface"
            ],
            "solutions": [
                "Remineralization with fluoride application (Gel, varnish, mouthwash)",
                "Education: Maintain oral hygiene, avoid excessive sweet/acidic foods",
                "Regular dental check-ups"
            ],
            "severity_level": 1
        },
        {
            "id": 1,
            "name": "Enamel Decay (Moderate)",
            "symptoms": [
                "Slight sensitivity to sweet foods or cold drinks",
                "Visible light brown discoloration",
                "Slight discomfort when eating",
                "Small visible cavities"
            ],
            "solutions": [
                "Dental filling",
                "Fluoride treatment",
                "Improved oral hygiene routine",
                "Dietary changes to reduce sugar intake"
            ],
            "severity_level": 2
        },
        {
            "id": 2,
            "name": "Dentin Decay",
            "symptoms": [
                "Tooth sensitivity",
                "Pain when consuming sweet, hot, or cold foods",
                "Visible dark brown or black spots on teeth",
                "Toothache or pain when biting down"
            ],
            "solutions": [
                "Dental filling or restoration",
                "Possible need for dental crown",
                "Prescription-strength fluoride toothpaste",
                "Regular professional cleanings"
            ],
            "severity_level": 3
        },
        {
            "id": 3,
            "name": "Pulp Involvement",
            "symptoms": [
                "Severe, persistent toothache",
                "Pain that disrupts sleep",
                "Sensitivity to temperature changes",
                "Pain when chewing or biting",
                "Swelling of the gum near the affected tooth"
            ],
            "solutions": [
                "Root canal treatment",
                "Antibiotics if infection is present",
                "Pain management",
                "Possible dental crown after treatment"
            ],
            "severity_level": 4
        },
        {
            "id": 4,
            "name": "Abscess Formation",
            "symptoms": [
                "Severe, throbbing pain",
                "Swelling in the face or cheek",
                "Tender, swollen lymph nodes under the jaw",
                "Fever",
                "Bad taste in the mouth due to draining pus"
            ],
            "solutions": [
                "Urgent dental treatment",
                "Drainage of the abscess",
                "Root canal therapy or tooth extraction",
                "Antibiotics to clear infection",
                "Pain management medication"
            ],
            "severity_level": 5
        }
    ]
    
    # Indonesian condition definitions
    conditions_id = [
        {
            "id": 0,
            "name": "Kerusakan pada Enamel (Tahap Awal)",
            "symptoms": [
                "Tidak menimbulkan nyeri",
                "Permukaan gigi mulai tampak bercak putih (White spot lesion)",
                "Jika dibiarkan: akan memburuk dengan tampak cekungan kecil atau permukaan kasar"
            ],
            "solutions": [
                "Remineralisasi dengan fluoride tropical (Gel, varnish, mouthwash)",
                "Edukasi: Jaga Kebersihan Mulut, hindari makanan manis/asam berlebihan",
                "Pemeriksaan gigi rutin"
            ],
            "severity_level": 1
        },
        {
            "id": 1,
            "name": "Kerusakan Enamel (Sedang)",
            "symptoms": [
                "Sedikit sensitif terhadap makanan manis atau minuman dingin",
                "Perubahan warna kecoklatan yang terlihat",
                "Sedikit tidak nyaman saat makan",
                "Lubang kecil yang terlihat"
            ],
            "solutions": [
                "Tambal gigi",
                "Perawatan fluoride",
                "Peningkatan rutinitas kebersihan mulut",
                "Perubahan pola makan untuk mengurangi asupan gula"
            ],
            "severity_level": 2
        },
        {
            "id": 2,
            "name": "Kerusakan Dentin",
            "symptoms": [
                "Gigi sensitif",
                "Nyeri saat mengonsumsi makanan manis, panas, atau dingin",
                "Bintik coklat tua atau hitam yang terlihat pada gigi",
                "Sakit gigi atau nyeri saat menggigit"
            ],
            "solutions": [
                "Tambal gigi atau restorasi",
                "Kemungkinan memerlukan mahkota gigi",
                "Pasta gigi fluoride dengan resep dokter",
                "Pembersihan profesional secara rutin"
            ],
            "severity_level": 3
        },
        {
            "id": 3,
            "name": "Keterlibatan Pulpa",
            "symptoms": [
                "Sakit gigi parah dan terus-menerus",
                "Nyeri yang mengganggu tidur",
                "Sensitif terhadap perubahan suhu",
                "Nyeri saat mengunyah atau menggigit",
                "Pembengkakan gusi di dekat gigi yang terkena"
            ],
            "solutions": [
                "Perawatan saluran akar",
                "Antibiotik jika ada infeksi",
                "Manajemen nyeri",
                "Kemungkinan mahkota gigi setelah perawatan"
            ],
            "severity_level": 4
        },
        {
            "id": 4,
            "name": "Pembentukan Abses",
            "symptoms": [
                "Nyeri parah dan berdenyut",
                "Pembengkakan di wajah atau pipi",
                "Kelenjar getah bening yang bengkak dan nyeri di bawah rahang",
                "Demam",
                "Rasa tidak enak di mulut karena nanah yang mengalir"
            ],
            "solutions": [
                "Perawatan gigi darurat",
                "Drainase abses",
                "Terapi saluran akar atau pencabutan gigi",
                "Antibiotik untuk mengatasi infeksi",
                "Obat pereda nyeri"
            ],
            "severity_level": 5
        }
    ]
    
    # Return the appropriate language set
    if language == 'id':
        return conditions_id
    else:
        return conditions_en
