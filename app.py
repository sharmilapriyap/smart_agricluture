import os
import traceback
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "secret123")

MOBILE_KEYWORDS = ("android", "iphone", "ipad", "ipod", "mobile", "opera mini", "windows phone")


TRANSLATIONS = {
    "english": {
        "app_title": "Smart Agriculture Dashboard",
        "subtitle": "Crop suggestions based on country, region, season, soil, and live weather",
        "country": "Country",
        "region": "Region",
        "season": "Season",
        "preference": "User Preference",
        "language": "Language Preference",
        "soil_title": "Simple Soil Questions",
        "soil_color": "1. Soil color",
        "texture": "2. Texture",
        "water_absorption": "3. Water absorption",
        "weather_title": "Auto Weather Detection",
        "weather_wait": "Detecting weather from your location...",
        "weather_ready": "Live weather detected successfully.",
        "weather_fallback": "Weather could not be detected. Suggestions will use your selected season and soil details.",
        "predict": "Get Crop Suggestion",
        "dashboard": "Farmer Dashboard",
        "top_crop": "Best Crop Suggestion",
        "alternatives": "Other Suitable Crops",
        "why": "Why this crop suits your input",
        "tips": "Smart Weather Suggestions",
        "fertilizer_button": "Fertilizer Recommendation",
        "fertilizer_title": "Fertilizer Plan",
        "organic": "Organic Fertilizers",
        "chemical": "Chemical Fertilizers",
        "schedule": "How many times",
        "ratio": "Recommended ratio",
        "method": "How to apply",
        "details": "Details",
        "no_match": "Please choose any other item.",
        "login": "Login",
        "enter_mobile": "Enter mobile number",
        "send_otp": "Send OTP",
        "enter_otp": "Enter OTP",
        "verify": "Verify OTP",
        "invalid_otp": "Invalid OTP. Please try again.",
        "kharif": "Monsoon",
        "rabi": "Winter",
        "summer": "Summer",
        "year_round": "Year Round",
        "vegetables": "Vegetables",
        "fruits": "Fruits",
        "cash_crops": "Cash Crops",
        "grains": "Grains",
        "pulses": "Pulses",
        "millets": "Millets",
    },
    "telugu": {
        "app_title": "స్మార్ట్ అగ్రికల్చర్ డ్యాష్‌బోర్డ్",
        "subtitle": "దేశం, ప్రాంతం, సీజన్, నేల, వాతావరణం ఆధారంగా పంట సూచనలు",
        "country": "దేశం",
        "region": "ప్రాంతం",
        "season": "సీజన్",
        "preference": "వినియోగదారు అభిరుచి",
        "language": "భాష ఎంపిక",
        "soil_title": "సరళమైన నేల ప్రశ్నలు",
        "soil_color": "1. నేల రంగు",
        "texture": "2. గుణము",
        "water_absorption": "3. నీరు పీల్చుకునే వేగం",
        "weather_title": "ఆటో వాతావరణ గుర్తింపు",
        "weather_wait": "మీ ప్రాంత వాతావరణం గుర్తిస్తోంది...",
        "weather_ready": "లైవ్ వాతావరణ సమాచారం సక్సెస్‌గా వచ్చింది.",
        "weather_fallback": "వాతావరణం గుర్తించలేకపోయాం. సీజన్ మరియు నేల ఆధారంగా సూచనలు ఇస్తాం.",
        "predict": "పంట సూచన చూడండి",
        "dashboard": "రైతు డ్యాష్‌బోర్డ్",
        "top_crop": "అత్యుత్తమ పంట సూచన",
        "alternatives": "ఇతర సరిపోయే పంటలు",
        "why": "ఈ పంట ఎందుకు సరిపోతుంది",
        "tips": "స్మార్ట్ వాతావరణ సూచనలు",
        "fertilizer_button": "ఎరువు సిఫార్సు",
        "fertilizer_title": "ఎరువు ప్రణాళిక",
        "organic": "సేంద్రీయ ఎరువులు",
        "chemical": "రసాయన ఎరువులు",
        "schedule": "ఎన్ని సార్లు",
        "ratio": "సూచించిన నిష్పత్తి",
        "method": "ఎలా వేయాలి",
        "details": "వివరాలు",
        "no_match": "దయచేసి మరో ఎంపికను ఎంచుకోండి.",
        "login": "లాగిన్",
        "enter_mobile": "మొబైల్ నంబర్ నమోదు చేయండి",
        "send_otp": "ఓటిపి పంపండి",
        "enter_otp": "ఓటిపి నమోదు చేయండి",
        "verify": "ఓటిపి నిర్ధారించండి",
        "invalid_otp": "తప్పు ఓటిపి. మళ్లీ ప్రయత్నించండి.",
        "kharif": "వానాకాలం",
        "rabi": "శీతాకాలం",
        "summer": "వేసవి",
        "year_round": "ఏడాది పొడవునా",
        "vegetables": "కూరగాయలు",
        "fruits": "పండ్లు",
        "cash_crops": "వాణిజ్య పంటలు",
        "grains": "ధాన్యాలు",
        "pulses": "పప్పుధాన్యాలు",
        "millets": "మిల్లెట్స్",
    },
    "tamil": {
        "app_title": "ஸ்மார்ட் வேளாண்மை டாஷ்போர்டு",
        "subtitle": "நாடு, பகுதி, பருவம், மண், நேரடி வானிலை அடிப்படையில் பயிர் பரிந்துரை",
        "country": "நாடு",
        "region": "பகுதி",
        "season": "பருவம்",
        "preference": "பயனர் விருப்பம்",
        "language": "மொழி தேர்வு",
        "soil_title": "எளிய மண் கேள்விகள்",
        "soil_color": "1. மண் நிறம்",
        "texture": "2. தன்மை",
        "water_absorption": "3. நீர் உறிஞ்சும் வேகம்",
        "weather_title": "தானியங்கி வானிலை கண்டறிதல்",
        "weather_wait": "உங்கள் இடத்தின் வானிலையை கண்டறிகிறது...",
        "weather_ready": "நேரடி வானிலை வெற்றிகரமாக பெறப்பட்டது.",
        "weather_fallback": "வானிலை கண்டறியப்படவில்லை. பருவம் மற்றும் மண் விவரங்களால் பரிந்துரைகள் தரப்படும்.",
        "predict": "பயிர் பரிந்துரை பெறுங்கள்",
        "dashboard": "விவசாயி டாஷ்போர்டு",
        "top_crop": "சிறந்த பயிர் பரிந்துரை",
        "alternatives": "மற்ற பொருத்தமான பயிர்கள்",
        "why": "இந்த பயிர் ஏன் பொருத்தம்",
        "tips": "ஸ்மார்ட் வானிலை அறிவுறுத்தல்கள்",
        "fertilizer_button": "உர பரிந்துரை",
        "fertilizer_title": "உர திட்டம்",
        "organic": "உயிரி உரங்கள்",
        "chemical": "ரசாயன உரங்கள்",
        "schedule": "எத்தனை முறை",
        "ratio": "பரிந்துரைக்கப்பட்ட விகிதம்",
        "method": "எப்படி இட வேண்டும்",
        "details": "விவரங்கள்",
        "no_match": "வேறு தேர்வை தேர்ந்தெடுக்கவும்.",
        "login": "உள்நுழைவு",
        "enter_mobile": "மொபைல் எண்ணை உள்ளிடுங்கள்",
        "send_otp": "ஓடிபி அனுப்பு",
        "enter_otp": "ஓடிபி உள்ளிடுங்கள்",
        "verify": "ஓடிபி சரிபார்",
        "invalid_otp": "தவறான ஓடிபி. மீண்டும் முயற்சிக்கவும்.",
        "kharif": "மழைக்காலம்",
        "rabi": "குளிர்காலம்",
        "summer": "கோடை",
        "year_round": "ஆண்டு முழுவதும்",
        "vegetables": "காய்கறிகள்",
        "fruits": "பழங்கள்",
        "cash_crops": "பணப்பயிர்கள்",
        "grains": "தானியங்கள்",
        "pulses": "பயறுகள்",
        "millets": "சிறுதானியங்கள்",
    },
    "hindi": {
        "app_title": "स्मार्ट एग्रीकल्चर डैशबोर्ड",
        "subtitle": "देश, क्षेत्र, मौसम, मिट्टी और लाइव वेदर के आधार पर फसल सुझाव",
        "country": "देश",
        "region": "क्षेत्र",
        "season": "सीजन",
        "preference": "उपयोगकर्ता पसंद",
        "language": "भाषा पसंद",
        "soil_title": "सरल मिट्टी प्रश्न",
        "soil_color": "1. मिट्टी का रंग",
        "texture": "2. बनावट",
        "water_absorption": "3. पानी सोखने की गति",
        "weather_title": "ऑटो वेदर डिटेक्शन",
        "weather_wait": "आपकी लोकेशन का मौसम पता किया जा रहा है...",
        "weather_ready": "लाइव वेदर सफलतापूर्वक मिल गया।",
        "weather_fallback": "मौसम नहीं मिल पाया। सुझाव सीजन और मिट्टी के आधार पर दिए जाएंगे।",
        "predict": "फसल सुझाव देखें",
        "dashboard": "किसान डैशबोर्ड",
        "top_crop": "सबसे अच्छा फसल सुझाव",
        "alternatives": "अन्य उपयुक्त फसलें",
        "why": "यह फसल क्यों सही है",
        "tips": "स्मार्ट वेदर सुझाव",
        "fertilizer_button": "उर्वरक सिफारिश",
        "fertilizer_title": "उर्वरक योजना",
        "organic": "जैविक उर्वरक",
        "chemical": "रासायनिक उर्वरक",
        "schedule": "कितनी बार",
        "ratio": "सुझाव अनुपात",
        "method": "कैसे देना है",
        "details": "विवरण",
        "no_match": "कृपया कोई दूसरा विकल्प चुनें।",
        "login": "लॉगिन",
        "enter_mobile": "मोबाइल नंबर दर्ज करें",
        "send_otp": "ओटीपी भेजें",
        "enter_otp": "ओटीपी दर्ज करें",
        "verify": "ओटीपी सत्यापित करें",
        "invalid_otp": "गलत ओटीपी। फिर से कोशिश करें।",
        "kharif": "मानसून",
        "rabi": "सर्दी",
        "summer": "गर्मी",
        "year_round": "पूरे वर्ष",
        "vegetables": "सब्जियां",
        "fruits": "फल",
        "cash_crops": "नकदी फसलें",
        "grains": "अनाज",
        "pulses": "दालें",
        "millets": "मिलेट्स",
    },
}

TRANSLATION_EXTRAS = {
    "english": {
        "english": "English",
        "telugu": "Telugu",
        "tamil": "Tamil",
        "hindi": "Hindi",
        "black": "Black",
        "red": "Red",
        "brown": "Brown",
        "sticky": "Sticky",
        "dry": "Dry",
        "soft": "Soft",
        "fast": "Fast",
        "slow": "Slow",
        "chip_location": "Country + Region",
        "chip_season": "Season",
        "chip_preference": "Preference",
        "chip_soil": "Simple Soil Inputs",
        "chip_weather": "Live Weather",
        "results_placeholder": "The dashboard will show crop suggestion, smart care tips, and fertilizer plan here after prediction.",
        "temp_label": "Temp",
        "humidity_label": "Humidity",
        "rain_chance_label": "Rain chance",
    },
    "telugu": {
        "english": "English",
        "telugu": "తెలుగు",
        "tamil": "తమిళం",
        "hindi": "హిందీ",
        "black": "నలుపు",
        "red": "ఎరుపు",
        "brown": "గోధుమ",
        "sticky": "అంటుకునే",
        "dry": "పొడి",
        "soft": "మెత్తని",
        "fast": "వేగంగా",
        "slow": "నెమ్మదిగా",
        "chip_location": "దేశం + ప్రాంతం",
        "chip_season": "సీజన్",
        "chip_preference": "అభిరుచి",
        "chip_soil": "సరళ నేల వివరాలు",
        "chip_weather": "లైవ్ వాతావరణం",
        "results_placeholder": "ప్రిడిక్షన్ తర్వాత ఇక్కడ పంట సూచన, సంరక్షణ చిట్కాలు, ఎరువు ప్రణాళిక కనిపిస్తుంది.",
        "temp_label": "ఉష్ణోగ్రత",
        "humidity_label": "తేమ",
        "rain_chance_label": "వర్షం అవకాశం",
    },
    "tamil": {
        "english": "English",
        "telugu": "தெலுங்கு",
        "tamil": "தமிழ்",
        "hindi": "இந்தி",
        "black": "கருப்பு",
        "red": "சிவப்பு",
        "brown": "பழுப்பு",
        "sticky": "ஒட்டும்",
        "dry": "உலர்",
        "soft": "மென்மை",
        "fast": "வேகமாக",
        "slow": "மெதுவாக",
        "chip_location": "நாடு + பகுதி",
        "chip_season": "பருவம்",
        "chip_preference": "விருப்பம்",
        "chip_soil": "எளிய மண் விவரங்கள்",
        "chip_weather": "நேரடி வானிலை",
        "results_placeholder": "கணிப்புக்குப் பிறகு இங்கு பயிர் பரிந்துரை, பராமரிப்பு குறிப்புகள், உர திட்டம் காட்டப்படும்.",
        "temp_label": "வெப்பநிலை",
        "humidity_label": "ஈரப்பதம்",
        "rain_chance_label": "மழை வாய்ப்பு",
    },
    "hindi": {
        "english": "English",
        "telugu": "तेलुगु",
        "tamil": "तमिल",
        "hindi": "हिंदी",
        "black": "काला",
        "red": "लाल",
        "brown": "भूरा",
        "sticky": "चिपचिपा",
        "dry": "सूखा",
        "soft": "मुलायम",
        "fast": "तेज़",
        "slow": "धीमा",
        "chip_location": "देश + क्षेत्र",
        "chip_season": "सीजन",
        "chip_preference": "पसंद",
        "chip_soil": "सरल मिट्टी विवरण",
        "chip_weather": "लाइव मौसम",
        "results_placeholder": "भविष्यवाणी के बाद यहां फसल सुझाव, देखभाल टिप्स और उर्वरक योजना दिखाई देगी.",
        "temp_label": "तापमान",
        "humidity_label": "नमी",
        "rain_chance_label": "बारिश की संभावना",
    },
}

