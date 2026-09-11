#!/usr/bin/env python
import os
import django
import random
from datetime import datetime, timedelta, date
from decimal import Decimal
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ip_sakti.settings')
django.setup()

from ip_sakti.models import (
    User, State, AYUSHFormulation, GITag, Patent, BiopiracyCase,
    Alert, TKDL_Entry, DashboardStat, IPActivity
)


def seed_users():
    print("Seeding users...")
    users_data = [
        {'email': 'admin@ipsakti.gov.in', 'first_name': 'Rajesh', 'last_name': 'Kumar', 'role': 'ADMIN', 'ministry_department': 'AYUSH', 'password': 'admin123'},
        {'email': 'official@ipsakti.gov.in', 'first_name': 'Priya', 'last_name': 'Sharma', 'role': 'MINISTRY', 'ministry_department': 'AYUSH', 'password': 'official123'},
        {'email': 'analyst@ipsakti.gov.in', 'first_name': 'Arun', 'last_name': 'Verma', 'role': 'ANALYST', 'ministry_department': 'CSIR', 'password': 'analyst123'},
        {'email': 'viewer@ipsakti.gov.in', 'first_name': 'Sneha', 'last_name': 'Patel', 'role': 'VIEWER', 'ministry_department': 'AYUSH', 'password': 'viewer123'},
    ]
    for user_data in users_data:
        if not User.objects.filter(email=user_data['email']).exists():
            data = dict(user_data)
            data['username'] = data['email'].split('@')[0]
            User.objects.create_user(**data)
            print(f"  Created: {user_data['email']}")


