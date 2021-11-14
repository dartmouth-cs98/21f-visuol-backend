# For simplicity, will assume either single or married filing separately. Hard to compare with married filing jointly without spousal data.
# Tax data from https://www.tax-brackets.org/federaltaxtable
def fed_tax(income, married):
    remaining_income = 0
    if(married=='married'):
        tax_brackets = {
            0: .1,
            9875: .12,
            40125: .22,
            85525: .24,
            163300: .32,
            207350: .35,
            311025: .37,
        }
        brackets = list(tax_brackets.keys())
        for i in range(len(brackets)):
            if(income > brackets[i]):
                if(i == len(brackets) - 1):
                    remaining_income += (income - brackets[i]) * tax_brackets[brackets[i]]
                else:
                    remaining_income += ((min(income, brackets[i + 1]) - brackets[i]) * tax_brackets[brackets[i]])
    else:
        tax_brackets = {
            0: .1,
            9875: .12,
            40125: .22,
            85525: .24,
            163300: .32,
            207350: .35,
            518400: .37,
        }
        brackets = list(tax_brackets.keys())
        for i in range(len(brackets)):
            if(income > brackets[i]):
                if(i == len(brackets) - 1):
                    remaining_income += (income - brackets[i]) * (tax_brackets[brackets[i]])
                else:
                    remaining_income += ((min(income, brackets[i + 1]) - brackets[i]) * (tax_brackets[brackets[i]]))
    return remaining_income/income