for language, extra_values in TRANSLATION_EXTRAS.items():
    TRANSLATIONS[language].update(extra_values)

TRANSLATIONS["english"].update(
    {
        "no_match_detail": "No exact crop match was found for this country, region, season, and preference combination.",
        "available_here": "Available here",
        "try_region": "Try region",
        "try_season": "Try season",
        "try_category": "Try preference",
        "closest_crops": "Closest available crops",
    }
)
TRANSLATIONS["telugu"].update(
    {
        "no_match_detail": "ఈ దేశం, ప్రాంతం, సీజన్, అభిరుచి కలయికకు ఖచ్చితమైన పంట సరిపోలిక దొరకలేదు.",
        "available_here": "ఇక్కడ అందుబాటులో ఉన్నవి",
        "try_region": "ప్రాంతం మార్చి చూడండి",
        "try_season": "సీజన్ మార్చి చూడండి",
        "try_category": "అభిరుచి మార్చి చూడండి",
        "closest_crops": "దగ్గరగా సరిపోయే పంటలు",
    }
)
TRANSLATIONS["tamil"].update(
    {
        "no_match_detail": "இந்த நாடு, பகுதி, பருவம், விருப்பம் இணைப்புக்கு சரியான பயிர் பொருத்தம் கிடைக்கவில்லை.",
        "available_here": "இங்கே கிடைப்பவை",
        "try_region": "பகுதியை மாற்றிப் பாருங்கள்",
        "try_season": "பருவத்தை மாற்றிப் பாருங்கள்",
        "try_category": "விருப்பத்தை மாற்றிப் பாருங்கள்",
        "closest_crops": "அருகிலான பயிர்கள்",
    }
)
TRANSLATIONS["hindi"].update(
    {
        "no_match_detail": "इस देश, क्षेत्र, सीजन और पसंद के संयोजन के लिए सटीक फसल मेल नहीं मिला।",
        "available_here": "यहां उपलब्ध",
        "try_region": "क्षेत्र बदलकर देखें",
        "try_season": "सीजन बदलकर देखें",
        "try_category": "पसंद बदलकर देखें",
        "closest_crops": "सबसे नज़दीकी फसलें",
    }
)


NATIVE_LANGUAGE_LABELS = {
    "english": "English",
    "telugu": "తెలుగు",
    "tamil": "தமிழ்",
    "hindi": "हिंदी",
}


LOCATION_TEXTS = {
    "english": {
        "India": "India",
        "USA": "USA",
        "Australia": "Australia",
        "Andhra Pradesh": "Andhra Pradesh",
        "Telangana": "Telangana",
        "Tamil Nadu": "Tamil Nadu",
        "Punjab": "Punjab",
        "Karnataka": "Karnataka",
        "Maharashtra": "Maharashtra",
        "California": "California",
        "Texas": "Texas",
        "Florida": "Florida",
        "Queensland": "Queensland",
        "Victoria": "Victoria",
    },
    "telugu": {
        "India": "భారతదేశం",
        "USA": "అమెరికా",
        "Australia": "ఆస్ట్రేలియా",
        "Andhra Pradesh": "ఆంధ్రప్రదేశ్",
        "Telangana": "తెలంగాణ",
        "Tamil Nadu": "తమిళనాడు",
        "Punjab": "పంజాబ్",
        "Karnataka": "కర్ణాటక",
        "Maharashtra": "మహారాష్ట్ర",
        "California": "కాలిఫోర్నియా",
        "Texas": "టెక్సాస్",
        "Florida": "ఫ్లోరిడా",
        "Queensland": "క్వీన్స్‌ల్యాండ్",
        "Victoria": "విక్టోరియా",
    },
    "tamil": {
        "India": "இந்தியா",
        "USA": "அமெரிக்கா",
        "Australia": "ஆஸ்திரேலியா",
        "Andhra Pradesh": "ஆந்திரப் பிரதேசம்",
        "Telangana": "தெலங்கானா",
        "Tamil Nadu": "தமிழ்நாடு",
        "Punjab": "பஞ்சாப்",
        "Karnataka": "கர்நாடகா",
        "Maharashtra": "மகாராஷ்டிரா",
        "California": "காலிஃபோர்னியா",
        "Texas": "டெக்சாஸ்",
        "Florida": "புளோரிடா",
        "Queensland": "குயின்ஸ்லாந்து",
        "Victoria": "விக்டோரியா",
    },
    "hindi": {
        "India": "भारत",
        "USA": "अमेरिका",
        "Australia": "ऑस्ट्रेलिया",
        "Andhra Pradesh": "आंध्र प्रदेश",
        "Telangana": "तेलंगाना",
        "Tamil Nadu": "तमिलनाडु",
        "Punjab": "पंजाब",
        "Karnataka": "कर्नाटक",
        "Maharashtra": "महाराष्ट्र",
        "California": "कैलिफोर्निया",
        "Texas": "टेक्सास",
        "Florida": "फ्लोरिडा",
        "Queensland": "क्वींसलैंड",
        "Victoria": "विक्टोरिया",
    },
}


CROP_TEXTS = {
    "telugu": {
        "Rice": {
            "name": "వరి",
            "why": "వేడి, తేమ ఎక్కువగా ఉండే మరియు నీటిని నిల్వ ఉంచే నేలల్లో వరి బాగా పెరుగుతుంది.",
            "fertilizer": {
                "organic": {
                    "details": "నాటు ముందు పశువుల ఎరువు లేదా కంపోస్ట్ వేస్తే నీటిని నిల్వ ఉంచే నేల నిర్మాణం మెరుగవుతుంది.",
                    "schedule": "2 సార్లు: ప్రారంభంలో ఒకసారి, 25 నుంచి 30 రోజుల తర్వాత మరోసారి.",
                    "ratio": "ఎకరానికి 5 నుంచి 8 టన్నుల కంపోస్ట్, లభ్యమైతే వేపపిండి కలపండి.",
                    "method": "నాటే ముందు తడి నేలలో కలపాలి. తర్వాత వేర్ల దగ్గర తేలికగా వేయాలి.",
                },
                "chemical": {
                    "details": "సమతుల్య పోషకాలు వరి మొక్కలో టిల్లర్ పెరుగుదల మరియు గింజ నింపుదలకు సహాయపడతాయి.",
                    "schedule": "3 విడతలు: మొదట, టిల్లరింగ్ దశలో, పానికిల్ ప్రారంభ దశలో.",
                    "ratio": "NPK 100:50:50 కిలోలు/హెక్టారు విడతలుగా.",
                    "method": "మొదటి మోతాదు నేలలో వేయాలి. తరువాత నత్రజనిని రెండు విడతలుగా నీటితో కలిపి ఇవ్వాలి.",
                },
            },
        },
        "Maize": {
            "name": "మొక్కజొన్న",
            "why": "మంచి డ్రైనేజ్ ఉన్న నేలల్లో, మితమైన వేడి మరియు తగిన తేమలో మొక్కజొన్న బాగా పెరుగుతుంది.",
            "fertilizer": {
                "organic": {
                    "details": "కంపోస్ట్ మరియు వెర్మీ కంపోస్ట్ వేర్ల పెరుగుదలను స్థిరంగా ఉంచుతాయి.",
                    "schedule": "2 సార్లు: భూమి సిద్ధం చేసే సమయంలో మరియు మోకాలి ఎత్తు దశలో.",
                    "ratio": "ఎకరానికి 3 నుంచి 4 టన్నుల కంపోస్ట్.",
                    "method": "బెడ్ సిద్ధం చేసే సమయంలో వేయాలి. 25 రోజుల తర్వాత వరుసల పక్కన వేయాలి.",
                },
                "chemical": {
                    "details": "శాకీయ పెరుగుదల దశలో నత్రజని చాలా ముఖ్యమైనది.",
                    "schedule": "3 సార్లు: మొదట, 25వ రోజు, 45వ రోజు.",
                    "ratio": "NPK 120:60:40 కిలోలు/హెక్టారు.",
                    "method": "వేర్లకు 5 సెం.మీ దూరంలో ఎరువు వేసి తేలికగా నీరు పెట్టాలి.",
                },
            },
        },
        "Tomato": {
            "name": "టమాటా",
            "why": "మెత్తని, మంచి డ్రైనేజ్ ఉన్న నేల మరియు మితమైన ఉష్ణోగ్రతలు టమాటాకు అనుకూలం.",
            "fertilizer": {
                "organic": {
                    "details": "సేంద్రీయ పదార్థం పండు కట్టడాన్ని మరియు నేల సూక్ష్మజీవుల క్రియాశీలతను మెరుగుపరుస్తుంది.",
                    "schedule": "3 సార్లు: నాటు ముందు, పుష్ప దశలో, పండు దశలో.",
                    "ratio": "ఎకరానికి 2 నుంచి 3 టన్నుల కంపోస్ట్, లభ్యమైతే బోన్‌మీల్ కలపండి.",
                    "method": "రైజ్డ్ బెడ్స్‌లో కలపాలి. తరువాత మొక్క చుట్టూ తేలికగా వేయాలి.",
                },
                "chemical": {
                    "details": "పండ్ల దశలో కొంచెం ఎక్కువ పొటాషియంతో సమతుల్య పోషకాలు టమాటాకు అవసరం.",
                    "schedule": "వివిధ పెరుగుదల దశల్లో 3 నుంచి 4 సార్లు.",
                    "ratio": "NPK 75:40:60 కిలోలు/హెక్టారు.",
                    "method": "మొదటి మోతాదును బేసల్‌గా ఇవ్వాలి. తర్వాత డ్రిప్ లైన్ దగ్గర విడతలుగా వేయాలి.",
                },
            },
        },
        "Chilli": {
            "name": "మిరప",
            "why": "త్వరగా డ్రైనేజ్ అయ్యే తేలికపాటి నేలలు మరియు వేడి వాతావరణంలో మిరప బాగా పెరుగుతుంది.",
            "fertilizer": {
                "organic": {
                    "details": "బాగా కుళ్లిన పశువుల ఎరువు మొక్కలకు హాని లేకుండా వేర్ల చుట్టూ చురుకుదనాన్ని పెంచుతుంది.",
                    "schedule": "2 సార్లు: బేసల్ దశలో మరియు పుష్ప దశలో.",
                    "ratio": "ఎకరానికి 2 టన్నుల కంపోస్ట్ మరియు వేపపిండి.",
                    "method": "బెడ్ తయారీ సమయంలో కలపాలి. తరువాత మొక్క చుట్టూ ఉంగరం మాదిరిగా వేయాలి.",
                },
                "chemical": {
                    "details": "పుష్ప మరియు పండు అభివృద్ధి దశల్లో విడతలుగా ఇచ్చే పోషకాలు మిరపకు మేలు చేస్తాయి.",
                    "schedule": "3 సార్లు: బేసల్, పుష్ప దశ, పండు కట్టే దశ.",
                    "ratio": "NPK 60:30:30 కిలోలు/హెక్టారు.",
                    "method": "చిన్న మోతాదులుగా విడతలుగా వేయాలి. కాండానికి నేరుగా తగలకుండా చూడాలి.",
                },
            },
        },
        "Mango": {
            "name": "మామిడి",
            "why": "నీరు నిల్వ కాకుండా ఉంటే వెచ్చని ప్రాంతాల్లో అనేక రకాల నేలలకు మామిడి బాగా సరిపోతుంది.",
            "fertilizer": {
                "organic": {
                    "details": "సేంద్రీయ ఎరువులు చెట్టు దీర్ఘకాల ఆరోగ్యం మరియు పండు నాణ్యతకు మేలు చేస్తాయి.",
                    "schedule": "సంవత్సరానికి 2 సార్లు: పుష్పదశ ముందు మరియు కోత తర్వాత.",
                    "ratio": "ఒక్కో చెట్టుకు 20 నుంచి 25 కిలోల పశువుల ఎరువు.",
                    "method": "కానోపీ డ్రిప్ లైన్ చుట్టూ వలయాకారపు కాలువలో వేసి మట్టితో కప్పాలి.",
                },
                "chemical": {
                    "details": "దశల ఆధారంగా చెట్టు పోషణ ఇవ్వాలి. అధిక మోతాదు వేయకూడదు.",
                    "schedule": "సంవత్సరానికి 2 సార్లు.",
                    "ratio": "పెద్ద చెట్టుకు NPK 1:0.5:1 కిలోల యాక్టివ్ న్యూట్రియెంట్ సమాన మోతాదు.",
                    "method": "డ్రిప్ లైన్ చుట్టూ సమంగా చల్లి తర్వాత నీరు పెట్టాలి.",
                },
            },
        },
        "Banana": {
            "name": "అరటి",
            "why": "సారవంతమైన నేల, వెచ్చని వాతావరణం మరియు నియమిత తేమలో అరటి బాగా స్పందిస్తుంది.",
            "fertilizer": {
                "organic": {
                    "details": "అరటికి నిరంతర పెరుగుదల కోసం సమృద్ధిగా సేంద్రీయ పదార్థం అవసరం.",
                    "schedule": "3 సార్లు: గుంత సిద్ధం, 45వ రోజు, 90వ రోజు.",
                    "ratio": "ఏడాదికి ఒక్కో మొక్కకు 10 నుంచి 15 కిలోల కంపోస్ట్.",
                    "method": "ప్సూడోస్టెమ్‌కు దూరంగా వలయాకారంగా వేసి తేలికగా కప్పాలి.",
                },
                "chemical": {
                    "details": "అరటి ముఖ్యంగా పొటాషియం కోసం ఎక్కువ పోషకాలు అవసరపడే పంట.",
                    "schedule": "శాకీయ పెరుగుదల కాలంలో 4 విడతలుగా.",
                    "ratio": "వైవిధ్యాన్ని బట్టి ఒక్కో మొక్కకు NPK 200:60:200 గ్రాములు.",
                    "method": "వలయాకారపు విడతలుగా వేసి వెంటనే నీరు పెట్టాలి.",
                },
            },
        },
        "Cotton": {
            "name": "పత్తి",
            "why": "వెచ్చని వాతావరణం, మంచి సూర్యరశ్మి మరియు మితమైన డ్రైనేజ్ ఉన్న నేలల్లో పత్తి బాగా సరిపోతుంది.",
            "fertilizer": {
                "organic": {
                    "details": "సేంద్రీయ పదార్థాలు నేల నిర్మాణం మరియు తేమ నిల్వను మెరుగుపరుస్తాయి.",
                    "schedule": "2 సార్లు: బేసల్ దశలో మరియు స్క్వేర్ ఫార్మేషన్ దశలో.",
                    "ratio": "ఎకరానికి 2 నుంచి 3 టన్నుల కంపోస్ట్.",
                    "method": "విత్తే ముందు నేలలో కలిపి, తరువాత వరుసల దగ్గర సైడ్ డ్రెస్సింగ్ చేయాలి.",
                },
                "chemical": {
                    "details": "సమతుల్య పోషణతో బోల్స్ బాగా వస్తాయి, అధిక శాకీయ పెరుగుదల తగ్గుతుంది.",
                    "schedule": "శాకీయ మరియు పుష్ప దశల్లో 3 సార్లు.",
                    "ratio": "NPK 100:50:50 కిలోలు/హెక్టారు.",
                    "method": "నత్రజనిని విడతలుగా ఇవ్వాలి. వర్షం ముందు భారీ మోతాదు వేయకండి.",
                },
            },
        },
        "Red Gram": {
            "name": "కందులు",
            "why": "మధ్యస్థంగా పొడి ప్రాంతాలు మరియు త్వరగా డ్రైనేజ్ అయ్యే నేలల్లో కందులు బాగా పెరుగుతాయి.",
            "fertilizer": {
                "organic": {
                    "details": "పప్పుధాన్యాలు మితమైన సేంద్రీయ పోషణ మరియు బయో ఇన్‌పుట్స్‌కు బాగా స్పందిస్తాయి.",
                    "schedule": "1 నుంచి 2 సార్లు: బేసల్ దశలో, అవసరమైతే ప్రారంభ కొమ్మల దశలో.",
                    "ratio": "ఎకరానికి 1.5 నుంచి 2 టన్నుల కంపోస్ట్ మరియు రైజోబియం ఇనాక్యులేషన్.",
                    "method": "విత్తే ముందు కంపోస్ట్ వేయాలి. గింజలను బయోఫర్టిలైజర్‌తో శుద్ధి చేయాలి.",
                },
                "chemical": {
                    "details": "పప్పుధాన్యాలకు తక్కువ నత్రజని సరిపోతుంది కానీ ఫాస్పరస్ మద్దతు ఉపయోగపడుతుంది.",
                    "schedule": "1 బేసల్ అప్లికేషన్, అవసరమైతే తేలికైన టాప్-అప్.",
                    "ratio": "NPK 20:50:20 కిలోలు/హెక్టారు.",
                    "method": "విత్తే సమయంలో గింజల కింద ఎరువును ఉంచాలి.",
                },
            },
        },
        "Foxtail Millet": {
            "name": "కొర్రలు",
            "why": "తక్కువ నీటి పరిస్థితులు మరియు తేలికపాటి నేలలకు కొర్రలు చాలా అనుకూలం.",
            "fertilizer": {
                "organic": {
                    "details": "కొర్రలకు తేలికైన కానీ నిరంతర పోషక మద్దతు అవసరం.",
                    "schedule": "1 నుంచి 2 సార్లు.",
                    "ratio": "ఎకరానికి 1 నుంచి 1.5 టన్నుల కంపోస్ట్.",
                    "method": "విత్తే ముందు కంపోస్ట్ చల్లి తేలికగా నేలలో కలపాలి.",
                },
                "chemical": {
                    "details": "వరి లేదా మొక్కజొన్నతో పోలిస్తే కొర్రలకు మితమైన రసాయన ఎరువు సరిపోతుంది.",
                    "schedule": "2 విడతలు: బేసల్ మరియు ప్రారంభ టిల్లరింగ్ దశలో.",
                    "ratio": "NPK 40:20:20 కిలోలు/హెక్టారు.",
                    "method": "మొదట బేసల్‌గా వేయాలి. తరువాత తేలికైన నత్రజని టాప్-అప్ ఇవ్వాలి.",
                },
            },
        },
    }
}