def seed_states():
    print("Seeding states...")
    states_data = [
        {'name': 'Kerala', 'code': 'KL', 'region': 'SOUTH', 'ayush_council_name': 'Kerala State AYUSH Society', 'population': 35000000, 'latitude': 10.8505, 'longitude': 76.2711},
        {'name': 'Tamil Nadu', 'code': 'TN', 'region': 'SOUTH', 'ayush_council_name': 'Tamil Nadu State AYUSH Department', 'population': 72000000, 'latitude': 11.1271, 'longitude': 78.6569},
        {'name': 'Karnataka', 'code': 'KA', 'region': 'SOUTH', 'ayush_council_name': 'Karnataka AYUSH Department', 'population': 61000000, 'latitude': 15.3173, 'longitude': 75.7139},
        {'name': 'Andhra Pradesh', 'code': 'AP', 'region': 'SOUTH', 'ayush_council_name': 'AP AYUSH Department', 'population': 53000000, 'latitude': 15.9129, 'longitude': 79.7400},
        {'name': 'Telangana', 'code': 'TS', 'region': 'SOUTH', 'ayush_council_name': 'Telangana AYUSH Department', 'population': 38000000, 'latitude': 18.1124, 'longitude': 79.0193},
        {'name': 'Maharashtra', 'code': 'MH', 'region': 'WEST', 'ayush_council_name': 'Maharashtra AYUSH Directorate', 'population': 112000000, 'latitude': 19.7515, 'longitude': 75.7139},
        {'name': 'Gujarat', 'code': 'GJ', 'region': 'WEST', 'ayush_council_name': 'Gujarat AYUSH Department', 'population': 60000000, 'latitude': 22.2587, 'longitude': 71.1924},
        {'name': 'Rajasthan', 'code': 'RJ', 'region': 'WEST', 'ayush_council_name': 'Rajasthan AYUSH Department', 'population': 68000000, 'latitude': 27.0238, 'longitude': 74.2179},
        {'name': 'Uttar Pradesh', 'code': 'UP', 'region': 'CENTRAL', 'ayush_council_name': 'UP AYUSH Department', 'population': 200000000, 'latitude': 26.8467, 'longitude': 80.9462},
        {'name': 'Madhya Pradesh', 'code': 'MP', 'region': 'CENTRAL', 'ayush_council_name': 'MP AYUSH Department', 'population': 72000000, 'latitude': 22.9734, 'longitude': 78.6569},
        {'name': 'West Bengal', 'code': 'WB', 'region': 'EAST', 'ayush_council_name': 'West Bengal AYUSH Department', 'population': 91000000, 'latitude': 22.9868, 'longitude': 87.8550},
        {'name': 'Odisha', 'code': 'OD', 'region': 'EAST', 'ayush_council_name': 'Odisha AYUSH Department', 'population': 42000000, 'latitude': 20.9517, 'longitude': 85.0985},
        {'name': 'Bihar', 'code': 'BR', 'region': 'EAST', 'ayush_council_name': 'Bihar AYUSH Department', 'population': 104000000, 'latitude': 25.0961, 'longitude': 85.3131},
        {'name': 'Jharkhand', 'code': 'JH', 'region': 'EAST', 'ayush_council_name': 'Jharkhand AYUSH Department', 'population': 33000000, 'latitude': 23.6102, 'longitude': 85.2799},
        {'name': 'Chhattisgarh', 'code': 'CG', 'region': 'CENTRAL', 'ayush_council_name': 'Chhattisgarh AYUSH Department', 'population': 25000000, 'latitude': 21.2787, 'longitude': 81.8661},
        {'name': 'Assam', 'code': 'AS', 'region': 'NORTHEAST', 'ayush_council_name': 'Assam AYUSH Department', 'population': 31000000, 'latitude': 26.2006, 'longitude': 92.9376},
        {'name': 'Himachal Pradesh', 'code': 'HP', 'region': 'NORTH', 'ayush_council_name': 'HP AYUSH Department', 'population': 6800000, 'latitude': 31.1048, 'longitude': 77.1734},
        {'name': 'Uttarakhand', 'code': 'UK', 'region': 'NORTH', 'ayush_council_name': 'Uttarakhand AYUSH Department', 'population': 10000000, 'latitude': 30.0668, 'longitude': 79.0193},
        {'name': 'Punjab', 'code': 'PB', 'region': 'NORTH', 'ayush_council_name': 'Punjab AYUSH Department', 'population': 27000000, 'latitude': 31.1471, 'longitude': 75.3412},
        {'name': 'Haryana', 'code': 'HR', 'region': 'NORTH', 'ayush_council_name': 'Haryana AYUSH Department', 'population': 25000000, 'latitude': 29.0588, 'longitude': 76.0856},
        {'name': 'Delhi', 'code': 'DL', 'region': 'NORTH', 'ayush_council_name': 'Delhi AYUSH Department', 'population': 16000000, 'latitude': 28.6139, 'longitude': 77.2090},
    ]
    for state_data in states_data:
        State.objects.get_or_create(code=state_data['code'], defaults=state_data)
    print(f"  Created {len(states_data)} states")


