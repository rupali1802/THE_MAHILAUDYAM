"""
Mahila Udyam - Number Converter
Convert numbers to words in English, Hindi (Romanized), and Tamil (Romanized)
Supports Indian numbering system (lakh, crore)
"""


class NumberConverter:
    """Convert numeric values to words in multiple languages"""

    ONES_EN = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
               'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
               'seventeen', 'eighteen', 'nineteen']

    TENS_EN = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    ONES_HI = ['', 'ek', 'do', 'teen', 'chaar', 'paanch', 'chhah', 'saat', 'aath', 'nau',
               'das', 'gyarah', 'barah', 'terah', 'chaudah', 'pandrah', 'solah', 'satrah',
               'atharah', 'unnees']

    TENS_HI = ['', '', 'bees', 'tees', 'chaalees', 'pachaas', 'saath', 'sattar', 'assee', 'nabbe']

    ONES_TA = ['', 'ondru', 'irandu', 'moondru', 'naangu', 'ainthu', 'aaru', 'ezhu', 'ettu', 'onpathu',
               'pathu', 'pathinondu', 'pannindu', 'pathinmoondru', 'pathinnaangu', 'pathinainthu',
               'pathinaaru', 'pathinezhu', 'pathinettu', 'patthonpathu']

    TENS_TA = ['', '', 'irupathu', 'muppathu', 'naarpathu', 'aimpathu', 'arupathu', 'ezhupathu',
               'enumpathu', 'thonnooru']

    @classmethod
    def _convert_below_100_en(cls, n):
        if n < 20:
            return cls.ONES_EN[n]
        tens = cls.TENS_EN[n // 10]
        ones = cls.ONES_EN[n % 10]
        return tens + (' ' + ones if ones else '')

    @classmethod
    def _convert_below_100_hi(cls, n):
        if n < 20:
            return cls.ONES_HI[n]
        # Hindi has unique words for many numbers
        special = {
            20: 'bees', 21: 'ikkees', 22: 'baees', 23: 'teis', 24: 'chaubeess', 25: 'pachees',
            26: 'chhabbees', 27: 'sattaees', 28: 'atthaees', 29: 'untees',
            30: 'tees', 31: 'ikattees', 32: 'battees', 33: 'taintees', 34: 'chautees',
            35: 'paintees', 36: 'chhattees', 37: 'saintees', 38: 'artees', 39: 'untaalees',
            40: 'chaalees', 41: 'iktaalees', 42: 'bayaalees', 43: 'tentaalees', 44: 'chawaalees',
            45: 'paintaalees', 46: 'chhayaalees', 47: 'santaalees', 48: 'artaalees', 49: 'unchaas',
            50: 'pachaas', 51: 'ikyaavan', 52: 'baavan', 53: 'tirpan', 54: 'chauvan',
            55: 'pachpan', 56: 'chhappan', 57: 'sattavan', 58: 'atthavan', 59: 'unsath',
            60: 'saath', 61: 'iksath', 62: 'baasath', 63: 'tirsath', 64: 'chaunsath',
            65: 'painsath', 66: 'chhayasath', 67: 'sarsath', 68: 'arsath', 69: 'unhattar',
            70: 'sattar', 71: 'ikahattar', 72: 'bahattar', 73: 'tihattar', 74: 'chauhattar',
            75: 'pachhattar', 76: 'chhihattar', 77: 'satahattar', 78: 'atthattar', 79: 'unasi',
            80: 'assee', 81: 'ikyaasi', 82: 'byaasi', 83: 'tiraasi', 84: 'chauraasi',
            85: 'pachaasi', 86: 'chhiyaasi', 87: 'sataasi', 88: 'atthaasi', 89: 'nawaasi',
            90: 'nabbe', 91: 'ikyanwe', 92: 'baanwe', 93: 'tiranwe', 94: 'chauranwe',
            95: 'pachanwe', 96: 'chhiyanwe', 97: 'sattanwe', 98: 'atthanwe', 99: 'ninanwe',
        }
        return special.get(n, cls.TENS_HI[n // 10] + ' ' + cls.ONES_HI[n % 10])

    @classmethod
    def _convert_below_100_ta(cls, n):
        if n < 20:
            return cls.ONES_TA[n]
        tens = cls.TENS_TA[n // 10]
        ones = cls.ONES_TA[n % 10]
        return tens + (' ' + ones if ones else '')

    @classmethod
    def to_words_en(cls, n):
        """Convert integer to English words (Indian number system)"""
        if n == 0:
            return 'zero'
        if n < 0:
            return 'minus ' + cls.to_words_en(-n)

        result = ''
        if n >= 10000000:  # crore
            result += cls.to_words_en(n // 10000000) + ' crore '
            n %= 10000000
        if n >= 100000:  # lakh
            result += cls.to_words_en(n // 100000) + ' lakh '
            n %= 100000
        if n >= 1000:  # thousand
            result += cls.to_words_en(n // 1000) + ' thousand '
            n %= 1000
        if n >= 100:  # hundred
            result += cls.ONES_EN[n // 100] + ' hundred '
            n %= 100
        if n > 0:
            result += cls._convert_below_100_en(n)
        return result.strip()

    @classmethod
    def to_words_hi(cls, n):
        """Convert integer to Hindi words (Romanized)"""
        if n == 0:
            return 'shoonya'
        if n < 0:
            return 'minus ' + cls.to_words_hi(-n)

        result = ''
        if n >= 10000000:
            result += cls.to_words_hi(n // 10000000) + ' karod '
            n %= 10000000
        if n >= 100000:
            result += cls.to_words_hi(n // 100000) + ' laakh '
            n %= 100000
        if n >= 1000:
            result += cls.to_words_hi(n // 1000) + ' hazaar '
            n %= 1000
        if n >= 100:
            result += cls.ONES_HI[n // 100] + ' sau '
            n %= 100
        if n > 0:
            result += cls._convert_below_100_hi(n)
        return result.strip()

    @classmethod
    def to_words_ta(cls, n):
        """Convert integer to Tamil words (Romanized)"""
        if n == 0:
            return 'poojiyam'
        if n < 0:
            return 'kurivum ' + cls.to_words_ta(-n)

        result = ''
        if n >= 10000000:
            result += cls.to_words_ta(n // 10000000) + ' kodi '
            n %= 10000000
        if n >= 100000:
            result += cls.to_words_ta(n // 100000) + ' latcham '
            n %= 100000
        if n >= 1000:
            result += cls.to_words_ta(n // 1000) + ' aayiram '
            n %= 1000
        if n >= 100:
            result += cls.ONES_TA[n // 100] + ' noooru '
            n %= 100
        if n > 0:
            result += cls._convert_below_100_ta(n)
        return result.strip()

    @classmethod
    def to_currency_en(cls, amount):
        """Convert amount to English currency words"""
        amount = float(amount)
        integer_part = int(amount)
        decimal_part = round((amount - integer_part) * 100)

        result = cls.to_words_en(integer_part) + ' rupees'
        if decimal_part > 0:
            result += ' and ' + cls.to_words_en(decimal_part) + ' paise'
        return result

    @classmethod
    def to_currency_hi(cls, amount):
        """Convert amount to Hindi currency words"""
        amount = float(amount)
        integer_part = int(amount)
        decimal_part = round((amount - integer_part) * 100)

        result = cls.to_words_hi(integer_part) + ' rupaye'
        if decimal_part > 0:
            result += ' aur ' + cls.to_words_hi(decimal_part) + ' paise'
        return result

    @classmethod
    def to_currency_ta(cls, amount):
        """Convert amount to Tamil currency words"""
        amount = float(amount)
        integer_part = int(amount)
        decimal_part = round((amount - integer_part) * 100)

        result = cls.to_words_ta(integer_part) + ' roopaay'
        if decimal_part > 0:
            result += ' mattum ' + cls.to_words_ta(decimal_part) + ' paisa'
        return result

    @classmethod
    def convert(cls, amount, language='en', currency=True):
        """Main conversion method"""
        try:
            if currency:
                if language == 'hi':
                    return cls.to_currency_hi(amount)
                elif language == 'ta':
                    return cls.to_currency_ta(amount)
                else:
                    return cls.to_currency_en(amount)
            else:
                if language == 'hi':
                    return cls.to_words_hi(int(amount))
                elif language == 'ta':
                    return cls.to_words_ta(int(amount))
                else:
                    return cls.to_words_en(int(amount))
        except Exception:
            return str(amount)


# Convenience function
def number_to_words(number, language='en', currency=True):
    return NumberConverter.convert(number, language, currency)


if __name__ == '__main__':
    # Test
    test_amounts = [0, 1, 15, 42, 100, 500, 1000, 15000, 100000, 1500000, 10000000]
    for amt in test_amounts:
        print(f"{amt}: EN={NumberConverter.to_words_en(amt)} | HI={NumberConverter.to_words_hi(amt)} | TA={NumberConverter.to_words_ta(amt)}")