def localize_crop_name(crop_name, language):
    crop_text = CROP_TEXTS.get(language, {}).get(crop_name, {})
    return crop_text.get("name", translate_exact_text(crop_name, language))


def localize_crop(crop, language):
    crop_text = CROP_TEXTS.get(language, {}).get(crop["name"], {})
    fertilizer_text = crop_text.get("fertilizer", {})
    fertilizer = {}

    for choice, plan in crop["fertilizer"].items():
        localized_plan = fertilizer_text.get(choice, {})
        fertilizer[choice] = {
            "details": localized_plan.get("details", translate_exact_text(plan["details"], language)),
            "schedule": localized_plan.get("schedule", translate_exact_text(plan["schedule"], language)),
            "ratio": localized_plan.get("ratio", translate_exact_text(plan["ratio"], language)),
            "method": localized_plan.get("method", translate_exact_text(plan["method"], language)),
        }

    return {
        "name": crop_text.get("name", translate_exact_text(crop["name"], language)),
        "why": crop_text.get("why", translate_exact_text(crop["why"], language)),
        "fertilizer": fertilizer,
    }


EXACT_TEXT_TRANSLATIONS = {
    "tamil": {
        "Rice": "அரிசி",
        "Maize": "மக்காச்சோளம்",
        "Tomato": "தக்காளி",
        "Chilli": "மிளகாய்",
        "Mango": "மாம்பழம்",
        "Banana": "வாழை",
        "Cotton": "பருத்தி",
        "Red Gram": "துவரம் பருப்பு",
        "Foxtail Millet": "தினை",
        "Rice suits warm, humid conditions with soils that hold water well.": "வெப்பமும் ஈரப்பதமும் அதிகமாக இருந்து, தண்ணீரை நன்றாக தக்கவைக்கும் மண்ணில் அரிசி சிறப்பாக வளரும்.",
        "Maize performs well in well-drained soils with moderate heat and balanced moisture.": "நல்ல வடிகால் கொண்ட மண், மிதமான வெப்பம் மற்றும் சமநிலை ஈரத்துடன் மக்காச்சோளம் நன்றாக வளரும்.",
        "Tomato prefers soft, well-drained soil and moderate temperatures.": "மென்மையான, நல்ல வடிகால் கொண்ட மண் மற்றும் மிதமான வெப்பநிலை தக்காளிக்கு ஏற்றது.",
        "Chilli grows best in lighter soils with quick drainage and warm weather.": "விரைவான வடிகால் உள்ள இலகு மண் மற்றும் சூடான காலநிலையில் மிளகாய் சிறப்பாக வளரும்.",
        "Mango suits warm regions and adapts well to many soils if waterlogging is avoided.": "நீர் தேங்காமல் இருந்தால், வெப்பமான பகுதிகளில் மாம்பழம் பல வகை மண்ணிலும் நன்றாக பொருந்தும்.",
        "Banana responds well to fertile soil, warmth, and regular moisture.": "செழிப்பான மண், வெப்பம் மற்றும் தொடர்ச்சியான ஈரத்துடன் வாழை நன்றாக வளர்கிறது.",
        "Cotton fits warm climates with good sunlight and moderately drained soils.": "நல்ல சூரியஒளி, மிதமான வடிகால் கொண்ட மண் மற்றும் வெப்பமான காலநிலை பருத்திக்கு ஏற்றது.",
        "Red gram suits moderately dry regions and soils with quick drainage.": "மிதமான உலர்ந்த பகுதிகள் மற்றும் விரைவான வடிகால் கொண்ட மண் துவரத்திற்கு ஏற்றது.",
        "Foxtail millet is ideal for lower water conditions and lighter soils.": "குறைந்த நீர் நிலை மற்றும் இலகு மண்ணுக்கு தினை மிகவும் ஏற்றது.",
        "Use farmyard manure or compost before transplanting to improve water-holding soil structure.": "நடவு செய்வதற்கு முன் பண்ணை உரம் அல்லது கம்போஸ்ட் பயன்படுத்தினால், தண்ணீர் தாங்கும் மண் அமைப்பு மேம்படும்.",
        "2 times: base application and one top-up after 25 to 30 days.": "2 முறை: அடிப்படை பயன்பாடு மற்றும் 25 முதல் 30 நாட்களுக்கு பிறகு ஒரு மேல்சேர்க்கை.",
        "5 to 8 tons compost per acre plus neem cake if available.": "ஒரு ஏக்கருக்கு 5 முதல் 8 டன் கம்போஸ்ட்; கிடைத்தால் வேப்பம் பிண்ணாக்கும் சேர்க்கலாம்.",
        "Mix compost into moist soil before planting, then apply a light side dressing near root zone.": "நடவு முன் ஈரமான மண்ணில் கம்போஸ்டை கலக்கவும்; பின்னர் வேர் பகுதிக்கு அருகில் இலகுவாக இடவும்.",
        "Balanced feeding helps rice maintain tiller growth and grain filling.": "சமநிலை உரமிடுதல் அரிசியில் கிளை வளர்ச்சிக்கும் கதிர் நிரப்பத்திற்கும் உதவும்.",
        "3 splits: basal, tillering stage, panicle initiation.": "3 பிரிவுகள்: அடிப்படை, கிளை வளர்ச்சி நிலை, கதிர் தொடக்க நிலை.",
        "NPK 100:50:50 kg/ha in split doses.": "பகுதியாக NPK 100:50:50 கி.கி./ஹெக்டேர்.",
        "Apply basal dose in soil, then top-dress nitrogen in two equal splits with irrigation support.": "அடிப்படை அளவை மண்ணில் இடவும்; பிறகு நீர்ப்பாசனத்துடன் நைட்ரஜனை இரண்டு சம அளவாக மேல்சேர்க்கை செய்யவும்.",
        "Compost and vermicompost support steady root growth in maize.": "கம்போஸ்ட் மற்றும் வெர்மிகம்போஸ்ட் மக்காச்சோளத்தில் சீரான வேர் வளர்ச்சிக்கு உதவும்.",
        "2 times: land preparation and knee-high stage.": "2 முறை: நிலம் தயாரிக்கும் போது மற்றும் முழங்கால் உயர நிலை.",
        "3 to 4 tons compost per acre.": "ஒரு ஏக்கருக்கு 3 முதல் 4 டன் கம்போஸ்ட்.",
        "Apply during bed preparation and side-dress near rows after 25 days.": "படுக்கை தயாரிக்கும் போது இடவும்; 25 நாட்களுக்கு பிறகு வரிசைகளின் அருகில் மேல்சேர்க்கை செய்யவும்.",
        "Nitrogen is especially important during vegetative growth.": "தாவர வளர்ச்சி நிலையில் நைட்ரஜன் மிகவும் முக்கியமானது.",
        "3 times: basal, 25 days, 45 days.": "3 முறை: அடிப்படை, 25 நாள், 45 நாள்.",
        "NPK 120:60:40 kg/ha.": "NPK 120:60:40 கி.கி./ஹெக்டேர்.",
        "Place fertilizer 5 cm away from roots and irrigate lightly after application.": "வேர்களிலிருந்து 5 செ.மீ. தூரத்தில் உரம் வைத்து, பிறகு லேசாக நீர்ப்பாசனம் செய்யவும்.",
        "Organic matter improves fruit set and soil microbial activity.": "உயிர்ச்சத்து பொருள் பழ அமைப்பையும் மண்ணிலுள்ள நுண்ணுயிர் செயல்பாடையும் மேம்படுத்தும்.",
        "3 times: before transplanting, flowering, fruiting.": "3 முறை: நடவு முன், பூக்கும் போது, காய்க்கும் போது.",
        "2 to 3 tons compost per acre with bone meal if available.": "ஒரு ஏக்கருக்கு 2 முதல் 3 டன் கம்போஸ்ட்; கிடைத்தால் எலும்புத்தூள் சேர்க்கலாம்.",
        "Mix into raised beds and add light ring application around each plant later.": "உயர்த்தப்பட்ட படுக்கைகளில் கலக்கவும்; பின்னர் ஒவ்வொரு செடியைச் சுற்றியும் இலகுவாக வளையமாக இடவும்.",
        "Tomato needs balanced nutrition with slightly higher potassium during fruiting.": "காய்க்கும் நிலையில் சிறிது அதிக பொட்டாசியத்துடன் சமநிலை ஊட்டச்சத்து தக்காளிக்கு தேவை.",
        "3 to 4 times across growth stages.": "வளர்ச்சி நிலைகளில் 3 முதல் 4 முறை.",
        "NPK 75:40:60 kg/ha.": "NPK 75:40:60 கி.கி./ஹெக்டேர்.",
        "Apply basal dose first, then use split top dressings near drip line.": "முதலில் அடிப்படை அளவை இடவும்; பின்னர் டிரிப் வரிக்கு அருகில் பகுதியாக மேல்சேர்க்கை செய்யவும்.",
        "Well-rotted manure keeps the root zone active without burning plants.": "நன்றாக அழுகிய பண்ணை உரம் செடிகளை சேதப்படுத்தாமல் வேர் பகுதியைச் செயல்பாட்டில் வைத்திருக்கும்.",
        "2 times: basal and flowering stage.": "2 முறை: அடிப்படை மற்றும் பூக்கும் நிலை.",
        "2 tons compost per acre plus neem cake.": "ஒரு ஏக்கருக்கு 2 டன் கம்போஸ்ட் மற்றும் வேப்பம் பிண்ணாக்கு.",
        "Incorporate at bed formation and add a ring around plants later.": "படுக்கை உருவாக்கும் போது கலக்கவும்; பின்னர் செடிகளைச் சுற்றி வளையமாக இடவும்.",
        "Chilli benefits from split nutrition during flowering and fruit development.": "பூக்கும் மற்றும் காய் வளர்ச்சி நிலையில் பகுதியாக உரமிடுதல் மிளகாய்க்கு பயனளிக்கும்.",
        "3 times: basal, flowering, fruit set.": "3 முறை: அடிப்படை, பூக்கும் போது, காய் அமைக்கும் போது.",
        "NPK 60:30:30 kg/ha.": "NPK 60:30:30 கி.கி./ஹெக்டேர்.",
        "Use smaller split doses and avoid direct contact with stem base.": "சிறிய பகுதியாக அளிக்கவும்; தண்டு அடிப்பகுதியை நேரடியாகத் தொடாதீர்கள்.",
        "Organic manures support long-term tree health and fruit quality.": "உயிர்சத்து உரங்கள் மரத்தின் நீண்டகால ஆரோக்கியத்தையும் பழத் தரத்தையும் மேம்படுத்தும்.",
        "2 times per year: before flowering and after harvest.": "ஆண்டுக்கு 2 முறை: பூக்கும் முன் மற்றும் அறுவடை பிறகு.",
        "20 to 25 kg farmyard manure per tree.": "ஒரு மரத்திற்கு 20 முதல் 25 கிலோ பண்ணை உரம்.",
        "Apply in a circular trench around the canopy drip line and cover with soil.": "மரத்தின் டிரிப் வரியைச் சுற்றி வளையக் குழியில் இட்டு மண்ணால் மூடவும்.",
        "Tree nutrition should be stage-based and not over-applied.": "மரத்திற்கு வளர்ச்சி நிலையைப் பொறுத்து உரமிட வேண்டும்; அதிகமாக இடக்கூடாது.",
        "2 times per year.": "ஆண்டுக்கு 2 முறை.",
        "Per mature tree: NPK 1:0.5:1 kg active nutrient equivalent.": "முழுவளர்ந்த ஒரு மரத்திற்கு: NPK 1:0.5:1 கிலோ செயற்பாட்டு ஊட்டச்சத்து சமம்.",
        "Broadcast evenly around drip line and irrigate after application.": "டிரிப் வரியைச் சுற்றி சமமாகப் பரப்பி, பின்னர் நீர்ப்பாசனம் செய்யவும்.",
        "Banana needs rich organic matter for sustained growth.": "தொடர்ச்சியான வளர்ச்சிக்காக வாழைக்கு அதிக உயிர்சத்து தேவை.",
        "3 times: pit preparation, 45 days, 90 days.": "3 முறை: குழி தயாரிப்பு, 45 நாள், 90 நாள்.",
        "10 to 15 kg compost per plant annually.": "ஒரு செடிக்கு ஆண்டுக்கு 10 முதல் 15 கிலோ கம்போஸ்ட்.",
        "Apply in ring form away from pseudostem and cover lightly.": "போலி தண்டிலிருந்து விலகி வளையமாக இட்டு இலகுவாக மூடவும்.",
        "Banana is a heavy feeder, especially for potassium.": "வாழை அதிக ஊட்டச்சத்து தேவைப்படுகிற பயிர், குறிப்பாக பொட்டாசியம்.",
        "4 split doses through vegetative period.": "தாவர வளர்ச்சி காலத்தில் 4 பகுதிகளாக அளிக்கவும்.",
        "NPK 200:60:200 g per plant depending on variety.": "வகையைப் பொறுத்து ஒரு செடிக்கு NPK 200:60:200 கிராம்.",
        "Apply in split ring doses and irrigate immediately.": "வளைய வடிவில் பகுதியாக அளித்து உடனே நீர்ப்பாசனம் செய்யவும்.",
        "Organic inputs improve soil structure and moisture retention.": "உயிர்சத்து உள்ளீடுகள் மண் அமைப்பையும் ஈரத்தைக் காப்பதையும் மேம்படுத்தும்.",
        "2 times: basal and square formation stage.": "2 முறை: அடிப்படை மற்றும் கொத்து உருவாகும் நிலை.",
        "2 to 3 tons compost per acre.": "ஒரு ஏக்கருக்கு 2 முதல் 3 டன் கம்போஸ்ட்.",
        "Work into soil before sowing and side dress later near plant rows.": "விதைப்பு முன் மண்ணில் கலக்கவும்; பின்னர் செடி வரிசைகளின் அருகில் மேல்சேர்க்கை செய்யவும்.",
        "Balanced feeding helps boll formation without excess vegetative growth.": "அதிக இலை வளர்ச்சி இல்லாமல் கொட்டைகள் உருவாக சமநிலை உரமிடுதல் உதவும்.",
        "3 times across vegetative and flowering stages.": "தாவர மற்றும் பூக்கும் நிலைகளில் 3 முறை.",
        "Use split nitrogen applications and avoid heavy doses before rain.": "நைட்ரஜனை பகுதிகளாக அளிக்கவும்; மழைக்கு முன் அதிக அளவு இட வேண்டாம்.",
        "Apply compost before sowing and treat seed with biofertilizer.": "விதைப்பு முன் கம்போஸ்ட் இடவும்; விதைகளை உயிர் உரத்தால் சிகிச்சை செய்யவும்.",
        "Pulse crops respond well to moderate organic nutrition and bio-inputs.": "பருப்பு வகைகள் மிதமான உயிர்சத்து மற்றும் உயிர் உள்ளீடுகளுக்கு நன்றாக பதிலளிக்கும்.",
        "1 to 2 times: basal and early branching if needed.": "1 முதல் 2 முறை: அடிப்படை மற்றும் தேவைப்பட்டால் ஆரம்ப கிளைநிலை.",
        "1.5 to 2 tons compost per acre with Rhizobium inoculation.": "ஒரு ஏக்கருக்கு 1.5 முதல் 2 டன் கம்போஸ்ட் மற்றும் ரைசோபியம் சேர்த்தல்.",
        "Pulses require lower nitrogen but benefit from phosphorus support.": "பருப்புகளுக்கு நைட்ரஜன் குறைவாக வேண்டியாலும், பாஸ்பரஸ் ஆதரவு பயன் தரும்.",
        "1 basal application, optional light top-up.": "1 அடிப்படை பயன்பாடு; விருப்பமாக இலகு மேல்சேர்க்கை.",
        "NPK 20:50:20 kg/ha.": "NPK 20:50:20 கி.கி./ஹெக்டேர்.",
        "Place fertilizer below seed line at sowing time.": "விதைப்பு நேரத்தில் விதை வரிக்குக் கீழே உரம் இடவும்.",
        "Millets need light but steady nutrient support.": "சிறுதானியங்களுக்கு இலகுவான ஆனால் தொடர்ச்சியான ஊட்டச்சத்து ஆதரவு தேவை.",
        "1 to 2 times.": "1 முதல் 2 முறை.",
        "1 to 1.5 tons compost per acre.": "ஒரு ஏக்கருக்கு 1 முதல் 1.5 டன் கம்போஸ்ட்.",
        "Broadcast compost before sowing and incorporate lightly.": "விதைப்பு முன் கம்போஸ்டை பரப்பி இலகுவாக மண்ணில் கலக்கவும்.",
        "Millets usually need moderate fertilizer compared to paddy or maize.": "நெல் அல்லது மக்காச்சோளத்தை விட சிறுதானியங்களுக்கு பொதுவாக மிதமான உரம் போதுமானது.",
        "2 splits: basal and early tillering.": "2 பிரிவுகள்: அடிப்படை மற்றும் ஆரம்ப கிளை வளர்ச்சி.",
        "NPK 40:20:20 kg/ha.": "NPK 40:20:20 கி.கி./ஹெக்டேர்.",
        "Apply as basal and give a light nitrogen top-up after establishment.": "அடிப்படை உரமாக இடவும்; நிலைபெற்ற பிறகு இலகு நைட்ரஜன் மேல்சேர்க்கை செய்யவும்.",
    },
    "hindi": {
        "Rice": "धान",
        "Maize": "मक्का",
        "Tomato": "टमाटर",
        "Chilli": "मिर्च",
        "Mango": "आम",
        "Banana": "केला",
        "Cotton": "कपास",
        "Red Gram": "अरहर",
        "Foxtail Millet": "कंगनी",
        "Rice suits warm, humid conditions with soils that hold water well.": "गर्म और आर्द्र मौसम तथा पानी रोकने वाली मिट्टी में धान अच्छी तरह बढ़ता है।",
        "Maize performs well in well-drained soils with moderate heat and balanced moisture.": "अच्छी जल निकासी वाली मिट्टी, मध्यम गर्मी और संतुलित नमी में मक्का अच्छी उपज देता है।",
        "Tomato prefers soft, well-drained soil and moderate temperatures.": "नरम, अच्छी जल निकासी वाली मिट्टी और मध्यम तापमान टमाटर के लिए उपयुक्त हैं।",
        "Chilli grows best in lighter soils with quick drainage and warm weather.": "तेज जल निकासी वाली हल्की मिट्टी और गर्म मौसम में मिर्च सबसे अच्छी बढ़ती है।",
        "Mango suits warm regions and adapts well to many soils if waterlogging is avoided.": "यदि जलभराव न हो तो आम गर्म क्षेत्रों और कई प्रकार की मिट्टियों में अच्छी तरह अनुकूल हो जाता है।",
        "Banana responds well to fertile soil, warmth, and regular moisture.": "उपजाऊ मिट्टी, गर्माहट और नियमित नमी के साथ केला अच्छी तरह बढ़ता है।",
        "Cotton fits warm climates with good sunlight and moderately drained soils.": "अच्छी धूप, मध्यम जल निकासी वाली मिट्टी और गर्म जलवायु कपास के लिए उपयुक्त हैं।",
        "Red gram suits moderately dry regions and soils with quick drainage.": "मध्यम सूखे क्षेत्र और तेज जल निकासी वाली मिट्टी अरहर के लिए उपयुक्त हैं।",
        "Foxtail millet is ideal for lower water conditions and lighter soils.": "कम पानी की स्थिति और हल्की मिट्टी के लिए कंगनी आदर्श है।",
        "Use farmyard manure or compost before transplanting to improve water-holding soil structure.": "रोपाई से पहले गोबर की खाद या कम्पोस्ट डालने से पानी रोकने वाली मिट्टी की संरचना बेहतर होती है।",
        "2 times: base application and one top-up after 25 to 30 days.": "2 बार: एक बेसल डोज और 25 से 30 दिनों बाद एक टॉप-अप।",
        "5 to 8 tons compost per acre plus neem cake if available.": "प्रति एकड़ 5 से 8 टन कम्पोस्ट और उपलब्ध हो तो नीम खली।",
        "Mix compost into moist soil before planting, then apply a light side dressing near root zone.": "रोपाई से पहले नम मिट्टी में कम्पोस्ट मिलाएं, फिर जड़ क्षेत्र के पास हल्की साइड ड्रेसिंग दें।",
        "Balanced feeding helps rice maintain tiller growth and grain filling.": "संतुलित पोषण धान में टिलर वृद्धि और दाना भराव बनाए रखने में मदद करता है।",
        "3 splits: basal, tillering stage, panicle initiation.": "3 भागों में: बेसल, टिलरिंग अवस्था, पैनिकल शुरू होने पर।",
        "NPK 100:50:50 kg/ha in split doses.": "NPK 100:50:50 किग्रा/हेक्टेयर विभाजित मात्रा में।",
        "Apply basal dose in soil, then top-dress nitrogen in two equal splits with irrigation support.": "बेसल डोज मिट्टी में दें, फिर सिंचाई के साथ नाइट्रोजन को दो बराबर भागों में ऊपर से दें।",
        "Compost and vermicompost support steady root growth in maize.": "कम्पोस्ट और वर्मी-कम्पोस्ट मक्का में जड़ों की स्थिर वृद्धि में मदद करते हैं।",
        "2 times: land preparation and knee-high stage.": "2 बार: खेत तैयारी के समय और पौधा घुटने तक पहुंचने पर।",
        "3 to 4 tons compost per acre.": "प्रति एकड़ 3 से 4 टन कम्पोस्ट।",
        "Apply during bed preparation and side-dress near rows after 25 days.": "बेड तैयारी के समय दें और 25 दिनों बाद कतारों के पास साइड ड्रेसिंग करें।",
        "Nitrogen is especially important during vegetative growth.": "वनस्पतिक वृद्धि के दौरान नाइट्रोजन विशेष रूप से महत्वपूर्ण है।",
        "3 times: basal, 25 days, 45 days.": "3 बार: बेसल, 25 दिन, 45 दिन।",
        "NPK 120:60:40 kg/ha.": "NPK 120:60:40 किग्रा/हेक्टेयर।",
        "Place fertilizer 5 cm away from roots and irrigate lightly after application.": "जड़ों से 5 सेमी दूर खाद रखें और बाद में हल्की सिंचाई करें।",
        "Organic matter improves fruit set and soil microbial activity.": "जैविक पदार्थ फल बनने और मिट्टी की सूक्ष्मजीवी गतिविधि को बेहतर बनाते हैं।",
        "3 times: before transplanting, flowering, fruiting.": "3 बार: रोपाई से पहले, फूल आने पर, फल बनने पर।",
        "2 to 3 tons compost per acre with bone meal if available.": "प्रति एकड़ 2 से 3 टन कम्पोस्ट और उपलब्ध हो तो बोन मील।",
        "Mix into raised beds and add light ring application around each plant later.": "उठी हुई क्यारियों में मिलाएं और बाद में हर पौधे के चारों ओर हल्की रिंग डोज दें।",
        "Tomato needs balanced nutrition with slightly higher potassium during fruiting.": "फल बनने के समय थोड़े अधिक पोटाश के साथ संतुलित पोषण टमाटर के लिए आवश्यक है।",
        "3 to 4 times across growth stages.": "विकास की अवस्थाओं में 3 से 4 बार।",
        "NPK 75:40:60 kg/ha.": "NPK 75:40:60 किग्रा/हेक्टेयर।",
        "Apply basal dose first, then use split top dressings near drip line.": "पहले बेसल डोज दें, फिर ड्रिप लाइन के पास विभाजित टॉप ड्रेसिंग करें।",
        "Well-rotted manure keeps the root zone active without burning plants.": "अच्छी तरह सड़ी हुई खाद पौधों को नुकसान पहुंचाए बिना जड़ क्षेत्र को सक्रिय रखती है।",
        "2 times: basal and flowering stage.": "2 बार: बेसल और फूल आने की अवस्था।",
        "2 tons compost per acre plus neem cake.": "प्रति एकड़ 2 टन कम्पोस्ट और नीम खली।",
        "Incorporate at bed formation and add a ring around plants later.": "क्यारी बनाते समय मिलाएं और बाद में पौधों के चारों ओर रिंग के रूप में दें।",
        "Chilli benefits from split nutrition during flowering and fruit development.": "फूल और फल विकास के दौरान विभाजित पोषण मिर्च के लिए लाभकारी है।",
        "3 times: basal, flowering, fruit set.": "3 बार: बेसल, फूल आने पर, फल सेट होने पर।",
        "NPK 60:30:30 kg/ha.": "NPK 60:30:30 किग्रा/हेक्टेयर।",
        "Use smaller split doses and avoid direct contact with stem base.": "छोटी विभाजित मात्रा दें और तने के आधार से सीधा संपर्क न होने दें।",
        "Organic manures support long-term tree health and fruit quality.": "जैविक खादें पेड़ के लंबे समय के स्वास्थ्य और फल की गुणवत्ता को बेहतर बनाती हैं।",
        "2 times per year: before flowering and after harvest.": "साल में 2 बार: फूल आने से पहले और कटाई के बाद।",
        "20 to 25 kg farmyard manure per tree.": "प्रति पेड़ 20 से 25 किलोग्राम गोबर की खाद।",
        "Apply in a circular trench around the canopy drip line and cover with soil.": "छत्र के ड्रिप लाइन के चारों ओर गोलाई में नाली बनाकर खाद दें और मिट्टी से ढक दें।",
        "Tree nutrition should be stage-based and not over-applied.": "पेड़ को उसकी अवस्था के अनुसार पोषण दें, अधिक मात्रा न दें।",
        "2 times per year.": "साल में 2 बार।",
        "Per mature tree: NPK 1:0.5:1 kg active nutrient equivalent.": "प्रति परिपक्व पेड़: NPK 1:0.5:1 किग्रा सक्रिय पोषक तत्व के बराबर।",
        "Broadcast evenly around drip line and irrigate after application.": "ड्रिप लाइन के चारों ओर समान रूप से बिखेरें और बाद में सिंचाई करें।",
        "Banana needs rich organic matter for sustained growth.": "लगातार वृद्धि के लिए केले को भरपूर जैविक पदार्थ चाहिए।",
        "3 times: pit preparation, 45 days, 90 days.": "3 बार: गड्ढा तैयारी, 45 दिन, 90 दिन।",
        "10 to 15 kg compost per plant annually.": "प्रति पौधा सालाना 10 से 15 किग्रा कम्पोस्ट।",
        "Apply in ring form away from pseudostem and cover lightly.": "कृत्रिम तने से दूर रिंग के रूप में दें और हल्के से ढक दें।",
        "Banana is a heavy feeder, especially for potassium.": "केला अधिक पोषण लेने वाली फसल है, खासकर पोटाश के लिए।",
        "4 split doses through vegetative period.": "वनस्पतिक अवधि में 4 विभाजित मात्राएं।",
        "NPK 200:60:200 g per plant depending on variety.": "किस्म के अनुसार प्रति पौधा NPK 200:60:200 ग्राम।",
        "Apply in split ring doses and irrigate immediately.": "विभाजित रिंग डोज के रूप में दें और तुरंत सिंचाई करें।",
        "Organic inputs improve soil structure and moisture retention.": "जैविक इनपुट मिट्टी की संरचना और नमी संरक्षण को बेहतर बनाते हैं।",
        "2 times: basal and square formation stage.": "2 बार: बेसल और स्क्वायर बनने की अवस्था।",
        "2 to 3 tons compost per acre.": "प्रति एकड़ 2 से 3 टन कम्पोस्ट।",
        "Work into soil before sowing and side dress later near plant rows.": "बुवाई से पहले मिट्टी में मिलाएं और बाद में पौधों की कतारों के पास साइड ड्रेसिंग करें।",
        "Balanced feeding helps boll formation without excess vegetative growth.": "संतुलित पोषण अत्यधिक वनस्पतिक वृद्धि के बिना बॉल बनने में मदद करता है।",
        "3 times across vegetative and flowering stages.": "वनस्पतिक और फूल अवस्था में 3 बार।",
        "Use split nitrogen applications and avoid heavy doses before rain.": "नाइट्रोजन को भागों में दें और बारिश से पहले भारी मात्रा न डालें।",
        "Apply compost before sowing and treat seed with biofertilizer.": "बुवाई से पहले कम्पोस्ट दें और बीज को जैव उर्वरक से उपचारित करें।",
        "Pulse crops respond well to moderate organic nutrition and bio-inputs.": "दलहनी फसलें मध्यम जैविक पोषण और जैव इनपुट पर अच्छा प्रतिसाद देती हैं।",
        "1 to 2 times: basal and early branching if needed.": "1 से 2 बार: बेसल और जरूरत हो तो शुरुआती शाखा अवस्था में।",
        "1.5 to 2 tons compost per acre with Rhizobium inoculation.": "प्रति एकड़ 1.5 से 2 टन कम्पोस्ट और राइजोबियम उपचार।",
        "Pulses require lower nitrogen but benefit from phosphorus support.": "दलहनी फसलों को कम नाइट्रोजन चाहिए, लेकिन फॉस्फोरस का सहारा लाभकारी होता है।",
        "1 basal application, optional light top-up.": "1 बेसल डोज, जरूरत हो तो हल्का टॉप-अप।",
        "NPK 20:50:20 kg/ha.": "NPK 20:50:20 किग्रा/हेक्टेयर।",
        "Place fertilizer below seed line at sowing time.": "बुवाई के समय खाद को बीज रेखा के नीचे रखें।",
        "Millets need light but steady nutrient support.": "मोटे अनाजों को हल्का लेकिन नियमित पोषण समर्थन चाहिए।",
        "1 to 2 times.": "1 से 2 बार।",
        "1 to 1.5 tons compost per acre.": "प्रति एकड़ 1 से 1.5 टन कम्पोस्ट।",
        "Broadcast compost before sowing and incorporate lightly.": "बुवाई से पहले कम्पोस्ट बिखेरें और हल्के से मिट्टी में मिला दें।",
        "Millets usually need moderate fertilizer compared to paddy or maize.": "धान या मक्का की तुलना में मोटे अनाजों को सामान्यतः मध्यम मात्रा में उर्वरक चाहिए।",
        "2 splits: basal and early tillering.": "2 भागों में: बेसल और शुरुआती टिलरिंग।",
        "NPK 40:20:20 kg/ha.": "NPK 40:20:20 किग्रा/हेक्टेयर।",
        "Apply as basal and give a light nitrogen top-up after establishment.": "बेसल के रूप में दें और पौधे जमने के बाद हल्का नाइट्रोजन टॉप-अप करें।",
    },
}