def seed_formulations():
    print("Seeding AYUSH formulations...")
    formulations = [
        {'name': 'Chyawanprash', 'sanskrit_name': 'च्यवनप्राश', 'category': 'AYURVEDA', 'ingredients': ['Amla', 'Ashwagandha', 'Shatavari', 'Giloy', 'Honey', 'Ghee'], 'preparation_method': 'Traditional preparation with herbs and ghee', 'source_text': 'Charaka Samhita', 'text_reference': 'Chikitsa Sthana', 'indication': 'Immunity booster', 'therapeutic_uses': 'Improves digestion, boosts immunity, respiratory health', 'is_registered': True, 'registration_number': 'AYU/REG/2020/001'},
        {'name': 'Kashayam', 'sanskrit_name': 'कशायम्', 'category': 'AYURVEDA', 'ingredients': ['Ginger', 'Black Pepper', 'Long Pepper', 'Honey'], 'preparation_method': 'Decoction method', 'source_text': 'Sushruta Samhita', 'text_reference': 'Sutra Sthana', 'indication': 'Fever, respiratory disorders', 'therapeutic_uses': 'Antipyretic, anti-inflammatory', 'is_registered': True, 'registration_number': 'AYU/REG/2020/002'},
        {'name': 'Dashamula', 'sanskrit_name': 'दशमूल', 'category': 'AYURVEDA', 'ingredients': ['Bilva', 'Agnimantha', 'Shyonaka', 'Gambhari', 'Patala', 'Gambhari', 'Brihati', 'Kantakari', 'Goksura', 'Shalaparni'], 'preparation_method': 'Decoction from ten roots', 'source_text': 'Charaka Samhita', 'text_reference': 'Sutra Sthana', 'indication': 'Fever, inflammation', 'therapeutic_uses': 'Anti-inflammatory, antipyretic', 'is_registered': True, 'registration_number': 'AYU/REG/2020/003'},
        {'name': 'Triphala', 'sanskrit_name': 'त्रिफला', 'category': 'AYURVEDA', 'ingredients': ['Haritaki', 'Bibhitaki', 'Amalaki'], 'preparation_method': 'Powdered form', 'source_text': 'Charaka Samhita', 'text_reference': 'Chikitsa Sthana', 'indication': 'Digestive health', 'therapeutic_uses': 'Digestive aid, antioxidant', 'is_registered': True, 'registration_number': 'AYU/REG/2020/004'},
        {'name': 'Brahmi Ghrita', 'sanskrit_name': 'ब्राह्मी घृत', 'category': 'AYURVEDA', 'ingredients': ['Brahmi', 'Ghee', 'Honey'], 'preparation_method': 'Ghee-based preparation', 'source_text': 'Ashtanga Hridaya', 'text_reference': 'Kalpa Sthana', 'indication': 'Memory enhancement', 'therapeutic_uses': 'Nootropic, cognitive enhancement', 'is_registered': True, 'registration_number': 'AYU/REG/2020/005'},
        {'name': 'Siddha Kayakalpa', 'sanskrit_name': 'சித்த காயகல்ப', 'category': 'SIDDHA', 'ingredients': ['Herbal decoctions', 'Mineral preparations', 'Metals'], 'preparation_method': 'Traditional Siddha method', 'source_text': 'Agastyar Hridayam', 'text_reference': 'Pooja Sthana', 'indication': 'Rejuvenation therapy', 'therapeutic_uses': 'Anti-aging, longevity', 'is_registered': True, 'registration_number': 'SID/REG/2020/001'},
        {'name': 'Unani Itrifal', 'sanskrit_name': 'اترہال', 'category': 'UNANI', 'ingredients': ['Emblica', 'Terminalia bellirica', 'Terminalia chebula'], 'preparation_method': 'Powdered form', 'source_text': 'Canon of Medicine', 'text_reference': 'Volume 1', 'indication': 'Digestive health', 'therapeutic_uses': 'Digestive tonic, antioxidant', 'is_registered': True, 'registration_number': 'UNA/REG/2020/001'},
        {'name': 'Homoeopathic Arsenicum Album', 'sanskrit_name': 'Arsenicum Album', 'category': 'HOMOEOPATHY', 'ingredients': ['Arsenic trioxide'], 'preparation_method': 'Potentization', 'source_text': 'Materia Medica', 'text_reference': 'Hahnemann', 'indication': 'Digestive disorders', 'therapeutic_uses': 'Anti-inflammatory', 'is_registered': True, 'registration_number': 'HOM/REG/2020/001'},
        {'name': 'Yoga Pranayama', 'sanskrit_name': 'प्राणायाम', 'category': 'YOGA', 'ingredients': [], 'preparation_method': 'Breathing techniques', 'source_text': 'Hatha Yoga Pradipika', 'text_reference': 'Chapter 2', 'indication': 'Stress relief', 'therapeutic_uses': 'Mental health, respiratory', 'is_registered': True, 'registration_number': 'YOG/REG/2020/001'},
    ]

    states = list(State.objects.all())
    for form_data in formulations:
        state = random.choice(states)
        form_data['state_of_origin'] = state
        form_data['digitized_in_tkdl'] = random.choice([True, False])
        if form_data['digitized_in_tkdl']:
            form_data['tkdl_entry_date'] = timezone.now().date() - timedelta(days=random.randint(30, 365))
        AYUSHFormulation.objects.get_or_create(
            name=form_data['name'],
            defaults=form_data
        )
    print(f"  Created {len(formulations)} formulations")


