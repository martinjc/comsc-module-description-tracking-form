from lib.handbookdata import get_module_list

if __name__ == "__main__":

    modules = get_module_list('COMSC')

    year1 = []
    year2 = []
    year3 = []
    msc = []
    nsa_year1 = []
    nsa_year2 = []
    nsa_year3 = []

    for module in modules:

        mcode = module['moduleCode']

        if mcode.startswith('CM1'):
            year1.append(mcode)
        elif mcode.startswith('CM2'):
            year2.append(mcode)
        elif mcode.startswith('CM3'):
            year3.append(mcode)
        elif mcode.startswith('CMT'):
            msc.append(mcode)
        elif mcode.startswith('CM61'):
            nsa_year1.append(mcode)
        elif mcode.startswith('CM62'):
            nsa_year2.append(mcode)
        elif mcode.startswith('CM63'):
            nsa_year3.append(mcode)

    print(year1)
    print(year2)
    print(year3)
    print(msc)
    print(nsa_year1)
    print(nsa_year2)
    print(nsa_year3)