DYNAMIC_TEXTS = {
    "english": {
        "soil_color_match": "Soil color matches {value} soil preference.",
        "soil_texture_match": "Soil texture matches {value} condition.",
        "water_absorption_match": "Water absorption pattern supports {crop}.",
        "temperature_ok": "Current temperature is suitable for healthy growth.",
        "humidity_ok": "Current humidity is within the crop comfort range.",
        "rain_ok": "Rain chances are acceptable for this crop.",
        "tip_heat": "Heat is high now, so give plants extra water in early morning or evening.",
        "tip_cold": "Temperature is low, so avoid overwatering and protect young plants from stress.",
        "tip_rain": "Rain is likely, so irrigation is not needed right now.",
        "tip_humidity_high": "Humidity is high, so disease risk is higher. Check leaves for fungal symptoms.",
        "tip_humidity_low": "Air is dry, so mulch can help keep root-zone moisture stable.",
        "tip_default": "Weather looks stable now. Continue regular irrigation and field monitoring.",
    },
    "telugu": {
        "soil_color_match": "నేల రంగు {value} ఎంపికకు సరిపోతుంది.",
        "soil_texture_match": "నేల గుణము {value} పరిస్థితికి సరిపోతుంది.",
        "water_absorption_match": "నీరు పీల్చుకునే స్వభావం {crop} పంటకు అనుకూలంగా ఉంది.",
        "temperature_ok": "ప్రస్తుత ఉష్ణోగ్రత ఆరోగ్యకరమైన పెరుగుదలకు అనుకూలంగా ఉంది.",
        "humidity_ok": "ప్రస్తుత తేమ ఈ పంటకు అనుకూల పరిమితిలో ఉంది.",
        "rain_ok": "వర్షం అవకాశం ఈ పంటకు అనుకూలంగా ఉంది.",
        "tip_heat": "ఇప్పుడు వేడి ఎక్కువగా ఉంది కాబట్టి ఉదయం లేదా సాయంత్రం అదనంగా నీరు ఇవ్వండి.",
        "tip_cold": "ఉష్ణోగ్రత తక్కువగా ఉంది కాబట్టి అధికంగా నీరు పెట్టకండి, చిన్న మొక్కలను ఒత్తిడినుంచి కాపాడండి.",
        "tip_rain": "వర్షం వచ్చే అవకాశం ఉంది కాబట్టి ప్రస్తుతం నీటిపారుదల అవసరం లేదు.",
        "tip_humidity_high": "తేమ ఎక్కువగా ఉంది కాబట్టి వ్యాధుల ముప్పు పెరుగుతుంది. ఆకులపై ఫంగస్ లక్షణాలు ఉన్నాయో చూడండి.",
        "tip_humidity_low": "గాలి పొడిగా ఉంది కాబట్టి మల్చింగ్ చేస్తే వేర్ల దగ్గర తేమ నిల్వగా ఉంటుంది.",
        "tip_default": "ప్రస్తుతం వాతావరణం స్థిరంగా ఉంది. నియమిత నీటిపారుదల మరియు పొలం పర్యవేక్షణ కొనసాగించండి.",
    },
    "tamil": {
        "soil_color_match": "மண் நிறம் {value} இந்த பயிருக்கான விருப்பத்துடன் பொருந்துகிறது.",
        "soil_texture_match": "மண் தன்மை {value} நிலைக்கு பொருந்துகிறது.",
        "water_absorption_match": "நீர் உறிஞ்சும் தன்மை {crop} பயிருக்குப் பொருத்தமாக உள்ளது.",
        "temperature_ok": "தற்போதைய வெப்பநிலை ஆரோக்கியமான வளர்ச்சிக்கு ஏற்றதாக உள்ளது.",
        "humidity_ok": "தற்போதைய ஈரப்பதம் இந்த பயிருக்கான ஏற்ற வரம்பில் உள்ளது.",
        "rain_ok": "மழை வாய்ப்பு இந்த பயிருக்குப் பொருத்தமாக உள்ளது.",
        "tip_heat": "இப்போது வெப்பம் அதிகமாக உள்ளது; அதிகாலை அல்லது மாலையில் கூடுதல் நீர் வழங்குங்கள்.",
        "tip_cold": "வெப்பநிலை குறைவாக உள்ளது; அதிக நீர் விடாதீர்கள், இளம் செடிகளை அழுத்தத்திலிருந்து காக்கவும்.",
        "tip_rain": "மழை பெய்ய வாய்ப்பு உள்ளது; அதனால் இப்போது பாசனம் தேவையில்லை.",
        "tip_humidity_high": "ஈரப்பதம் அதிகமாக உள்ளது; நோய் அபாயம் உயரும். இலைகளில் பூஞ்சை அறிகுறிகள் உள்ளனவா பார்க்கவும்.",
        "tip_humidity_low": "காற்று உலர்ந்துள்ளது; அதனால் மல்சிங் செய்தால் வேர் பகுதிக்கு அருகில் ஈரம் தங்கும்.",
        "tip_default": "தற்போது வானிலை நிலையாக உள்ளது. வழக்கமான பாசனமும் வயல் கண்காணிப்பும் தொடருங்கள்.",
    },
    "hindi": {
        "soil_color_match": "मिट्टी का रंग {value} इस फसल की पसंद से मेल खाता है।",
        "soil_texture_match": "मिट्टी की बनावट {value} स्थिति से मेल खाती है।",
        "water_absorption_match": "पानी सोखने का स्वभाव {crop} फसल के लिए उपयुक्त है।",
        "temperature_ok": "वर्तमान तापमान स्वस्थ वृद्धि के लिए उपयुक्त है।",
        "humidity_ok": "वर्तमान नमी इस फसल की अनुकूल सीमा में है।",
        "rain_ok": "बारिश की संभावना इस फसल के लिए स्वीकार्य है।",
        "tip_heat": "अभी गर्मी ज्यादा है, इसलिए सुबह जल्दी या शाम को अतिरिक्त पानी दें।",
        "tip_cold": "तापमान कम है, इसलिए ज्यादा सिंचाई न करें और छोटे पौधों को तनाव से बचाएं।",
        "tip_rain": "बारिश की संभावना है, इसलिए अभी सिंचाई की जरूरत नहीं है।",
        "tip_humidity_high": "नमी ज्यादा है, इसलिए रोग का खतरा बढ़ सकता है। पत्तियों पर फफूंद के लक्षण देखें।",
        "tip_humidity_low": "हवा सूखी है, इसलिए मल्चिंग करने से जड़ों के पास नमी बनी रहेगी।",
        "tip_default": "अभी मौसम स्थिर है। नियमित सिंचाई और खेत की निगरानी जारी रखें।",
    },
}