def seed_gi_tags():
    print("Seeding GI tags...")
    gi_tags_data = [
        {'name': 'Darjeeling Tea', 'product': 'Tea', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Tea Board India', 'registration_number': 'GI-001'},
        {'name': 'Basmati Rice', 'product': 'Rice', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'APEDA', 'registration_number': 'GI-002'},
        {'name': 'Mysore Silk', 'product': 'Textile', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Silk Board', 'registration_number': 'GI-003'},
        {'name': 'Kanchipuram Silk Saree', 'product': 'Textile', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Weavers Cooperative', 'registration_number': 'GI-004'},
        {'name': 'Araria Banana', 'product': 'Banana', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Bihar Horticulture', 'registration_number': 'GI-005'},
        {'name': 'Alleppey Green Cardamom', 'product': 'Spice', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Spices Board', 'registration_number': 'GI-006'},
        {'name': 'Coimbatore Wet Grinder', 'product': 'Appliances', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Tamil Nadu Industries', 'registration_number': 'GI-007'},
        {'name': 'Mekhela Chador', 'product': 'Textile', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Assam Weavers', 'registration_number': 'GI-008'},
        {'name': 'Pashmina Shawl', 'product': 'Textile', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Kashmir Artisans', 'registration_number': 'GI-009'},
        {'name': 'Mysore Sandalwood Oil', 'product': 'Essential Oil', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'Karnataka Forest Dept', 'registration_number': 'GI-010'},
        {'name': 'Kerala Coconut Oil', 'product': 'Oil', 'category': 'AYURVEDA', 'status': 'PENDING', 'applicant': 'Kerala Coconut Board', 'registration_number': 'GI-011'},
        {'name': 'Rajasthan Blue Pottery', 'product': 'Handicraft', 'category': 'AYURVEDA', 'status': 'PENDING', 'applicant': 'Rajasthan Handicrafts', 'registration_number': 'GI-012'},
        {'name': 'Aranmula Kannadi', 'product': 'Handicraft', 'category': 'AYURVEDA', 'status': 'EXAMINED', 'applicant': 'Kerala Handicrafts', 'registration_number': 'GI-013'},
        {'name': 'Nirmal Furniture', 'product': 'Furniture', 'category': 'AYURVEDA', 'status': 'PENDING', 'applicant': 'Telangana Handicrafts', 'registration_number': 'GI-014'},
        {'name': 'Srikalahasti Kalamkari', 'product': 'Textile', 'category': 'AYURVEDA', 'status': 'REGISTERED', 'applicant': 'AP Handlooms', 'registration_number': 'GI-015'},
    ]

    for gi_data in gi_tags_data:
        states = State.objects.filter(code__in=['KL', 'WB', 'KA', 'TN', 'AS', 'RJ', 'TS', 'AP', 'GJ', 'HP'])
        state = random.choice(list(states))
        gi_data['state'] = state
        gi_data['issued_date'] = date(2020, 1, 1) + timedelta(days=random.randint(0, 1500))
        GITag.objects.get_or_create(
            registration_number=gi_data['registration_number'],
            defaults=gi_data
        )
    print(f"  Created {len(gi_tags_data)} GI tags")


def seed_patents():
    print("Seeding patents...")
    patents_data = [
        {'title': 'Novel Ayurvedic Formulation for Diabetes Management', 'applicant': 'CSIR-IMTECH', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2019-05-15', 'is_biopiracy_suspect': False},
        {'title': 'Herbal Composition for treating respiratory disorders', 'applicant': 'University of Mysore', 'country': 'IN', 'status': 'PUBLISHED', 'ayush_category': 'AYURVEDA', 'filing_date': '2021-08-20', 'is_biopiracy_suspect': False},
        {'title': 'Traditional Turmeric-based wound healing composition', 'applicant': 'CSIR-CIMAP', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2018-03-10', 'is_biopiracy_suspect': False},
        {'title': 'Method for preparing standardized Ashwagandha extract', 'applicant': 'CSIR-CDRI', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2017-11-05', 'is_biopiracy_suspect': False},
        {'title': 'Yoga-based therapy for stress management', 'applicant': 'Morarji Desai National Institute of Yoga', 'country': 'IN', 'status': 'PUBLISHED', 'ayush_category': 'YOGA', 'filing_date': '2022-01-15', 'is_biopiracy_suspect': False},
        {'title': 'Novel Homoeopathic formulation for skin diseases', 'applicant': 'Central Council for Research in Homoeopathy', 'country': 'IN', 'status': 'FILED', 'ayush_category': 'HOMOEOPATHY', 'filing_date': '2023-06-20', 'is_biopiracy_suspect': False},
        {'title': 'Siddha herbal formulation for arthritis', 'applicant': 'Central Council for Research in Siddha', 'country': 'IN', 'status': 'PUBLISHED', 'ayush_category': 'SIDDHA', 'filing_date': '2020-09-10', 'is_biopiracy_suspect': False},
        {'title': 'Unani formulation for digestive disorders', 'applicant': 'CCRUM', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'UNANI', 'filing_date': '2016-04-25', 'is_biopiracy_suspect': False},
        {'title': 'Herbal Anticancer composition from Ayurvedic plants', 'applicant': 'Bharat Biotech', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2015-07-30', 'is_biopiracy_suspect': False},
        {'title': 'Immunomodulatory herbal formulation', 'applicant': 'Zandu Pharmaceuticals', 'country': 'IN', 'status': 'FILED', 'ayush_category': 'AYURVEDA', 'filing_date': '2023-11-01', 'is_biopiracy_suspect': False},
        {'title': 'Curcumin-based pharmaceutical composition', 'applicant': 'University of Kerala', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2014-02-14', 'is_biopiracy_suspect': False},
        {'title': 'Neem-based pesticide composition', 'applicant': 'TERI', 'country': 'IN', 'status': 'PUBLISHED', 'ayush_category': 'AYURVEDA', 'filing_date': '2021-05-20', 'is_biopiracy_suspect': False},
        {'title': 'Ayurvedic anti-aging formulation', 'applicant': 'Patanjali Ayurved', 'country': 'IN', 'status': 'FILED', 'ayush_category': 'AYURVEDA', 'filing_date': '2022-08-15', 'is_biopiracy_suspect': False},
        {'title': 'Traditional Neem tooth powder', 'applicant': 'Ministry of AYUSH', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2013-09-01', 'is_biopiracy_suspect': False},
        {'title': 'Herbal cough syrup formulation', 'applicant': 'Dabur India', 'country': 'IN', 'status': 'GRANTED', 'ayush_category': 'AYURVEDA', 'filing_date': '2012-12-10', 'is_biopiracy_suspect': False},
    ]

    for pat_data in patents_data:
        pat_data.setdefault('application_number', f"IN/{2024}/{random.randint(10000, 99999)}")
        pat_data.setdefault('assignee', pat_data['applicant'])
        pat_data.setdefault('abstract', f"Novel {pat_data['ayush_category'].lower()} formulation...")
        Patent.objects.get_or_create(
            application_number=pat_data['application_number'],
            defaults=pat_data
        )
    print(f"  Created {len(patents_data)} patents")


def seed_tkdl_entries():
    print("Seeding TKDL entries...")
    tkdl_data = [
        {'formulation_name': 'Chyawanprash', 'text_source': 'Charaka Samhita', 'total_texts': 5000, 'digitized_texts': 4750, 'coverage_percentage': 95.0, 'ayush_category': 'AYURVEDA', 'is_verified': True},
        {'formulation_name': 'Kashayam', 'text_source': 'Sushruta Samhita', 'total_texts': 3000, 'digitized_texts': 2850, 'coverage_percentage': 95.0, 'ayush_category': 'AYURVEDA', 'is_verified': True},
        {'formulation_name': 'Dashamula', 'text_source': 'Charaka Samhita', 'total_texts': 2500, 'digitized_texts': 2375, 'coverage_percentage': 95.0, 'ayush_category': 'AYURVEDA', 'is_verified': True},
        {'formulation_name': 'Triphala', 'text_source': 'Sushruta Samhita', 'total_texts': 4000, 'digitized_texts': 3600, 'coverage_percentage': 90.0, 'ayush_category': 'AYURVEDA', 'is_verified': True},
        {'formulation_name': 'Siddha Kayakalpa', 'text_source': 'Agastyar Hridayam', 'total_texts': 1500, 'digitized_texts': 1050, 'coverage_percentage': 70.0, 'ayush_category': 'SIDDHA', 'is_verified': False},
        {'formulation_name': 'Unani Itrifal', 'text_source': 'Canon of Medicine', 'total_texts': 2000, 'digitized_texts': 1800, 'coverage_percentage': 90.0, 'ayush_category': 'UNANI', 'is_verified': True},
        {'formulation_name': 'Yoga Pranayama', 'text_source': 'Hatha Yoga Pradipika', 'total_texts': 3500, 'digitized_texts': 3150, 'coverage_percentage': 90.0, 'ayush_category': 'YOGA', 'is_verified': True},
        {'formulation_name': 'Homoeopathic Materia Medica', 'text_source': 'Hahnemann', 'total_texts': 1000, 'digitized_texts': 950, 'coverage_percentage': 95.0, 'ayush_category': 'HOMOEOPATHY', 'is_verified': True},
    ]
    for tkdl in tkdl_data:
        TKDL_Entry.objects.get_or_create(formulation_name=tkdl['formulation_name'], defaults=tkdl)
    print(f"  Created {len(tkdl_data)} TKDL entries")


def seed_alerts():
    print("Seeding alerts...")
    alerts_data = [
        {'type': 'BIOPIRACY', 'severity': 'CRITICAL', 'title': 'Biopiracy Alert: Chinese patent on Ashwagandha', 'message': 'Patent filed by Chinese company on traditional Ashwagandha formulation without prior art citation'},
        {'type': 'BIOPIRACY', 'severity': 'HIGH', 'title': 'Biopiracy Alert: US patent on Turmeric', 'message': 'US Patent USPTO 5,401,504 claims turmeric wound healing - prior art already in TKDL'},
        {'type': 'BIOPIRACY', 'severity': 'HIGH', 'title': 'Biopiracy Alert: European patent on Neem', 'message': 'EPO patent on neem-based pesticide - TKDL evidence ready'},
        {'type': 'PATENT', 'severity': 'MEDIUM', 'title': 'New patent filed: Ayurvedic sleep aid', 'message': 'New patent application filed for Ayurvedic sleep aid formulation'},
        {'type': 'GI_TAG', 'severity': 'INFO', 'title': 'GI Tag approved: Darjeeling Tea renewal', 'message': 'GI Tag for Darjeeling Tea has been renewed successfully'},
        {'type': 'TKDL', 'severity': 'INFO', 'title': 'TKDL Coverage Update', 'message': 'Ayurveda texts digitization reached 95% coverage'},
        {'type': 'BIOPIRACY', 'severity': 'HIGH', 'title': 'Biopiracy Alert: Japanese patent on Shilajit', 'message': 'Japan patent office filing on Shilajit extract without prior art reference'},
        {'type': 'SYSTEM', 'severity': 'LOW', 'title': 'System maintenance scheduled', 'message': 'System will undergo maintenance on Sunday 2:00 AM IST'},
    ]
    for alert_data in alerts_data:
        Alert.objects.get_or_create(title=alert_data['title'], defaults=alert_data)
    print(f"  Created {len(alerts_data)} alerts")


def seed_biopiracy_cases():
    print("Seeding biopiracy cases...")
    patents = list(Patent.objects.all()[:10])
    formulations = list(AYUSHFormulation.objects.all()[:10])
    users = list(User.objects.all())

    cases_data = [
        {'status': 'RESOLVED', 'priority': 'CRITICAL', 'risk_score': 95, 'description': 'US Patent on Turmeric - Successfully challenged using TKDL prior art. Patent revoked.'},
        {'status': 'PRIOR_ART_FILED', 'priority': 'HIGH', 'risk_score': 85, 'description': 'Chinese patent on Ashwagandha extract - Prior art submitted to CNIPA'},
        {'status': 'UNDER_REVIEW', 'priority': 'HIGH', 'risk_score': 78, 'description': 'European patent on Neem-based formulation under review'},
        {'status': 'ESCALATED', 'priority': 'CRITICAL', 'risk_score': 92, 'description': 'Japanese patent on Shilajit - Escalated to Ministry for diplomatic intervention'},
        {'status': 'DETECTED', 'priority': 'MEDIUM', 'risk_score': 65, 'description': 'USPTO filing on traditional Ayurvedic sleep aid - Under analysis'},
    ]

    for i, case_data in enumerate(cases_data):
        if i < len(patents) and i < len(formulations):
            patent = patents[i]
            formulation = formulations[i]
            assigned_to = random.choice(users) if users else None

            case = BiopiracyCase.objects.create(
                patent=patent,
                formulation=formulation,
                **case_data,
                assigned_to=assigned_to,
            )
            if case.status == 'RESOLVED':
                case.resolved_date = timezone.now() - timedelta(days=random.randint(30, 180))
                case.prior_art_submitted = True
                case.prior_art_date = case.resolved_date - timedelta(days=30)
                case.save()
    print(f"  Created {len(cases_data)} biopiracy cases")


def seed_dashboard_stats():
    print("Seeding dashboard stats...")
    for i in range(90):
        stat_date = timezone.now().date() - timedelta(days=i)
        DashboardStat.objects.get_or_create(
            date=stat_date,
            defaults={
                'total_gi_tags': random.randint(300, 350),
                'total_patents': random.randint(500, 600),
                'total_biopiracy_cases': random.randint(50, 100),
                'active_biopiracy_cases': random.randint(10, 30),
                'resolved_biopiracy_cases': random.randint(40, 70),
                'total_formulations': random.randint(200, 250),
                'digitized_formulations': random.randint(150, 200),
                'total_alerts': random.randint(100, 200),
                'unread_alerts': random.randint(5, 20),
            }
        )
    print(f"  Created 90 days of dashboard stats")


def seed_activities():
    print("Seeding activities...")
    activities = [
        {'activity_type': 'GI_ISSUED', 'title': 'GI Tag issued for Darjeeling Tea', 'description': 'GI Tag registration number GI-001 issued'},
        {'activity_type': 'PATENT_GRANTED', 'title': 'Patent granted for Turmeric formulation', 'description': 'Indian patent granted for novel turmeric wound healing'},
        {'activity_type': 'BIOPIRACY_RESOLVED', 'title': 'US Patent revoked: Turmeric case', 'description': 'Prior art from TKDL successfully challenged USPTO patent'},
        {'activity_type': 'TKDL_ADDED', 'title': 'New TKDL entry: Siddha Kayakalpa', 'description': 'Traditional Siddha formulation added to digital library'},
        {'activity_type': 'FORMULATION_REGISTERED', 'title': 'Chyawanprash registered', 'description': 'Traditional formulation registered with AYUSH department'},
    ]
    for activity_data in activities:
        IPActivity.objects.get_or_create(title=activity_data['title'], defaults=activity_data)
    print(f"  Created {len(activities)} activities")


def main():
    print("=" * 60)
    print("IP-SAKTI Database Seeding")
    print("=" * 60)
    seed_users()
    seed_states()
    seed_formulations()
    seed_gi_tags()
    seed_patents()
    seed_tkdl_entries()
    seed_alerts()
    seed_biopiracy_cases()
    seed_dashboard_stats()
    seed_activities()
    print("=" * 60)
    print("Seeding completed successfully!")
    print("=" * 60)
    print("\nDefault login credentials:")
    print("  Admin: admin@ipsakti.gov.in / admin123")
    print("  Ministry Official: official@ipsakti.gov.in / official123")
    print("  Analyst: analyst@ipsakti.gov.in / analyst123")
    print("  Viewer: viewer@ipsakti.gov.in / viewer123")


if __name__ == '__main__':
    main()
