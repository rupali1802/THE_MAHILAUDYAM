/**
 * Sakhi Personality System
 * Warm, knowledgeable voice AI assistant
 * Speaks only in the selected language
 */

const SAKHI_RESPONSES = {
  // GREETINGS & IDENTIFICATION
  greetings: {
    en: "Hi! I'm Sakhi, here to help you build a strong business. What can I help you with today?",
    hi: "Namaste! Mein Sakhi hoon, aapke business ko strong banane mein aapki madad karne ke liye. Aap mujhe kya bataana chaahti hain?",
    ta: "Vanakkam! Naan Sakhi, unakku oru powerful business virkaiyai mattum ullathukkaga un uravi. Ethaa solla vendum?",
  },

  notAI: {
    en: "No I am Sakhi and I am here to help women like you build a strong business. Now tell me what you need.",
    hi: "Nahi, mein Sakhi hoon aur main aapko ek mzboot vyapaar banane mein madad karne ke liye hoon. Ab batao tumhe kya chahiye.",
    ta: "Illa, naan Sakhi. Naan unnai powerful vyapar irukka vettu. Ena vendum?",
  },

  // INCOME & EXPENSE HELP
  recordIncome: {
    en: "So to record income, tell me the amount and what you sold. For example you could say 500 rupees from vegetable sales or 2000 from tailoring.",
    hi: "To aay record karne ke liye mujhe batao ruppaye ki sankhya aur kya becha ho. Jaisa ke 500 rupaye sabzi se ya 2000 sewayi se.",
    ta: "Varumanam padikka ammavaalan sutratu kura enbadai sonnu. Jaisa 500 kaaikari vilai ya 2000 thozhilai vilai.",
  },

  addExpense: {
    en: "So tell me what expense you want to add, the amount, and what it was for. For example 200 rupees for transport or 500 for materials.",
    hi: "Batao kaun sa kharcha add karna hai, kitnaa hai, aur kis liye tha. Jaisa 200 transport or 500 materials ke liye.",
    ta: "Sollu ethaa selavu, kuthiyethu, ethukaga? 200 payanam ya 500 sarukkiyi.",
  },

  // SCHEMES & LOANS
  mudraLoan: {
    en: "Mudra Loan has three levels. First is Shishu with fifty thousand rupees maximum. Then Kishore gives you up to five lakh. The highest is Tarun which goes up to ten lakh rupees. All three have simple approval and very low interest rates. I will show you the official link on your screen so you can apply directly.",
    hi: "Mudra loan ke teen levels hain. Pehla Shishu mein paanch hajar rupaye milte hain. Phir Kishore mein paanch lakh tak. Sabse bada Tarun hai jo das lakh tak deta hai. Sab ke liye approval asaan hai aur interest bahut kam hai. Main aapko official link dikhatiun hoon taki aap direct apply kar sakein.",
    ta: "Mudra loan muninru kayumkum irukku. Shishu - anju aayiram. Kishore - anju latcham. Tarun - pathu latcham rubai. VeLai solluki mathipu adhigam vilai. Naain official link kaatathu.",
  },

  standUpIndia: {
    en: "Stand Up India is for women and SC ST entrepreneurs. You can get between ten lakh and one crore rupees. The approval process is faster and they give very good support. Let me show you the official link so you can start your application today.",
    hi: "Stand Up India mahilaon aur SC ST ke liye hai. Aap ko das lakh se ek crore tak rupaye mil sakte hain. Approval process jaldi hota hai aur support bahut badhiya hai. Main aapko link dikhata hoon taaki aaj hi apply kar sakein.",
    ta: "Stand Up India penmanirum SC ST yarkum. Pathu latcham irundhu oru kodi rubai. Mattutta solluki kathirayan. Naain link kaatathu.",
  },

  // NUMBERS & AMOUNTS
  // These are included in numberConverter.js
  
  // FOLLOW UP QUESTIONS
  followUpQuestions: {
    en: [
      "So tell me what kind of business are you thinking of starting?",
      "Which state are you from because that will help me find the best schemes available for you there?",
      "Have you registered your business yet or are you still planning?",
      "What's your main business activity - are you selling products or providing services?",
      "Have you applied for MUDRA loan before or is this your first time?",
    ],
    hi: [
      "To batao kaun se business ke baare mein soch rahe ho?",
      "Aap kaun se state se ho? Yeh janne se main best yojanayen suggest kar sakti hoon.",
      "Kya apna business register karwaa liya ya abhi planning stage mein ho?",
      "Aapka main business kya hai - product bech rahe ho ya service de rahe ho?",
      "Kya pehle Mudra loan apply kiya hai ya pehli baar ho?",
    ],
    ta: [
      "Sollu ethaa business irunthu vizhainundrai sokku?",
      "Nee ethaa nattilai irundhai? Attukaga best thittagal katathu.",
      "Business padhkaram pannittai ya ippothu nenaykittai?",
      "Nei ethaa kaiyam - karai vittai ya sevai kotta vittai?",
      "Mudra loan kuda mattum ventudai ya inthamuththu mattai?",
    ],
  },

  // SUPPORT MESSAGES
  errorProcessing: {
    en: "Sorry, I didn't quite get that. Could you say it again please?",
    hi: "Maafi chahti hoon, samajh nahi aayi. Dobara bataogi na?",
    ta: "Manakkanum, purithavillai. Punarpadi solnavanam?",
  },

  successMessage: {
    en: "Great! I've recorded that for you.",
    hi: "Bilkul! Main yeh record kar deti hoon.",
    ta: "Sari! Padikka vendiyadhu seittai.",
  },
};

export default SAKHI_RESPONSES;