def translate_exact_text(text, language):
    return EXACT_TEXT_TRANSLATIONS.get(language, {}).get(text, text)


def dynamic_text(language, key, **values):
    lang_pack = DYNAMIC_TEXTS.get(language, DYNAMIC_TEXTS["english"])
    template = lang_pack.get(key, DYNAMIC_TEXTS["english"][key])
    return template.format(**values)


COUNTRY_REGIONS = {
    "India": ["Andhra Pradesh", "Telangana", "Tamil Nadu", "Punjab", "Karnataka", "Maharashtra"],
    "USA": ["California", "Texas", "Florida"],
    "Australia": ["Queensland", "Victoria"],
}


CROP_CATALOG = [
    {
        "name": "Rice",
        "category": "grains",
        "countries": ["India"],
        "regions": ["Andhra Pradesh", "Telangana", "Tamil Nadu"],
        "seasons": ["kharif"],
        "soil_color": ["black", "brown"],
        "texture": ["sticky", "soft"],
        "water_absorption": ["slow"],
        "temperature": (24, 34),
        "humidity": (70, 92),
        "rainfall": (100, 400),
        "why": "Rice suits warm, humid conditions with soils that hold water well.",
        "fertilizer": {
            "organic": {
                "details": "Use farmyard manure or compost before transplanting to improve water-holding soil structure.",
                "schedule": "2 times: base application and one top-up after 25 to 30 days.",
                "ratio": "5 to 8 tons compost per acre plus neem cake if available.",
                "method": "Mix compost into moist soil before planting, then apply a light side dressing near root zone.",
            },
            "chemical": {
                "details": "Balanced feeding helps rice maintain tiller growth and grain filling.",
                "schedule": "3 splits: basal, tillering stage, panicle initiation.",
                "ratio": "NPK 100:50:50 kg/ha in split doses.",
                "method": "Apply basal dose in soil, then top-dress nitrogen in two equal splits with irrigation support.",
            },
        },
    },
    {
        "name": "Maize",
        "category": "grains",
        "countries": ["India", "USA"],
        "regions": ["Karnataka", "Maharashtra", "Texas", "Punjab"],
        "seasons": ["kharif", "summer"],
        "soil_color": ["brown", "black"],
        "texture": ["soft", "dry"],
        "water_absorption": ["fast", "slow"],
        "temperature": (20, 32),
        "humidity": (45, 75),
        "rainfall": (60, 180),
        "why": "Maize performs well in well-drained soils with moderate heat and balanced moisture.",
        "fertilizer": {
            "organic": {
                "details": "Compost and vermicompost support steady root growth in maize.",
                "schedule": "2 times: land preparation and knee-high stage.",
                "ratio": "3 to 4 tons compost per acre.",
                "method": "Apply during bed preparation and side-dress near rows after 25 days.",
            },
            "chemical": {
                "details": "Nitrogen is especially important during vegetative growth.",
                "schedule": "3 times: basal, 25 days, 45 days.",
                "ratio": "NPK 120:60:40 kg/ha.",
                "method": "Place fertilizer 5 cm away from roots and irrigate lightly after application.",
            },
        },
    },
    {
        "name": "Tomato",
        "category": "vegetables",
        "countries": ["India", "USA"],
        "regions": ["Andhra Pradesh", "Karnataka", "California", "Tamil Nadu"],
        "seasons": ["rabi", "summer"],
        "soil_color": ["red", "brown"],
        "texture": ["soft", "dry"],
        "water_absorption": ["fast", "slow"],
        "temperature": (18, 30),
        "humidity": (45, 75),
        "rainfall": (20, 120),
        "why": "Tomato prefers soft, well-drained soil and moderate temperatures.",
        "fertilizer": {
            "organic": {
                "details": "Organic matter improves fruit set and soil microbial activity.",
                "schedule": "3 times: before transplanting, flowering, fruiting.",
                "ratio": "2 to 3 tons compost per acre with bone meal if available.",
                "method": "Mix into raised beds and add light ring application around each plant later.",
            },
            "chemical": {
                "details": "Tomato needs balanced nutrition with slightly higher potassium during fruiting.",
                "schedule": "3 to 4 times across growth stages.",
                "ratio": "NPK 75:40:60 kg/ha.",
                "method": "Apply basal dose first, then use split top dressings near drip line.",
            },
        },
    },
    {
        "name": "Chilli",
        "category": "vegetables",
        "countries": ["India"],
        "regions": ["Andhra Pradesh", "Telangana", "Tamil Nadu"],
        "seasons": ["rabi", "summer"],
        "soil_color": ["red", "brown"],
        "texture": ["dry", "soft"],
        "water_absorption": ["fast"],
        "temperature": (20, 34),
        "humidity": (40, 70),
        "rainfall": (20, 100),
        "why": "Chilli grows best in lighter soils with quick drainage and warm weather.",
        "fertilizer": {
            "organic": {
                "details": "Well-rotted manure keeps the root zone active without burning plants.",
                "schedule": "2 times: basal and flowering stage.",
                "ratio": "2 tons compost per acre plus neem cake.",
                "method": "Incorporate at bed formation and add a ring around plants later.",
            },
            "chemical": {
                "details": "Chilli benefits from split nutrition during flowering and fruit development.",
                "schedule": "3 times: basal, flowering, fruit set.",
                "ratio": "NPK 60:30:30 kg/ha.",
                "method": "Use smaller split doses and avoid direct contact with stem base.",
            },
        },
    },
    {
        "name": "Mango",
        "category": "fruits",
        "countries": ["India", "Australia"],
        "regions": ["Andhra Pradesh", "Telangana", "Maharashtra", "Queensland"],
        "seasons": ["year_round"],
        "soil_color": ["red", "brown", "black"],
        "texture": ["soft", "dry"],
        "water_absorption": ["fast", "slow"],
        "temperature": (24, 38),
        "humidity": (40, 75),
        "rainfall": (30, 250),
        "why": "Mango suits warm regions and adapts well to many soils if waterlogging is avoided.",
        "fertilizer": {
            "organic": {
                "details": "Organic manures support long-term tree health and fruit quality.",
                "schedule": "2 times per year: before flowering and after harvest.",
                "ratio": "20 to 25 kg farmyard manure per tree.",
                "method": "Apply in a circular trench around the canopy drip line and cover with soil.",
            },
            "chemical": {
                "details": "Tree nutrition should be stage-based and not over-applied.",
                "schedule": "2 times per year.",
                "ratio": "Per mature tree: NPK 1:0.5:1 kg active nutrient equivalent.",
                "method": "Broadcast evenly around drip line and irrigate after application.",
            },
        },
    },
    {
        "name": "Banana",
        "category": "fruits",
        "countries": ["India"],
        "regions": ["Tamil Nadu", "Andhra Pradesh", "Maharashtra"],
        "seasons": ["year_round"],
        "soil_color": ["brown", "black"],
        "texture": ["soft", "sticky"],
        "water_absorption": ["slow", "fast"],
        "temperature": (22, 35),
        "humidity": (55, 90),
        "rainfall": (60, 220),
        "why": "Banana responds well to fertile soil, warmth, and regular moisture.",
        "fertilizer": {
            "organic": {
                "details": "Banana needs rich organic matter for sustained growth.",
                "schedule": "3 times: pit preparation, 45 days, 90 days.",
                "ratio": "10 to 15 kg compost per plant annually.",
                "method": "Apply in ring form away from pseudostem and cover lightly.",
            },
            "chemical": {
                "details": "Banana is a heavy feeder, especially for potassium.",
                "schedule": "4 split doses through vegetative period.",
                "ratio": "NPK 200:60:200 g per plant depending on variety.",
                "method": "Apply in split ring doses and irrigate immediately.",
            },
        },
    },
    {
        "name": "Cotton",
        "category": "cash_crops",
        "countries": ["India", "USA", "Australia"],
        "regions": ["Telangana", "Maharashtra", "Texas", "Victoria"],
        "seasons": ["kharif"],
        "soil_color": ["black", "brown"],
        "texture": ["soft", "dry"],
        "water_absorption": ["slow", "fast"],
        "temperature": (22, 36),
        "humidity": (35, 70),
        "rainfall": (40, 150),
        "why": "Cotton fits warm climates with good sunlight and moderately drained soils.",
        "fertilizer": {
            "organic": {
                "details": "Organic inputs improve soil structure and moisture retention.",
                "schedule": "2 times: basal and square formation stage.",
                "ratio": "2 to 3 tons compost per acre.",
                "method": "Work into soil before sowing and side dress later near plant rows.",
            },
            "chemical": {
                "details": "Balanced feeding helps boll formation without excess vegetative growth.",
                "schedule": "3 times across vegetative and flowering stages.",
                "ratio": "NPK 100:50:50 kg/ha.",
                "method": "Use split nitrogen applications and avoid heavy doses before rain.",
            },
        },
    },
    {
        "name": "Red Gram",
        "category": "pulses",
        "countries": ["India"],
        "regions": ["Andhra Pradesh", "Karnataka", "Maharashtra"],
        "seasons": ["kharif"],
        "soil_color": ["red", "brown"],
        "texture": ["dry", "soft"],
        "water_absorption": ["fast"],
        "temperature": (20, 34),
        "humidity": (35, 70),
        "rainfall": (50, 140),
        "why": "Red gram suits moderately dry regions and soils with quick drainage.",
        "fertilizer": {
            "organic": {
                "details": "Pulse crops respond well to moderate organic nutrition and bio-inputs.",
                "schedule": "1 to 2 times: basal and early branching if needed.",
                "ratio": "1.5 to 2 tons compost per acre with Rhizobium inoculation.",
                "method": "Apply compost before sowing and treat seed with biofertilizer.",
            },
            "chemical": {
                "details": "Pulses require lower nitrogen but benefit from phosphorus support.",
                "schedule": "1 basal application, optional light top-up.",
                "ratio": "NPK 20:50:20 kg/ha.",
                "method": "Place fertilizer below seed line at sowing time.",
            },
        },
    },
    {
        "name": "Foxtail Millet",
        "category": "millets",
        "countries": ["India"],
        "regions": ["Andhra Pradesh", "Karnataka", "Tamil Nadu"],
        "seasons": ["kharif", "rabi"],
        "soil_color": ["red", "brown"],
        "texture": ["dry", "soft"],
        "water_absorption": ["fast"],
        "temperature": (18, 32),
        "humidity": (30, 65),
        "rainfall": (30, 110),
        "why": "Foxtail millet is ideal for lower water conditions and lighter soils.",
        "fertilizer": {
            "organic": {
                "details": "Millets need light but steady nutrient support.",
                "schedule": "1 to 2 times.",
                "ratio": "1 to 1.5 tons compost per acre.",
                "method": "Broadcast compost before sowing and incorporate lightly.",
            },
            "chemical": {
                "details": "Millets usually need moderate fertilizer compared to paddy or maize.",
                "schedule": "2 splits: basal and early tillering.",
                "ratio": "NPK 40:20:20 kg/ha.",
                "method": "Apply as basal and give a light nitrogen top-up after establishment.",
            },
        },
    },
]

