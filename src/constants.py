class ENCOUNTER:
    ULDUAR_IDS = {
        'Flame Leviathan': 744,
        'Ignis the Furnace Master': 745,
        'Razorscale': 746,
        'XT-002 Deconstructor': 747,
        'The Assembly of Iron': 748,
        'Kologarn': 749,
        'Auriaya': 750,
        'Hodir': 751,
        'Thorim': 752,
        'Freya': 753,
        'Mimiron': 754,
        'General Vezax': 755,
        'Yogg-Saron': 756,
        'Algalon the Observer': 757,
    }

    TOGC_IDS = {
        'The Northrend Beasts': 629,
        'Lord Jaraxxus': 633,
        'Faction Champions': 637,
        "Twin Val'kyr": 641,
        "Anub'arak": 645,
    }

    ICC_IDS = {
        'Lord Marrowgar': 845,
        'Lady Deathwhisper': 846,
        'Icecrown Gunship Battle': 847,
        'Deathbringer Saurfang': 848,
        'Festergut': 849,
        'Rotface': 850,
        'Professor Putricide': 851,
        'Blood Council': 852,
        "Blood-Queen Lana'thel": 853,
        'Valithria Dreamwalker': 854,
        'Sindragosa': 855,
        'The Lich King': 856,
    }

    IDS = {**ULDUAR_IDS, **TOGC_IDS, **ICC_IDS}
    NAMES = {id: name for name, id in IDS.items()}

    @staticmethod
    def get_id(name: str) -> int:
        if name not in ENCOUNTER.IDS:
            raise ValueError(f"Unknown encounter name: {name}")
        return ENCOUNTER.IDS[name]

    @staticmethod
    def get_name(id: int) -> str:
        if id not in ENCOUNTER.NAMES:
            raise ValueError(f"Unknown encounter ID: {id}")
        return ENCOUNTER.NAMES[id]
