import os
from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secret123"

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
    return crop_text.get("name", crop_name)


def localize_crop(crop, language):
    crop_text = CROP_TEXTS.get(language, {}).get(crop["name"], {})
    fertilizer_text = crop_text.get("fertilizer", {})
    fertilizer = {}

    for choice, plan in crop["fertilizer"].items():
        localized_plan = fertilizer_text.get(choice, {})
        fertilizer[choice] = {
            "details": localized_plan.get("details", plan["details"]),
            "schedule": localized_plan.get("schedule", plan["schedule"]),
            "ratio": localized_plan.get("ratio", plan["ratio"]),
            "method": localized_plan.get("method", plan["method"]),
        }

    return {
        "name": crop_text.get("name", crop["name"]),
        "why": crop_text.get("why", crop["why"]),
        "fertilizer": fertilizer,
    }


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
    if is_mobile_request():
        return redirect(url_for("home"))
    language = session.get("language", "english")
    return render_template("login.html", t=get_translation(language))


@app.route("/send_otp", methods=["POST"])
def send_otp():
    if is_mobile_request():
        return redirect(url_for("home"))
    mobile = request.form["mobile"]
    otp = random.randint(1000, 9999)
    session["otp"] = str(otp)
    session["mobile"] = mobile
    print("OTP:", otp)
    return render_template("verify.html", t=get_translation(session.get("language", "english")))


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    if is_mobile_request():
        return redirect(url_for("home"))
    user_otp = request.form["otp"]

    if user_otp == session.get("otp"):
        return redirect("/home")

    return render_template(
        "verify.html",
        t=get_translation(session.get("language", "english")),
        error=get_translation(session.get("language", "english"))["invalid_otp"],
    )


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
                error=get_translation(user_input["language"])["no_match"],
            ),
        )

    matches = filter_crops(user_input)
    if not matches:
        return render_template(
            "index.html",
            **template_context(
                language=user_input["language"],
                form_data=form_data,
                error=get_translation(user_input["language"])["no_match"],
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
    }

    return render_template(
        "index.html",
        **template_context(language=user_input["language"], form_data=form_data, result=result),
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