CROP_CATALOG.extend(
    [
        {
            "name": "Orange",
            "category": "fruits",
            "countries": ["USA"],
            "regions": ["Florida", "California"],
            "seasons": ["year_round"],
            "soil_color": ["brown", "red"],
            "texture": ["soft", "dry"],
            "water_absorption": ["fast", "slow"],
            "temperature": (16, 32),
            "humidity": (45, 80),
            "rainfall": (40, 180),
            "why": "Orange grows well in sunny subtropical regions with moderate moisture and good drainage.",
            "fertilizer": {
                "organic": {
                    "details": "Compost and citrus-friendly organic manure support steady flowering and fruit quality.",
                    "schedule": "2 to 3 times per year.",
                    "ratio": "15 to 20 kg compost per mature tree.",
                    "method": "Apply around the drip line and lightly incorporate into soil.",
                },
                "chemical": {
                    "details": "Balanced nutrition with nitrogen and potash supports fruit development in citrus.",
                    "schedule": "3 split doses in active growth periods.",
                    "ratio": "NPK 1:0.5:1 per mature tree equivalent, adjusted by age.",
                    "method": "Broadcast evenly around canopy edge and irrigate after application.",
                },
            },
        },
        {
            "name": "Soybean",
            "category": "pulses",
            "countries": ["USA"],
            "regions": ["Texas", "Florida"],
            "seasons": ["kharif", "summer"],
            "soil_color": ["brown", "black"],
            "texture": ["soft", "dry"],
            "water_absorption": ["fast", "slow"],
            "temperature": (20, 32),
            "humidity": (40, 75),
            "rainfall": (50, 160),
            "why": "Soybean suits warm conditions, moderate rainfall, and well-drained fertile soils.",
            "fertilizer": {
                "organic": {
                    "details": "Moderate compost and bio-inputs support nodulation and steady growth.",
                    "schedule": "1 to 2 times.",
                    "ratio": "1.5 to 2 tons compost per acre with Rhizobium treatment.",
                    "method": "Apply before sowing and use biofertilizer-treated seed.",
                },
                "chemical": {
                    "details": "Soybean needs moderate phosphorus support and limited nitrogen.",
                    "schedule": "1 basal dose, optional correction later.",
                    "ratio": "NPK 20:60:20 kg/ha.",
                    "method": "Band place below seed line at sowing time.",
                },
            },
        },
        {
            "name": "Lettuce",
            "category": "vegetables",
            "countries": ["USA", "Australia"],
            "regions": ["California", "Victoria", "Queensland"],
            "seasons": ["rabi", "summer"],
            "soil_color": ["brown", "red"],
            "texture": ["soft"],
            "water_absorption": ["fast", "slow"],
            "temperature": (12, 24),
            "humidity": (45, 75),
            "rainfall": (20, 100),
            "why": "Lettuce prefers mild temperatures, light fertile soil, and regular moisture without waterlogging.",
            "fertilizer": {
                "organic": {
                    "details": "Fine compost improves leaf growth and soil softness for lettuce beds.",
                    "schedule": "2 times: bed preparation and early leaf stage.",
                    "ratio": "1.5 to 2 tons compost per acre.",
                    "method": "Mix into topsoil before sowing and add a light side dressing later.",
                },
                "chemical": {
                    "details": "Light and balanced feeding supports leafy growth without tip burn.",
                    "schedule": "2 split doses.",
                    "ratio": "NPK 40:20:20 kg/ha.",
                    "method": "Apply in light doses near rows followed by gentle irrigation.",
                },
            },
        },
        {
            "name": "Wheat",
            "category": "grains",
            "countries": ["USA", "Australia"],
            "regions": ["Texas", "Victoria", "Queensland"],
            "seasons": ["rabi"],
            "soil_color": ["brown", "black"],
            "texture": ["soft", "dry"],
            "water_absorption": ["fast", "slow"],
            "temperature": (10, 25),
            "humidity": (35, 70),
            "rainfall": (30, 120),
            "why": "Wheat suits cooler seasons, moderate moisture, and well-drained loamy soils.",
            "fertilizer": {
                "organic": {
                    "details": "Well-decomposed manure improves soil tilth and moisture balance for wheat.",
                    "schedule": "1 to 2 times.",
                    "ratio": "2 tons compost per acre.",
                    "method": "Incorporate before sowing and add light top dressing if needed.",
                },
                "chemical": {
                    "details": "Wheat responds well to balanced basal fertilization and timely nitrogen top-up.",
                    "schedule": "2 to 3 splits.",
                    "ratio": "NPK 100:50:40 kg/ha.",
                    "method": "Apply basal dose before sowing and split nitrogen at crown root and tillering stages.",
                },
            },
        },
        {
            "name": "Chickpea",
            "category": "pulses",
            "countries": ["Australia"],
            "regions": ["Victoria", "Queensland"],
            "seasons": ["rabi"],
            "soil_color": ["brown", "red"],
            "texture": ["dry", "soft"],
            "water_absorption": ["fast"],
            "temperature": (15, 28),
            "humidity": (30, 65),
            "rainfall": (25, 100),
            "why": "Chickpea performs well in cooler dry-season conditions with lighter, well-drained soils.",
            "fertilizer": {
                "organic": {
                    "details": "Moderate compost and biofertilizer support healthy root activity in chickpea.",
                    "schedule": "1 to 2 times.",
                    "ratio": "1 to 1.5 tons compost per acre.",
                    "method": "Apply before sowing and use bio-inoculated seed.",
                },
                "chemical": {
                    "details": "Chickpea needs modest fertilizer with phosphorus support more than nitrogen.",
                    "schedule": "1 basal dose.",
                    "ratio": "NPK 20:50:20 kg/ha.",
                    "method": "Place below seed zone during sowing.",
                },
            },
        },
        {
            "name": "Sugarcane",
            "category": "cash_crops",
            "countries": ["Australia", "USA"],
            "regions": ["Queensland", "Florida"],
            "seasons": ["year_round", "summer"],
            "soil_color": ["brown", "black", "red"],
            "texture": ["soft", "sticky"],
            "water_absorption": ["slow", "fast"],
            "temperature": (22, 36),
            "humidity": (50, 85),
            "rainfall": (80, 250),
            "why": "Sugarcane needs warmth, steady moisture, and fertile soils for strong cane growth.",
            "fertilizer": {
                "organic": {
                    "details": "Heavy compost and organic matter support long-duration sugarcane growth.",
                    "schedule": "2 to 3 times.",
                    "ratio": "4 to 6 tons compost per acre.",
                    "method": "Apply in furrows before planting and top up along rows later.",
                },
                "chemical": {
                    "details": "Sugarcane responds to higher nutrient supply over a long growing period.",
                    "schedule": "3 split doses.",
                    "ratio": "NPK 150:60:60 kg/ha.",
                    "method": "Apply basal dose in furrows and split nitrogen during early growth stages.",
                },
            },
        },
        {
            "name": "Avocado",
            "category": "fruits",
            "countries": ["Australia"],
            "regions": ["Queensland", "Victoria"],
            "seasons": ["year_round"],
            "soil_color": ["brown", "red"],
            "texture": ["soft", "dry"],
            "water_absorption": ["fast"],
            "temperature": (16, 30),
            "humidity": (45, 75),
            "rainfall": (40, 180),
            "why": "Avocado grows best in frost-safe regions with good drainage and steady moisture.",
            "fertilizer": {
                "organic": {
                    "details": "Organic mulches and compost support soil biology and root-zone stability in avocado.",
                    "schedule": "2 times per year.",
                    "ratio": "10 to 15 kg compost per tree.",
                    "method": "Apply around the drip line and keep mulch away from the trunk base.",
                },
                "chemical": {
                    "details": "Stage-based balanced feeding supports vegetative growth and fruit set in avocado.",
                    "schedule": "2 to 3 times per year.",
                    "ratio": "Balanced NPK by tree age and canopy size.",
                    "method": "Apply evenly around root zone and irrigate afterward.",
                },
            },
        },
    ]
)


