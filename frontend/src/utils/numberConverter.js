/**
 * Convert numbers to spoken words in Hindi and Tamil
 * For use in Sakhi's voice output
 */

// Hindi number words
const HINDI_UNITS = [
  '', 'ek', 'do', 'teen', 'char', 'panch', 'chah', 'saat', 'aath', 'nau'
];

const HINDI_TEENS = [
  'das', 'gyarah', 'barah', 'terah', 'chaudah', 'pandrah', 'solas', 'satrah', 'athaarah', 'unnis'
];

const HINDI_TENS = [
  '', '', 'bees', 'tees', 'chalis', 'pachas', 'saath', 'sattar', 'assi', 'nabbe'
];

const HINDI_SCALES = [
  { value: 10000000, name: 'crore' },
  { value: 100000, name: 'lakh' },
  { value: 1000, name: 'hajar' },
  { value: 100, name: 'sau' },
];

// Tamil number words
const TAMIL_UNITS = [
  '', 'oru', 'iruppu', 'munutru', 'nanka', 'anju', 'aru', 'eru', 'ettu', 'thozhambai'
];

const TAMIL_TEENS = [
  'pathu', 'pattinoru', 'pattiruvvu', 'pattinmunutru', 'pattumannka', 'pattuanju', 
  'pattaru', 'patteru', 'pattettu', 'pattonthombai'
];

const TAMIL_TENS = [
  '', '', 'iruppattu', 'munutruttu', 'nanpattu', 'anpattu', 'aruppattu', 'erupattu', 'ettupattu', 'tonnattu'
];

const TAMIL_SCALES = [
  { value: 10000000, name: 'kodi' },
  { value: 100000, name: 'latcham' },
  { value: 1000, name: 'aayiram' },
  { value: 100, name: 'nooru' },
];

/**
 * Convert number to Hindi words
 * @param {number} num - The number to convert
 * @returns {string} - Hindi spoken representation
 */
export function numberToHindi(num) {
  if (num === 0) return 'zero';
  if (num < 0) return 'minus ' + numberToHindi(Math.abs(num));

  let result = '';
  
  for (let scale of HINDI_SCALES) {
    if (num >= scale.value) {
      const quotient = Math.floor(num / scale.value);
      result += convertHindiThreeDigits(quotient) + ' ' + scale.name + ' ';
      num = num % scale.value;
    }
  }

  if (num > 0) {
    result += convertHindiThreeDigits(num);
  }

  return result.trim();
}

/**
 * Convert 3-digit number to Hindi
 */
function convertHindiThreeDigits(num) {
  if (num === 0) return '';
  
  let result = '';
  
  const hundreds = Math.floor(num / 100);
  if (hundreds > 0) {
    result += HINDI_UNITS[hundreds] + ' sau ';
  }

  const remainder = num % 100;
  if (remainder >= 20) {
    const tens = Math.floor(remainder / 10);
    const units = remainder % 10;
    result += HINDI_TENS[tens];
    if (units > 0) result += ' ' + HINDI_UNITS[units];
  } else if (remainder >= 10) {
    result += HINDI_TEENS[remainder - 10];
  } else if (remainder > 0) {
    result += HINDI_UNITS[remainder];
  }

  return result.trim();
}

/**
 * Convert number to Tamil words
 */
export function numberToTamil(num) {
  if (num === 0) return 'zero';
  if (num < 0) return 'negative ' + numberToTamil(Math.abs(num));

  let result = '';
  
  for (let scale of TAMIL_SCALES) {
    if (num >= scale.value) {
      const quotient = Math.floor(num / scale.value);
      result += convertTamilThreeDigits(quotient) + ' ' + scale.name + ' ';
      num = num % scale.value;
    }
  }

  if (num > 0) {
    result += convertTamilThreeDigits(num);
  }

  return result.trim();
}

/**
 * Convert 3-digit number to Tamil
 */
function convertTamilThreeDigits(num) {
  if (num === 0) return '';
  
  let result = '';
  
  const hundreds = Math.floor(num / 100);
  if (hundreds > 0) {
    result += TAMIL_UNITS[hundreds] + ' nooru ';
  }

  const remainder = num % 100;
  if (remainder >= 20) {
    const tens = Math.floor(remainder / 10);
    const units = remainder % 10;
    result += TAMIL_TENS[tens];
    if (units > 0) result += ' ' + TAMIL_UNITS[units];
  } else if (remainder >= 10) {
    result += TAMIL_TEENS[remainder - 10];
  } else if (remainder > 0) {
    result += TAMIL_UNITS[remainder];
  }

  return result.trim();
}

/**
 * Format amount as spoken currency in selected language
 */
export function amountToSpeech(amount, language) {
  let numPart = '';
  
  if (language === 'hi') {
    numPart = numberToHindi(amount);
    return numPart + ' rupaye';
  } else if (language === 'ta') {
    numPart = numberToTamil(amount);
    return numPart + ' rubai';
  } else {
    // English
    return formatEnglishNumber(amount) + ' rupees';
  }
}

/**
 * Format number in English words
 */
function formatEnglishNumber(num) {
  const ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'];
  const teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'];
  const tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];

  function convertThreeDigits(n) {
    let result = '';
    if (n >= 100) {
      result += ones[Math.floor(n / 100)] + ' hundred ';
      n %= 100;
    }
    if (n >= 20) {
      result += tens[Math.floor(n / 10)];
      if (n % 10 > 0) result += ' ' + ones[n % 10];
    } else if (n >= 10) {
      result += teens[n - 10];
    } else if (n > 0) {
      result += ones[n];
    }
    return result.trim();
  }

  if (num === 0) return 'zero';
  if (num < 0) return 'minus ' + formatEnglishNumber(Math.abs(num));

  let result = '';
  
  if (num >= 10000000) {
    result += convertThreeDigits(Math.floor(num / 10000000)) + ' crore ';
    num %= 10000000;
  }
  if (num >= 100000) {
    result += convertThreeDigits(Math.floor(num / 100000)) + ' lakh ';
    num %= 100000;
  }
  if (num >= 1000) {
    result += convertThreeDigits(Math.floor(num / 1000)) + ' thousand ';
    num %= 1000;
  }
  if (num > 0) {
    result += convertThreeDigits(num);
  }

  return result.trim();
}
