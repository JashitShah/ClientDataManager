import pandas as pd
import os
import os.path
import copy

df = None
filename = "data.csv"

selection = []
undo_stack = []
stack_pointer = 0

if os.path.exists("./" + filename):
    df = pd.read_csv(filename, index_col=[0])
    undo_stack.append(df)
    print("Existing database found!")

else:
    print("Existing database not found. Creating one.")
    df = pd.DataFrame(columns=['company_name',
                               'addressee_name',
                               'number_1',
                               'number_2',
                               'number_3',
                               'email',
                               'website',
                               'salutation',
                               'industry',
                               'state',
                               'city',
                               'address_line_1',
                               'address_line_2',
                               'street',
                               'area',
                               'pincode',
                               'status',
                               'comments'])
    df.to_csv(filename)
    undo_stack.append(df)


def new():
    print("\n\nPlease input bare essential details below.")
    global df
    global filename
    cmp = str(input("company name: "))
    name = str(input("addressee name: "))
    telephone = str(input("enter number: "))
    email = str(input("email: "))
    industry = str(input("industry: "))
    state = str(input("state: "))
    comments = str(input("Please enter comments, if any: "))

    correct = str(input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: "))

    if not (correct == 'y' or correct == 'n'):
        return

    while correct.lower() == 'n':
        print("\n\nWhich ones would you like to correct? Chain them using space separators. Enter nothing to "
              "discard.\n\n")
        print(
            "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n num: NUMBER \n ema: EMAIL \n ind: INDUSTRY \n sta: "
            "STATE \n"
            "com: COMMENTS")
        hook = str(input("\n\nPlease enter your hook here: "))
        arr = hook.split()
        final = list(set(arr))

        for i in range(len(final)):
            if final[i] == 'nam':
                name = str(input("enter new addressee name: "))
            elif final[i] == 'cmp':
                cmp = str(input("enter new company name: "))
            elif final[i] == 'num':
                telephone = str(input("enter new number: "))
            elif final[i] == 'ema':
                email = str(input("enter new email: "))
            elif final[i] == 'ind':
                industry = str(input("enter new industry: "))
            elif final[i] == 'sta':
                state = str(input("enter new state: "))
            elif final[i] == 'com':
                comments = str(input("enter new comments: "))

        correct = input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: ")
        if not (correct == 'y' or correct == 'n'):
            return

    df2 = {'company_name': cmp,
           'addressee_name': name,
           'number_1': telephone,
           'email': email,
           'industry': industry,
           'state': state,
           'comments': comments}

    df.loc[len(df)] = df2
    df.to_csv(filename)
    savetostack(df)


def find():
    global df
    df = df.fillna("")

    print("\n\nPlease define a search criteria as indicated below:\n\n")
    print("\n[MATCH CASE (optional)] [SEARCH CRITERIA 1] and/or [SEARCH CRITERIA 2] and/or ... [SEARCH CRITERIA N]")
    print("[SEARCH CRITERIA] can be 'column_code=string' or '~column_code=string', the latter tilda (~) meaning "
          "negation.\nPlease ensure you put strings in double quotes (\"\")."
          "\nAnything after the equals sign (\"=\") will be found")
    print("\nCase options:\n -t Match case \n -f Do not match case")
    print("\n\nColumn codes:\n nam: Addressee name\n cmp: Company name\n nu1: First number\n nu2: Second number"
          "\n nu3: Third number\n ema: Email\n web: Website\n sal: Salutation\n ind: Industry\n sta: State\n cit: City"
          "\n ad1: Address Line 1\n ad2: Address Line 2\n str: Street\n are: Area\n pin: PIN Code\n sts: Status\n"
          " com: Comments")

    col_codes = [
        ["nam", "addressee_name"],
        ["cmp", "company_name"],
        ["nu1", "number1"],
        ["nu2", "number2"],
        ["nu3", "number3"],
        ["ema", "email"],
        ["web", "website"],
        ["sal", "salutation"],
        ["ind", "industry"],
        ["sta", "state"],
        ["cit", "city"],
        ["ad1", "address_line_1"],
        ["ad2", "address_line_2"],
        ["str", "street"],
        ["are", "area"],
        ["pin", "pincode"],
        ["sts", "status"],
        ["com", "comments"]
    ]

    uinput = str(input("Enter your hook here, ALL to print everything, or enter nothing to exit: "))
    
    if uinput == "ALL":
        print(df)
        return [i for i in range(len(df))]

    if uinput == "":
        return []

    case = False

    if uinput.startswith("-f") or uinput.startswith("-t"):
        if uinput.startswith("-t"):
            case = True
            uinput = uinput[3:]
        else:
            case = False
            uinput = uinput[3:]

    for i in range(len(col_codes)):
        uinput = uinput.replace(col_codes[i][0] + "=", col_codes[i][1] + "=")

    p = 0
    while True:
        if uinput[p] == "=":
            a = uinput.index("\"", p)
            b = uinput.index("\"", a+1)
            uinput = uinput[:b + 1] + ", na;False, case;" + str(case) + ")" + uinput[b + 1:]
            uinput = uinput.replace("=", ".str.contains(", 1)
        if p == len(uinput) - 1:
            break
        p += 1

    uinput = uinput.replace(";", "=")
    try:
        df2 = df.query(uinput, engine='python')
    except pd.errors.UndefinedVariableError:
        print("One of the column names is undefined. Please check your spelling and try again.")
        return []
    print(df2)
    return list(df2.index.values)


def find_and_select():
    global selection
    print("\n\nAll items matching the below search criteria will be selected.")
    arr = find()
    if len(arr) == 0:
        print("Nothing new selected.")
    selection = selection + arr
    selection = list(set(selection))


def minnew():
    global df
    global filename
    print("\n\nMinnew allows you to enter the minimum required details for a new entry. \n\n")
    cmp = input("company name: ")
    name = input("addressee name: ")
    telephone = input("telephone: ")
    email = input("email: ")

    correct = str(input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: "))

    if correct.lower() != "y" and correct.lower() != "n":
        return

    while correct.lower() == "n":
        print("\n\nWhich ones would you like to correct? Chain them using space separators. Enter nothing to discard.")
        print(
            "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n num: NUMBER \n ema: EMAIL")
        hook = str(input("\n\nPlease enter your hook here: "))
        arr = hook.split()
        final = list(set(arr))

        for i in range(len(final)):
            if final[i] == 'nam':
                name = str(input("enter new addressee name: "))
            elif final[i] == 'cmp':
                cmp = str(input("enter new company name: "))
            elif final[i] == 'num':
                telephone = str(input("enter new number: "))
            elif final[i] == 'ema':
                email = str(input("enter new email: "))

        correct = input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: ")
        if not (correct == 'y' or correct == 'n'):
            return

    df2 = {'company_name': cmp,
           'addressee_name': name,
           'number_1': telephone,
           'email': email}

    df.loc[len(df)] = df2
    df.to_csv(filename)
    savetostack(df)


def maxnew():
    print("\n\nMaxnew allows you to enter all details in every field for a new entry\n\n")
    global df
    global filename
    cmp = str(input("company name: "))
    name = str(input("addressee name: "))
    number1 = str(input("first number: "))
    number2 = str(input("second number: "))
    number3 = str(input("third number: "))
    web = str(input("website: "))
    sal = str(input("salutation: "))
    ad1 = str(input("address line 1: "))
    ad2 = str(input("address line 2: "))
    stt = str(input("street: "))
    area = str(input("area: "))
    pin = str(input("pincode: "))
    city = str(input("city: "))
    state = str(input("state: "))
    sta = str(input("communication status: "))
    email = str(input("email: "))
    industry = str(input("industry: "))
    comments = str(input("Please enter comments, if any: "))

    correct = str(input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: "))

    if not (correct == 'y' or correct == 'n'):
        return

    while correct.lower() == 'n':
        print("\n\nWhich ones would you like to correct? Chain them using space separators. Enter nothing to discard.")
        print(
            "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n nu1: FIRST NUMBER \n nu2: SECOND NUMBER \n nu3: THIRD "
            "NUMBER \n web: WEBSITE \n sal: SALUTATION \n ad1: ADDRESS LINE 1 \n ad2: ADDRESS LINE 2 \n str: STREET "
            "\n are: AREA \n pin: PINCODE \n cit: CITY \n sts: STATUS \n ema: EMAIL \n ind: INDUSTRY \n sta: "
            "STATE \n"
            "com: COMMENTS")
        hook = str(input("\n\nPlease enter your hook here: "))
        arr = hook.split()
        final = list(set(arr))

        for i in range(len(final)):
            if final[i] == 'nam':
                name = str(input("enter new addressee name: "))
            elif final[i] == 'cmp':
                cmp = str(input("enter new company name: "))
            elif final[i] == 'nu1':
                number1 = str(input("enter new first number: "))
            elif final[i] == 'nu2':
                number2 = str(input("enter new second number: "))
            elif final[i] == 'nu3':
                number3 = str(input("enter new third number: "))
            elif final[i] == 'web':
                web = str(input("enter new website: "))
            elif final[i] == 'sal':
                sal = str(input("enter new salutation: "))
            elif final[i] == 'ad1':
                ad1 = str(input("enter new address line 1: "))
            elif final[i] == 'ad2':
                ad2 = str(input("enter new address line 2: "))
            elif final[i] == 'str':
                stt = str(input("enter new street: "))
            elif final[i] == 'are':
                area = str(input("enter new area: "))
            elif final[i] == 'pin':
                pin = str(input("enter new pincode: "))
            elif final[i] == 'cit':
                city = str(input("enter new city: "))
            elif final[i] == 'sts':
                sta = str(input("enter new communication status: "))
            elif final[i] == 'ema':
                email = str(input("enter new email: "))
            elif final[i] == 'ind':
                industry = str(input("enter new industry: "))
            elif final[i] == 'sta':
                state = str(input("enter new state: "))
            elif final[i] == 'com':
                comments = str(input("enter new comments: "))

        correct = input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: ")
        if not (correct == 'y' or correct == 'n'):
            return

    df2 = {'company_name': cmp,
           'addressee_name': name,
           'salutation': sal,
           'number_1': number1,
           'email': email,
           'industry': industry,
           'state': state,
           'comments': comments,
           'number_2': number2,
           'number_3': number3,
           'address_line_1': ad1,
           'address_line_2': ad2,
           'street': stt,
           'area': area,
           'pincode': pin,
           'city': city,
           'status': sta,
           'website': web}

    df.loc[len(df)] = df2
    df.to_csv(filename)
    savetostack(df)


def selectivenew():
    global df
    global filename
    print("\n\nSelectivenew allows you to create a new entry by selecting only specific columns.\n\n")
    print("Please define a selection hook by chaining together one or more of these using spaces.")
    print("The hook can contain repetitions but repeated entries won't be asked more than once.")
    print(
        "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n nu1: FIRST NUMBER \n nu2: SECOND NUMBER \n nu3: THIRD "
        "NUMBER \n web: WEBSITE \n sal: SALUTATION \n ad1: ADDRESS LINE 1 \n ad2: ADDRESS LINE 2 \n str: STREET "
        "\n are: AREA \n pin: PINCODE \n cit: CITY \n sts: STATUS \n ema: EMAIL \n ind: INDUSTRY \n sta: "
        "STATE \n"
        "com: COMMENTS")
    name, cmp, number1, number2, number3, web, sal, ad1, ad2, stt, area, pin, city, sta, email, industry, state, comments = "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
    _selectivenew(name, cmp, number1, number2, number3, web, sal, ad1, ad2, stt, area, pin, city, sta, email,
                  industry, state, comments)


def _selectivenew(name, cmp, number1, number2, number3, web, sal, ad1, ad2, stt, area, pin, city, sta, email,
                  industry, state, comments):
    global df
    global filename
    
    hook = str(input("\n\nPlease enter your hook here: "))
    
    if hook == "":
        return
    
    arr = hook.split()
    final = list(set(arr))

    for i in range(len(final)):
        if final[i] == 'nam':
            name = str(input("enter new addressee name: "))
        elif final[i] == 'cmp':
            cmp = str(input("enter new company name: "))
        elif final[i] == 'nu1':
            number1 = str(input("enter new first number: "))
        elif final[i] == 'nu2':
            number2 = str(input("enter new second number: "))
        elif final[i] == 'nu3':
            number3 = str(input("enter new third number: "))
        elif final[i] == 'web':
            web = str(input("enter new website: "))
        elif final[i] == 'sal':
            sal = str(input("enter new salutation: "))
        elif final[i] == 'ad1':
            ad1 = str(input("enter new address line 1: "))
        elif final[i] == 'ad2':
            ad2 = str(input("enter new address line 2: "))
        elif final[i] == 'str':
            stt = str(input("enter new street: "))
        elif final[i] == 'are':
            area = str(input("enter new area: "))
        elif final[i] == 'pin':
            pin = str(input("enter new pincode: "))
        elif final[i] == 'cit':
            city = str(input("enter new city: "))
        elif final[i] == 'sts':
            sta = str(input("enter new communication status: "))
        elif final[i] == 'ema':
            email = str(input("enter new email: "))
        elif final[i] == 'ind':
            industry = str(input("enter new industry: "))
        elif final[i] == 'sta':
            state = str(input("enter new state: "))
        elif final[i] == 'com':
            comments = str(input("enter new comments: "))

    correct = input("\n\nAre these details correct? y for yes, n to correct, or anything else to discard: ")
    if correct == 'y':
        df2 = {'company_name': cmp,
            'addressee_name': name,
            'salutation': sal,
            'number_1': number1,
            'email': email,
            'industry': industry,
            'state': state,
            'comments': comments,
            'number_2': number2,
            'number_3': number3,
            'address_line_1': ad1,
            'address_line_2': ad2,
            'street': stt,
            'area': area,
            'pincode': pin,
            'city': city,
            'status': sta,
            'website': web}
        df.loc[len(df)] = df2
        df.to_csv(filename)
        savetostack(df)

    elif correct == 'n':
        _selectivenew(name, cmp, number1, number2, number3, web, sal, ad1, ad2, stt, area, pin, city, sta, email,
                  industry, state, comments)
                  
    else:
        return


def select(args = []):
    global selection
    global df
    
    if len(args) > 0:
        if str(args[0]) == "ALL":
            for i in range(len(df)):
                selection.append(i)
            selection = list(set(selection))
            return
        for i in range(len(args)):
            if str(args[i]).isnumeric():
                value = int(args[i])
                if value < len(df):
                    selection.append(value)
                else:
                    print(str(value), "exceeds bounds.")
            
            elif "-" in str(args[i]):
                arr = str(args[i]).split("-")
                if str(arr[0]).isnumeric() and str(arr[1]).isnumeric():
                    if int(str(arr[0])) < len(df) and int(str(arr[1])) < len(df):
                        for i in range(int(str(arr[0])), int(str(arr[1])) + 1):
                            selection.append(i)
                    else:
                        print("One or more of the indices is out of bounds.")
                else:
                    print("One of the arguments in", args[i], "is not an integer, therefore invalid.")
                    
            else:
                print(args[i], "is not a valid argument.")
                
    else:
        print("\n\nNO ARGUMENTS FOUND")
        print("\n\n You can select one or multiple items using the select command. \n\n")
        print("You can enter your selection list below following this convention: [int OR int-int] [SPACE] [another int OR int-int]")
        print("The ('-') hyphen signifies a range between the two numbers.")
        arguments = str(input("Enter your selection here, ALL to select everything, or NONE to exit select mode: "))
        if arguments == "NONE" or arguments == "none":
            return
        select(arguments.split(" "))
    
    selection = list(set(selection))
            

def deselect(strinput=""):
    global selection
    deselection = []
    if strinput.strip() == "":
        print("\n\nNo input found.")
        a = str(input("Enter an input here, enter ALL to deselect everything, or enter nothing to exit: "))
        if a.strip() == "":
            return
        else:
            deselect(a)
    else:
        args = strinput.split()
        
        if str(args[0]) == "ALL":
            for i in range(len(df)):
                deselection.append(i)
            deselection = list(set(deselection))
            new_selection = []
            for i in range(len(selection)):
                if not selection[i] in deselection:
                    new_selection.append(selection[i])
            cls()
            selection = new_selection
            return
        for i in range(len(args)):
            if str(args[i]).isnumeric():
                value = int(args[i])
                if value < len(df):
                    deselection.append(value)
                else:
                    print(str(value), "exceeds bounds.")
            
            elif "-" in str(args[i]):
                arr = str(args[i]).split("-")
                if str(arr[0]).isnumeric() and str(arr[1]).isnumeric():
                    if int(str(arr[0])) < len(df) and int(str(arr[1])) < len(df):
                        for i in range(int(str(arr[0])), int(str(arr[1])) + 1):
                            deselection.append(i)
                    else:
                        print("One or more of the indices is out of bounds.")
                else:
                    print("One of the arguments in", args[i], "is not an integer, therefore invalid.")
                    
            else:
                print(args[i], "is not a valid argument.")
        
        deselection = list(set(deselection))
        
    new_selection = []
    for i in range(len(selection)):
        if not selection[i] in deselection:
            new_selection.append(selection[i])
    cls()
    selection = new_selection
        


def cls():
    global selection
    selection.clear()


def edit(n = -1):
    global df
    global filename
    global selection
    if n == -1 and len(selection) > 0:
        print("\n\n")
        a = str(input(str(len(selection)) + " row(s) is/are selected. All of them will be edited at once. Proceed? y for yes, anything else to exit. "))
        if a=='y':
            print("Please define an edit hook by chaining together one or more of these using spaces.")
            print("The hook can contain repetitions but repeated entries won't be asked more than once.")
            print(
                "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n nu1: FIRST NUMBER \n nu2: SECOND NUMBER \n nu3: THIRD "
                "NUMBER \n web: WEBSITE \n sal: SALUTATION \n ad1: ADDRESS LINE 1 \n ad2: ADDRESS LINE 2 \n str: STREET "
                "\n are: AREA \n pin: PINCODE \n cit: CITY \n sts: STATUS \n ema: EMAIL \n ind: INDUSTRY \n sta: "
                "STATE \n"
                "com: COMMENTS")
            name, cmp, number1, number2, number3, web, sal, ad1, ad2, stt, area, pin, city, sta, email, industry, state, comments = "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
            hook = str(input("\n\nPlease enter your hook here or enter nothing to exit: "))
    
            if hook == "":
                return
    
            arr = hook.split()
            final = list(set(arr))

            for i in range(len(final)):
                if final[i] == 'nam':
                    name = str(input("enter new addressee name: "))
                    df.loc[selection, "addressee_name"] = name
                elif final[i] == 'cmp':
                    cmp = str(input("enter new company name: "))
                    df.loc[selection, "company_name"] = cmp
                elif final[i] == 'nu1':
                    number1 = str(input("enter new first number: "))
                    df.loc[selection, "number1"] = number1
                elif final[i] == 'nu2':
                    number2 = str(input("enter new second number: "))
                    df.loc[selection, "number2"] = number2
                elif final[i] == 'nu3':
                    number3 = str(input("enter new third number: "))
                    df.loc[selection, "number3"] = number3
                elif final[i] == 'web':
                    web = str(input("enter new website: "))
                    df.loc[selection, "website"] = web
                elif final[i] == 'sal':
                    sal = str(input("enter new salutation: "))
                    df.loc[selection, "salutation"] = sal
                elif final[i] == 'ad1':
                    ad1 = str(input("enter new address line 1: "))
                    df.loc[selection, "address_line_1"] = ad1
                elif final[i] == 'ad2':
                    ad2 = str(input("enter new address line 2: "))
                    df.loc[selection, "address_line_2"] = ad2
                elif final[i] == 'str':
                    stt = str(input("enter new street: "))
                    df.loc[selection, "street"] = stt
                elif final[i] == 'are':
                    area = str(input("enter new area: "))
                    df.loc[selection, "area"] = area
                elif final[i] == 'pin':
                    pin = str(input("enter new pincode: "))
                    df.loc[selection, "pincode"] = pin
                elif final[i] == 'cit':
                    city = str(input("enter new city: "))
                    df.loc[selection, "city"] = city
                elif final[i] == 'sts':
                    sta = str(input("enter new communication status: "))
                    df.loc[selection, "status"] = sta
                elif final[i] == 'ema':
                    email = str(input("enter new email: "))
                    df.loc[selection, "email"] = email
                elif final[i] == 'ind':
                    industry = str(input("enter new industry: "))
                    df.loc[selection, "industry"] = industry
                elif final[i] == 'sta':
                    state = str(input("enter new state: "))
                    df.loc[selection, "state"] = state
                elif final[i] == 'com':
                    comments = str(input("enter new comments: "))
                    df.loc[selection, "comments"] = comments
                
        else:
            return
        
    elif n >= 0:
        temp = copy.copy(selection)
        cls()
        selection.append(n)
        edit()
        cls()
        selection = temp
    
    else:
        print("Nothing selected.")
        return
        
    df.to_csv(filename)
    savetostack(df)
    

def delete(n = -1):
    global selection
    global df
    global filename
    if n > -1:
        if n >= len(df):
            print(n, "exceeds bounds.")
            return
        df = df.drop([n])
        df = df.reset_index(drop=True)
        df.to_csv(filename)
        savetostack(df)
        return
    if len(selection) > 0:
        a = str(input(str(len(selection)) + " rows will be deleted. Are you sure? y for yes, anything else to exit. "))
        if a == 'y':
            df = df.drop(selection)
            df = df.reset_index(drop=True)
            df.to_csv(filename)
            savetostack(df)
            cls()
        else:
            return
    else:
        print("Nothing selected.")


def sort(inputstr = ""):
    istr = inputstr.strip()
    if istr == "":
        print("\n\n Here you can sort the sheet by any column in ascending or descending order.")
        print("Please use the following format: [COLUMN_CODE][SPACE][(optional)ASCENDING = True/False]")
        print("Here are the column codes:")
        print(
        "\n\n nam: ADDRESSEE NAME \n cmp: COMPANY NAME \n nu1: FIRST NUMBER \n nu2: SECOND NUMBER \n nu3: THIRD "
        "NUMBER \n web: WEBSITE \n sal: SALUTATION \n ad1: ADDRESS LINE 1 \n ad2: ADDRESS LINE 2 \n str: STREET "
        "\n are: AREA \n pin: PINCODE \n cit: CITY \n sts: STATUS \n ema: EMAIL \n ind: INDUSTRY \n sta: "
        "STATE \n"
        "com: COMMENTS")
        uinput = input("Please enter your command here, or enter nothing to exit: ")
        if uinput.strip() == "":
            return
        else:
            sort(uinput)
            
    else:
        arr = istr.split(" ")
        if len(arr) >= 2:
            _sort(str(arr[0]), str(arr[1]))
        else:
            _sort(str(arr[0]))


def _sort(column = "", ascending = ""):
    global df
    global filename
    
    col = column
    asc = True
    if ascending == "False" or ascending == "f" or ascending == "F" or ascending == "false":
        asc = False
    else:
        asc = True
    
    col_codes = [
        ["nam", "addressee_name"],
        ["cmp", "company_name"],
        ["nu1", "number1"],
        ["nu2", "number2"],
        ["nu3", "number3"],
        ["ema", "email"],
        ["web", "website"],
        ["sal", "salutation"],
        ["ind", "industry"],
        ["sta", "state"],
        ["cit", "city"],
        ["ad1", "address_line_1"],
        ["ad2", "address_line_2"],
        ["str", "street"],
        ["are", "area"],
        ["pin", "pincode"],
        ["sts", "status"],
        ["com", "comments"]
    ]
    
    col_names = ["nam", "cmp", "nu1", "nu2", "nu3", "ema", "web", "sal", "ind", "sta", "cit", "ad1", "ad2", "str", "are", "pin", "sts", "com"]
    
    if not col in col_names:
        print("Invalid or no column selected.")
        return
    
    for i in range(len(col_codes)):
        if col_codes[i][0] in col:
            col = col.replace(col_codes[i][0], col_codes[i][1])
            break
    
    df = df.sort_values(by=[col], ascending=asc, na_position="first")
    df = df.reset_index(drop=True)
    df.to_csv(filename)
    savetostack(df)
    

def display():
    global selection
    if len(selection) > 0:
        print(df.iloc[selection])
    else:
        print("Nothing selected.")
    
    
def displayall():
    global df
    print(df.to_string())
    
 
def undo():
    global stack_pointer
    global undo_stack
    global filename
    global df
    
    if stack_pointer > 0:
        stack_pointer -= 1
        df = undo_stack[stack_pointer]
        undo_stack[stack_pointer].to_csv(filename)
        print("Undid once.")
        
    else:
        print("Cannot undo any further.")
    

def redo():
    global stack_pointer
    global undo_stack
    global filename
    global df
    
    if stack_pointer < len(undo_stack) - 1:
        stack_pointer += 1
        undo_stack[stack_pointer].to_csv(filename)
        df = undo_stack[stack_pointer]
        print("Redid once.")
        
    else:
        print("Cannot redo any further.")
    
    
def main():
    command = input("\n\nType a command here, 'help' for help, and 'exit' to exit the application: ")
    arr = command.strip().split(" ")
    
    if arr[0].lower() == "exit":
        return
    elif arr[0].lower() == "help":
        print("\n\nThe following guide will show you how to use this tool.")
        print("These are the commands and their descriptions:")
        print("new/n\t\t\t\t\tCreates a new entry with essential details as inputs.")
        print("minnew/nn\t\t\t\tCreates a new entry with bare minimum details as inputs.")
        print("maxnew/xn\t\t\t\tCreates a new entry with all details as inputs.")
        print("selectivenew/selnew/sn\t\t\tCreates a new entry and allows the user to choose its fields of input.")
        print("find/f\t\t\t\t\tFinds all entries matching a criterion defined by the user. The command itself contains more details.")
        print("findandselect/fselect/fs/fsel\t\tFinds all entries matching a criterion defined by the user and selects them.")
        print("select/sel/s\t\t\t\tSelect item/items. Optionally follow it up with indices or ranges to select them. Example: 2 3-8 19-23")
        print("deselect/desel/ds\t\t\tDeselects already selected indices. Optionally follow it up with indices or ranges to deselect them. Example: 2 3-8 19-23")
        print("sort/st\t\t\t\t\tSort by any column in ascending or descending order. Optionally follow it up with [COLUMN_CODE] [TRUE or FALSE(Ascending?)]")
        print("cls\t\t\t\t\tClear selection.")
        print("edit/ed\t\t\t\t\tEdit selection. Optionally follow it up with any number to edit that specific entry only.")
        print("delete/del\t\t\t\tDelete selection. Optionally follow it up with any number to delete that specific entry only.")
        print("display/dis/d\t\t\t\tDisplay selection.")
        print("displayall/disall/da\t\t\tDisplay everything in full detail.")
        print("undo/u\t\t\t\t\tUndoes once.")
        print("redo/r\t\t\t\t\tRedoes once.")
        main()
    elif arr[0] == "new" or arr[0] == "n":
        new()
        main()
    elif arr[0] == "minnew" or arr[0] == "nn":
        minnew()
        main()
    elif arr[0] == "maxnew" or arr[0] == "xn":
        maxnew()
        main()
    elif arr[0] == "selectivenew" or arr[0] == "selnew" or arr[0] == "sn":
        selectivenew()
        main()
    elif arr[0] == "find" or arr[0] == "f":
        find()
        main()
    elif arr[0] == "findandselect" or arr[0] == "fselect" or arr[0] == "fs" or arr[0] == "fsel":
        find_and_select()
        main()
    elif arr[0] == "select" or arr[0] == "sel" or arr[0] == "s":
        if len(arr) > 1:
            select(arr[1:])
        else:
            select()
        main()
    elif arr[0] == "deselect" or arr[0] == "desel" or arr[0] == "ds":
        if len(arr) > 1:
            deselect(" ".join([i.strip() for i in arr[1:]]))
        else:
            deselect()
        main()
    elif arr[0] == "sort" or arr[0] == "st":
        if len(arr) > 1:
            sort(" ".join([i.strip() for i in arr[1:]]))
        else:
            sort()
        main()
    elif arr[0] == "cls" or arr[0] == "clear" or arr[0] == "clearselection" or arr[0] == "clearsel":
        cls()
        main()
    elif arr[0] == "edit" or arr[0] == "ed":
        if len(arr) > 1:
            if arr[1].isnumeric():
                edit(int(arr[1]))
            else:
                print("Argument invalid.")
        else:
            edit()
        main()
    elif arr[0] == "delete" or arr[0] == "del":
        if len(arr) > 1:
            if arr[1].isnumeric():
                delete(int(arr[1]))
            else:
                print("Argument invalid.")
        else:
            delete()
        main()
    elif arr[0] == "display" or arr[0] == "dis" or arr[0] == "d":
        display()
        main()
    elif arr[0] == "displayall" or arr[0] == "disall" or arr[0] == "da":
        displayall()
        main()
    elif arr[0] == "undo" or arr[0] == "u":
        undo()
        main()
    elif arr[0] == "redo" or arr[0] == "r":
        redo()
        main()
    else:
        print("Invalid command. Please check your spelling or run 'help' for help.")
        main()
    
    
def savetostack(df):
    global undo_stack
    global stack_pointer
    
    if len(undo_stack) > 200 and stack_pointer == len(undo_stack) - 1:
        undo_stack.pop(0)
        stack_pointer -= 1
    
    elif stack_pointer == (len(undo_stack) - 1):
        undo_stack.append(copy.copy(df))
        stack_pointer += 1
        
    elif stack_pointer < (len(undo_stack) - 1) and stack_pointer >= 0:
        del undo_stack[stack_pointer + 1:]
        undo_stack.append(copy.copy(df))
        stack_pointer += 1
        
    else:
        print("Somehow, the stack pointer is invalid.")
        
 
print("WELCOME TO JASHIT SHAH'S DATABASE MANAGER! HOPE THIS TOOL MAKES DATABASE MANAGEMENT EASIER AND FASTER.")
print("Version 1.0\n\n")
main()
 