def get_translation(language):
    return TRANSLATIONS.get(language, TRANSLATIONS["english"])


def is_mobile_request():
    user_agent = request.headers.get("User-Agent", "").lower()
    return any(keyword in user_agent for keyword in MOBILE_KEYWORDS)


def get_region_options(country):
    return COUNTRY_REGIONS.get(country, [])


def normalize_form(form):
    return {
        "country": form.get("country", "India"),
        "region": form.get("region", "Andhra Pradesh"),
        "season": form.get("season", "kharif").lower(),
        "category": form.get("category", "vegetables").lower(),
        "language": form.get("language", "english").lower(),
        "soil_color": form.get("soil_color", "black").lower(),
        "texture": form.get("texture", "soft").lower(),
        "water_absorption": form.get("water_absorption", "slow").lower(),
        "temperature": parse_float(form.get("weather_temperature")),
        "humidity": parse_float(form.get("weather_humidity")),
        "rain_probability": parse_float(form.get("weather_rain_probability")),
        "weather_code": parse_float(form.get("weather_code")),
        "weather_status": form.get("weather_status", "unavailable"),
    }


def parse_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def score_crop(crop, user_input):
    score = 0
    reasons = []
    language = user_input.get("language", "english")
    translation = get_translation(language)
    localized_crop_name = localize_crop_name(crop["name"], language)
    soil_color_label = translation.get(user_input["soil_color"], user_input["soil_color"].title())
    texture_label = translation.get(user_input["texture"], user_input["texture"])

    if user_input["soil_color"] in crop["soil_color"]:
        score += 2
        if language == "telugu":
            reasons.append(f"నేల రంగు {soil_color_label} ఎంపికకు సరిపోతుంది.")
        else:
            reasons.append(f"Soil color matches {soil_color_label} soil preference.")
    if user_input["texture"] in crop["texture"]:
        score += 2
        if language == "telugu":
            reasons.append(f"నేల గుణము {texture_label} పరిస్థితికి సరిపోతుంది.")
        else:
            reasons.append(f"Soil texture matches {texture_label} condition.")
    if user_input["water_absorption"] in crop["water_absorption"]:
        score += 2
        if language == "telugu":
            reasons.append(f"నీరు పీల్చుకునే స్వభావం {localized_crop_name} పంటకు అనుకూలంగా ఉంది.")
        else:
            reasons.append(f"Water absorption pattern supports {localized_crop_name}.")

    temperature = user_input["temperature"]
    humidity = user_input["humidity"]
    rain_probability = user_input["rain_probability"]

    if temperature is not None:
        if crop["temperature"][0] <= temperature <= crop["temperature"][1]:
            score += 3
            reasons.append("ప్రస్తుత ఉష్ణోగ్రత ఆరోగ్యకరమైన పెరుగుదలకు అనుకూలంగా ఉంది." if language == "telugu" else "Current temperature is suitable for healthy growth.")
        else:
            score -= 1

    if humidity is not None:
        if crop["humidity"][0] <= humidity <= crop["humidity"][1]:
            score += 2
            reasons.append("ప్రస్తుత తేమ ఈ పంటకు అనుకూల పరిమితిలో ఉంది." if language == "telugu" else "Current humidity is within the crop comfort range.")
        else:
            score -= 1

    if rain_probability is not None:
        rainfall_level = rain_probability * 2
        if crop["rainfall"][0] <= rainfall_level <= crop["rainfall"][1]:
            score += 1
            reasons.append("వర్షం అవకాశం ఈ పంటకు అనుకూలంగా ఉంది." if language == "telugu" else "Rain chances are acceptable for this crop.")

    if not reasons:
        reasons.append(localize_crop(crop, language)["why"])

    return score, reasons


def filter_crops(user_input):
    shortlisted = []
    for crop in CROP_CATALOG:
        if user_input["country"] not in crop["countries"]:
            continue
        if user_input["region"] not in crop["regions"]:
            continue
        if user_input["category"] != crop["category"]:
            continue
        if user_input["season"] not in crop["seasons"] and "year_round" not in crop["seasons"]:
            continue

        score, reasons = score_crop(crop, user_input)
        localized_crop = localize_crop(crop, user_input.get("language", "english"))
        shortlisted.append(
            {
                "name": localized_crop["name"],
                "why": localized_crop["why"],
                "score": score,
                "reasons": reasons,
                "fertilizer": localized_crop["fertilizer"],
            }
        )

    shortlisted.sort(key=lambda item: item["score"], reverse=True)
    return shortlisted


def build_weather_tips(user_input):
    tips = []
    language = user_input.get("language", "english")
    temperature = user_input["temperature"]
    humidity = user_input["humidity"]
    rain_probability = user_input["rain_probability"]
    weather_code = int(user_input["weather_code"]) if user_input["weather_code"] is not None else None

    if temperature is not None and temperature >= 34:
        tips.append("ఇప్పుడు వేడి ఎక్కువగా ఉంది కాబట్టి ఉదయం లేదా సాయంత్రం అదనంగా నీరు ఇవ్వండి." if language == "telugu" else "Heat is high now, so give plants extra water in early morning or evening.")
    elif temperature is not None and temperature <= 16:
        tips.append("ఉష్ణోగ్రత తక్కువగా ఉంది కాబట్టి అధికంగా నీరు పెట్టకండి, చిన్న మొక్కలను ఒత్తిడినుంచి కాపాడండి." if language == "telugu" else "Temperature is low, so avoid overwatering and protect young plants from stress.")

    rainy_codes = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95}
    if (rain_probability is not None and rain_probability >= 60) or (weather_code in rainy_codes):
        tips.append("వర్షం వచ్చే అవకాశం ఉంది కాబట్టి ప్రస్తుతం నీటిపారుదల అవసరం లేదు." if language == "telugu" else "Rain is likely, so irrigation is not needed right now.")

    if humidity is not None and humidity >= 80:
        tips.append("తేమ ఎక్కువగా ఉంది కాబట్టి వ్యాధుల ముప్పు పెరుగుతుంది. ఆకులపై ఫంగస్ లక్షణాలు ఉన్నాయో చూడండి." if language == "telugu" else "Humidity is high, so disease risk is higher. Check leaves for fungal symptoms.")
    elif humidity is not None and humidity <= 35:
        tips.append("గాలి పొడిగా ఉంది కాబట్టి మల్చింగ్ చేస్తే వేర్ల దగ్గర తేమ నిల్వగా ఉంటుంది." if language == "telugu" else "Air is dry, so mulch can help keep root-zone moisture stable.")

    if not tips:
        tips.append("ప్రస్తుతం వాతావరణం స్థిరంగా ఉంది. నియమిత నీటిపారుదల మరియు పొలం పర్యవేక్షణ కొనసాగించండి." if language == "telugu" else "Weather looks stable now. Continue regular irrigation and field monitoring.")

    return tips


def score_crop(crop, user_input):
    score = 0
    reasons = []
    language = user_input.get("language", "english")
    translation = get_translation(language)
    localized_crop_name = localize_crop_name(crop["name"], language)
    soil_color_label = translation.get(user_input["soil_color"], user_input["soil_color"].title())
    texture_label = translation.get(user_input["texture"], user_input["texture"])

    if user_input["soil_color"] in crop["soil_color"]:
        score += 2
        reasons.append(dynamic_text(language, "soil_color_match", value=soil_color_label))
    if user_input["texture"] in crop["texture"]:
        score += 2
        reasons.append(dynamic_text(language, "soil_texture_match", value=texture_label))
    if user_input["water_absorption"] in crop["water_absorption"]:
        score += 2
        reasons.append(dynamic_text(language, "water_absorption_match", crop=localized_crop_name))

    temperature = user_input["temperature"]
    humidity = user_input["humidity"]
    rain_probability = user_input["rain_probability"]

    if temperature is not None:
        if crop["temperature"][0] <= temperature <= crop["temperature"][1]:
            score += 3
            reasons.append(dynamic_text(language, "temperature_ok"))
        else:
            score -= 1

    if humidity is not None:
        if crop["humidity"][0] <= humidity <= crop["humidity"][1]:
            score += 2
            reasons.append(dynamic_text(language, "humidity_ok"))
        else:
            score -= 1

    if rain_probability is not None:
        rainfall_level = rain_probability * 2
        if crop["rainfall"][0] <= rainfall_level <= crop["rainfall"][1]:
            score += 1
            reasons.append(dynamic_text(language, "rain_ok"))

    if not reasons:
        reasons.append(localize_crop(crop, language)["why"])

    return score, reasons


def build_weather_tips(user_input):
    tips = []
    language = user_input.get("language", "english")
    temperature = user_input["temperature"]
    humidity = user_input["humidity"]
    rain_probability = user_input["rain_probability"]
    weather_code = int(user_input["weather_code"]) if user_input["weather_code"] is not None else None

    if temperature is not None and temperature >= 34:
        tips.append(dynamic_text(language, "tip_heat"))
    elif temperature is not None and temperature <= 16:
        tips.append(dynamic_text(language, "tip_cold"))

    rainy_codes = {51, 53, 55, 61, 63, 65, 80, 81, 82, 95}
    if (rain_probability is not None and rain_probability >= 60) or (weather_code in rainy_codes):
        tips.append(dynamic_text(language, "tip_rain"))

    if humidity is not None and humidity >= 80:
        tips.append(dynamic_text(language, "tip_humidity_high"))
    elif humidity is not None and humidity <= 35:
        tips.append(dynamic_text(language, "tip_humidity_low"))

    if not tips:
        tips.append(dynamic_text(language, "tip_default"))

    return tips


def localize_value_list(values, language, value_map=None):
    location_map = LOCATION_TEXTS.get(language, LOCATION_TEXTS["english"])
    translation = get_translation(language)
    localized = []
    for value in values:
        if value_map == "location":
            localized.append(location_map.get(value, value))
        else:
            localized.append(translation.get(value, value.title() if "_" not in value else value.replace("_", " ").title()))
    return localized


def match_crops(user_input, *, require_region=True, require_season=True):
    shortlisted = []
    for crop in CROP_CATALOG:
        if user_input["country"] not in crop["countries"]:
            continue
        if user_input["category"] != crop["category"]:
            continue
        if require_region and user_input["region"] not in crop["regions"]:
            continue
        if require_season and user_input["season"] not in crop["seasons"] and "year_round" not in crop["seasons"]:
            continue

        score, reasons = score_crop(crop, user_input)
        if not require_region and user_input["region"] in crop["regions"]:
            score += 1
        if not require_season and (user_input["season"] in crop["seasons"] or "year_round" in crop["seasons"]):
            score += 1

        localized_crop = localize_crop(crop, user_input.get("language", "english"))
        shortlisted.append(
            {
                "name": localized_crop["name"],
                "why": localized_crop["why"],
                "score": score,
                "reasons": reasons,
                "fertilizer": localized_crop["fertilizer"],
            }
        )

    shortlisted.sort(key=lambda item: item["score"], reverse=True)
    return shortlisted


def build_no_match_message(user_input, closest_matches=None):
    language = user_input["language"]
    translation = get_translation(language)
    country_crops = [crop for crop in CROP_CATALOG if user_input["country"] in crop["countries"]]

    if not country_crops:
        return f'{translation["no_match_detail"]} {translation["no_match"]}'

    region_options = sorted(
        {
            region
            for crop in country_crops
            if crop["category"] == user_input["category"]
            for region in crop["regions"]
        }
    )
    season_options = sorted(
        {
            season
            for crop in country_crops
            if crop["category"] == user_input["category"]
            for season in crop["seasons"]
        }
    )
    category_options = sorted({crop["category"] for crop in country_crops})

    message_parts = [translation["no_match_detail"]]
    if region_options:
        message_parts.append(
            f'{translation["try_region"]}: {", ".join(localize_value_list(region_options[:4], language, "location"))}.'
        )
    if season_options:
        message_parts.append(
            f'{translation["try_season"]}: {", ".join(localize_value_list(season_options[:4], language))}.'
        )
    if category_options:
        message_parts.append(
            f'{translation["try_category"]}: {", ".join(localize_value_list(category_options[:4], language))}.'
        )
    if closest_matches:
        closest_names = ", ".join(item["name"] for item in closest_matches[:3])
        if closest_names:
            message_parts.append(f'{translation["closest_crops"]}: {closest_names}.')

    return " ".join(message_parts)


def get_crop_matches(user_input):
    strict_matches = match_crops(user_input, require_region=True, require_season=True)
    if strict_matches:
        return strict_matches, False, None

    relaxed_matches = match_crops(user_input, require_region=False, require_season=True)
    if not relaxed_matches:
        relaxed_matches = match_crops(user_input, require_region=True, require_season=False)
    if not relaxed_matches:
        relaxed_matches = match_crops(user_input, require_region=False, require_season=False)

    if relaxed_matches:
        return [], False, build_no_match_message(user_input, relaxed_matches)

    return [], False, build_no_match_message(user_input)


def template_context(language="english", form_data=None, result=None, error=None):
    selected_language = language if language in TRANSLATIONS else "english"
    translation = get_translation(selected_language)
    form_data = form_data or {
        "country": "India",
        "region": "Andhra Pradesh",
        "season": "kharif",
        "category": "vegetables",
        "language": selected_language,
        "soil_color": "black",
        "texture": "soft",
        "water_absorption": "slow",
        "weather_temperature": "",
        "weather_humidity": "",
        "weather_rain_probability": "",
        "weather_code": "",
        "weather_status": "unavailable",
    }

    return {
        "t": translation,
        "translations": TRANSLATIONS,
        "native_language_labels": NATIVE_LANGUAGE_LABELS,
        "location_texts": LOCATION_TEXTS.get(selected_language, LOCATION_TEXTS["english"]),
        "all_location_texts": LOCATION_TEXTS,
        "countries": list(COUNTRY_REGIONS.keys()),
        "regions_by_country": COUNTRY_REGIONS,
        "seasons": ["kharif", "rabi", "summer", "year_round"],
        "categories": ["vegetables", "fruits", "cash_crops", "grains", "pulses", "millets"],
        "form_data": form_data,
        "result": result,
        "error": error,
    }


@app.route("/")
def login():
    return redirect(url_for("home"))


@app.route("/send_otp", methods=["POST"])
def send_otp():
    return redirect(url_for("home"))


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    language = request.args.get("language", session.get("language", "english")).lower()
    session["language"] = language
    return render_template("index.html", **template_context(language=language))


@app.route("/predict", methods=["POST"])
def predict():
    user_input = normalize_form(request.form)
    session["language"] = user_input["language"]

    form_data = {
        "country": user_input["country"],
        "region": user_input["region"],
        "season": user_input["season"],
        "category": user_input["category"],
        "language": user_input["language"],
        "soil_color": user_input["soil_color"],
        "texture": user_input["texture"],
        "water_absorption": user_input["water_absorption"],
        "weather_temperature": request.form.get("weather_temperature", ""),
        "weather_humidity": request.form.get("weather_humidity", ""),
        "weather_rain_probability": request.form.get("weather_rain_probability", ""),
        "weather_code": request.form.get("weather_code", ""),
        "weather_status": request.form.get("weather_status", "unavailable"),
    }

    if user_input["region"] not in get_region_options(user_input["country"]):
        return render_template(
            "index.html",
            **template_context(
                language=user_input["language"],
                form_data=form_data,
                error=build_no_match_message(user_input),
            ),
        )

    matches, used_relaxed_match, match_error = get_crop_matches(user_input)
    if not matches:
        return render_template(
            "index.html",
            **template_context(
                language=user_input["language"],
                form_data=form_data,
                error=match_error or get_translation(user_input["language"])["no_match"],
            ),
        )

    best_crop = matches[0]
    result = {
        "crop": best_crop["name"],
        "why": best_crop["why"],
        "reasons": best_crop["reasons"],
        "tips": build_weather_tips(user_input),
        "alternatives": [item["name"] for item in matches[1:4]],
        "fertilizer": best_crop["fertilizer"],
        "weather_status": user_input["weather_status"],
        "used_relaxed_match": used_relaxed_match,
    }

    return render_template(
        "index.html",
        **template_context(language=user_input["language"], form_data=form_data, result=result),
    )


@app.route("/health")
def health():
    return {"status": "ok"}, 200


@app.errorhandler(Exception)
def handle_exception(error):
    print("Unhandled application error:")
    traceback.print_exc()
    language = session.get("language", "english")
    try:
        return (
            render_template(
                "index.html",
                **template_context(
                    language=language,
                    error="Something went wrong. Please refresh and try again.",
                ),
            ),
            500,
        )
    except Exception:
        return "Application error. Please refresh and try again.", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
